# -*- coding: utf-8 -*-
from statechartObjects.State import*
from statechartObjects.Transition import*
from statechartObjects.Statechart import*
from statechartObjects.HistoryState import*
from statechartObjects.Onentry import*
from statechartObjects.Onexit import*
from Misc import*
from classObjects.Class import*
from classObjects.Method import*
from classObjects.Association import*
from classObjects.Inheritance import*
from classObjects.Constructor import*
from classObjects.Destructor import*
from classObjects.Attribute import*
import xml.etree.ElementTree as ET
import sys

class ModelParser():

    def parseModel(self, file):
        tree = ET.parse(file)
        root = tree.getroot()
        classes = {}
        statecharts = {}
        statesPerLevel = {}
        author = root.get('author')
        modelName = root.get('name')
        inport = root.find('inport').get('name') if root.find('inport') != None else None
        outport = root.find('outport').get('name') if root.find('outport') != None else None
        top = root.find('top').text.strip() if root.find('top') != None else None
        description = root.find('description').text.strip() if root.find('description') != None else None
        miscInfo = Misc(author, modelName, top, inport, outport, description)

        #process classes
        for cl in root.findall('class'):
            newClass = self.processClass(cl)
            classes[newClass.name] = newClass
            
            #process associated statechart
            for statechart in cl.findall('scxml'):
                initialState = statechart.get('initial')
                states = {}
                newStatechart = Statechart(initialState, states)
                statecharts[newClass.name] = newStatechart
                level = 0
                self.processStates(statechart, newStatechart, level, statesPerLevel) 
                    
        return classes, statecharts, statesPerLevel, miscInfo
                
    def hasChildren(self, state):
        return state.find('state') != None

    def processStates(self, statechart, newStatechart, level, statesPerLevel):
        if not level in statesPerLevel:
            statesPerLevel[level] = []
        allStates = statechart.findall('state') + statechart.findall('parallel')
        #is it logical to lump history states together with states and parallel states even though they can't be the top element?
        for state in allStates:
            parallel = False if state.tag == "state" else True
            stateId = state.get('id')
            transitions = []
            initialState = state.get('initial') #if its not a composite state, its None
            childStates = {}
            parentState = None if level == 0 else newStatechart
            
            onentry = state.find('onentry')
            newOnentry = Onentry('', '', '')
            if(onentry != None):
                entryScript = onentry.find('script').text.strip() if onentry.find('script') != None else None
                entryLog = onentry.find('log').text.strip() if onentry.find('log') != None else None
                entryRaise = onentry.find('raise').text.strip() if onentry.find('raise') != None else None
                newOnentry = Onentry(entryScript, entryLog, entryRaise)

            onexit = state.find('onexit')
            newOnexit = Onexit('', '', '')
            if(onexit != None):
                exitScript = onexit.find('script').text.strip() if onexit.find('script') != None else None
                exitLog = onexit.find('log').text.strip() if onexit.find('log') != None else None
                exitRaise = onexit.find('raise').text.strip() if onexit.find('raise') != None else None
                newOnexit = Onexit(exitScript, exitLog, exitRaise)
                
            newState = State(stateId, transitions, newOnentry, newOnexit, initialState, childStates, parentState, parallel)                
            newStatechart.addState(newState)
            
            #process outgoing transitions
            for transition in state.findall('transition'):
                script = transition.find('script') 
                target = transition.get('target')
                after = transition.get('after')
                event = transition.get('event')
                if after == None:
                    after = -1
                newTransition = Transition(target, event, float(after), script)
                newState.addTransition(newTransition)
    
            for historyState in state.findall('history'):
                name = historyState.get('id')
                kind = historyState.get('type')
                if kind == None:
                    kind = "shallow"
                newHistoryState = HistoryState(name, kind, parentState)
                newState.addState(newHistoryState)
                if not level+1 in statesPerLevel:
                    statesPerLevel[level+1] = []
                statesPerLevel[level+1].append(newHistoryState) #######
                
            if self.hasChildren(state): #or initialState != None. doesnt catch history states! (it doesnt make sense to though)
                newLevel = level + 1
                self.processStates(state, newState, newLevel, statesPerLevel)
    
            statesPerLevel[level].append(newState)
            print(statesPerLevel)
                       
    def processClass(self, cl):
        xmlClassName = cl.get('name')
        methods = []
        relationships = []
        attributes = []
        constructors = []
        destructors = []
        default = cl.get('default')
        relationshipsXML = cl.find('relationships')
        
        for assoc in relationshipsXML.findall('association'):
            name = assoc.get('name')
            className = assoc.get('class')
            min_ = assoc.get('min') if assoc.get('min') != None else 0
            max_ = assoc.get('max') if assoc.get('max') != None else float('inf')
            association = Association(name, className, min_, max_)
            relationships.append(association)
            
        for i in relationshipsXML.findall('inheritance'):
            name = i.get('name')
            priority = i.get('priority') if i.get('priority') != None else 0
            inheritance = Inheritance(name, priority)
            relationships.append(inheritance)
        
        for attr in cl.findall('attribute'):
            name = attr.get('name')
            type_ = attr.get('type')
            at = Attribute(name, type_)
            attributes.append(at)
        
        for method in cl.findall('method'):
            methodName = method.get('name')
            body = method.find('body').text.strip()
            newMethod = Method(methodName, body)
            methods.append(newMethod)
            
        for constructs in cl.findall('constructor'):
            parameters = []
            body = i.get('body') if i.get('body') != None else ''
            constructor = Constructor(parameters, body)
            constructors.append(constructor)
            
        for destructs in cl.findall('destructor'):
            body = i.get('body') if i.get('body') != None else ''
            destructor = Destructor(body)
            destructors.append(destructor)
            
        newClass = Class(xmlClassName, methods, relationships, attributes, constructors, destructors, default)
        return newClass