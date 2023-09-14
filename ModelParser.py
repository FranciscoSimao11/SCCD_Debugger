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
                    
                    #process onentry scripts
                    entryScript = state.find('./onentry/script')
                    if entryScript != None:
                        entryScript = entryScript.text.strip()
                        
                    #process onexit scripts
                    exitScript = state.find('./onexit/script')
                    if exitScript != None:
                        exitScript = exitScript.text.strip()
                        
                    newState = State(stateId, transitions, entryScript, exitScript)
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
                    
        return classes, statecharts
                

    # associate transitions with the objects of their target states instead of simply the stateId 
    # should I do this or should I get the state from the states dictionary everytime im doing a transition?
    # def fixTransitions(self, states):
    #     for state in states.values():
    #         for transition in state.transitions:
    #             targetName = transition.target
    #             transition.target = states[targetName]

    

    #para cada transicao. substituir o nome target pelo actual estado
    #ou criar um mapa para dar match na altura da execucao? execuçao mais lenta ou startup mais lento?