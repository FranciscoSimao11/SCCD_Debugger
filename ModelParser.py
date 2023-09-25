# -*- coding: utf-8 -*-
from State import *
from Transition import *
from Class import*
from Method import*
from Statechart import*
from HistoryState import*
from Misc import*
from Association import*
from Inheritance import*
import xml.etree.ElementTree as ET
import sys

class ModelParser():

    # def __init__(self):
    #          self.states = []
    

    
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
            className = cl.get('name')
            methods = []
            relationships = []
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
            
            newClass = Class(className, methods, relationships, default)
            classes[className] = newClass
            
            #process class methods
            for method in cl.findall('method'):
                methodName = method.get('name')
                body = method.find('body').text.strip()
                newMethod = Method(methodName, body)
                newClass.addMethod(newMethod)
                
            #process associated statechart
            for statechart in cl.findall('scxml'):
                initialState = statechart.get('initial')
                states = {}
                newStatechart = Statechart(initialState, states)
                statecharts[className] = newStatechart
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
            if(state.tag == "state"):
                parallel = False
            else:
                parallel = True
            stateId = state.get('id')
            transitions = []
            initialState = state.get('initial') #if its not a composite state, its None
            childStates = {}
            
            if level == 0:
                parentState = None
            else:
                parentState = newStatechart
            
            #process onentry scripts
            entryScript = state.find('./onentry/script')
            if entryScript != None:
                entryScript = entryScript.text.strip()
                
            #process onexit scripts
            exitScript = state.find('./onexit/script')
            if exitScript != None:
                exitScript = exitScript.text.strip()
            
            newState = State(stateId, transitions, entryScript, exitScript, initialState, childStates, parentState, parallel)                
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
            
                
    # associate transitions with the objects of their target states instead of simply the stateId 
    # should I do this or should I get the state from the states dictionary everytime im doing a transition?
    # def fixTransitions(self, states):
    #     for state in states.values():
    #         for transition in state.transitions:
    #             targetName = transition.target
    #             transition.target = states[targetName]

    

    #para cada transicao. substituir o nome target pelo actual estado
    #ou criar um mapa para dar match na altura da execucao? execuçao mais lenta ou startup mais lento?