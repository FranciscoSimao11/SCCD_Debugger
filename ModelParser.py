# -*- coding: utf-8 -*-
from State import *
from Transition import *
from Class import*
from Method import*
from Statechart import*
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
        
        #process classes
        for cl in root.findall('class'):
            className = cl.get('name')
            methods = []
            relationships = []
            default = cl.get('default')
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
                
                #process statechart states
                for state in statechart.findall('state'):
                    stateId = state.get('id')
                    transitions = []
                    newState = State(stateId, transitions)
                    newStatechart.addState(newState)
                    
                    #process onentry scripts
                    for entryScript in state.findall('onentry'):
                        script = entryScript.find('script')
                        
                    #process onexit scripts
                    for exitScript in state.findall('onexit'):
                        script = exitScript.find('script')
                    
                    #process outgoing transitions
                    for transition in state.findall('transition'):
                        script = transition.find('script')
                        target = transition.get('target')
                        after = transition.get('after')
                        event = transition.get('event')
                        if after == None:
                            after = -1
                        newTransition = Transition(target, event, float(after))
                        newState.addTransition(newTransition)
                    
                        
        return classes, statecharts
                

        
    # def parseModel(self, file):
    #     classes = {}
    #     states = {}
    #     middleOfScript = False
    #     middleOfMethod = False
    #     for each in file:
    #         line = each.strip()
    #         if "<scxml" in line:
    #             parts = line.split(' ')
    #             initialStateId = parts[1][9:-2]
    #         elif "<state id" in line:                
    #             parts = line.split(' ')
    #             stateId = parts[1][4:-2]
    #             state = State(stateId, [], '')
    #             currState = state
    #             states[stateId] = state
    #         elif "<transition" in line:
    #             parts = line.split(' ')
    #             target = ''
    #             event = ''
    #             after = -1 
    #             for each in parts:
    #                 if "target" in each:
    #                     target = each[11:-1] #8 starts at 11 to remove the string b4 the name
    #                 elif "event" in each:
    #                     event = each[7:-1]
    #                 elif "after" in each:
    #                     after = float(each[7:-1])
    #             targetName = target
    #             transition = Transition(target, event, after)
    #             currState.addTransition(transition)
    #         elif "<class" in line:
    #             parts = line.split(' ')
    #             name = ''
    #             defaultClass = ''
    #             for each in parts:
    #                 if "name" in each:
    #                     name = each[6:-1]
    #                 elif "default" in each:
    #                     defaultClass = each[9:-1]
    #                     if defaultClass == "false":
    #                         defaultClass = False
    #                     else:
    #                         defaultClass = True
    #             newClass = Class(name, [], [], defaultClass)
    #             currClass = newClass
    #             classes[name] = newClass
    #         elif "<method" in line:
    #             print("method")
    #             parts = line.split(' ')
    #             name = ''
    #             method = Method(name, '')
    #             currMethod = method
    #             middleOfMethod = True
    #         elif middleOfMethod:
    #             currMethod.text += line + "\n"
    #             print(currMethod.text)
    #         elif "</method" in line:
    #             print("end of method")
    #             middleOfMethod = False
    #             currMethod.text = currMethod.text[6:-8] 
    #             currClass.addMethod(currMethod)
    #         elif "<script" in line:
    #             print("script")
    #             middleOfScript = True
    #             currScript = ''
    #         elif middleOfScript:
    #             currScript += line + "\n"
    #         elif "</script" in line:
    #             print("end of script")
    #             middleOfScript = False
    #             currState.script = currScript[:-2]
           
    #     self.fixTransitions(states)
    #     return (states, classes, initialStateId)


    #associate transitions with the objects of their target states instead of simply the stateId 
    #should I do this or should I get the state from the states dictionary everytime im doing a transition?
    # def fixTransitions(self, states):
    #     for state in states.values():
    #         for transition in state.transitions:
    #             targetName = transition.target
    #             transition.target = states[targetName]

    

    #para cada transicao. substituir o nome target pelo actual estado
    #ou criar um mapa para dar match na altura da execucao? execuçao mais lenta ou startup mais lento?