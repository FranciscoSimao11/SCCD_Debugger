# -*- coding: utf-8 -*-
from State import *
from Transition import *

class ModelParser():

    # def __init__(self):
    #          self.states = []
    

    
    def parseModel(self, file):
        states = {}
        for each in file:
            line = each.strip()
            if "<scxml" in line:
                parts = line.split(' ')
                initialStateId = parts[1][9:-2]
            elif "<state id" in line:                
                parts = line.split(' ')
                stateId = parts[1][4:-2]
                state = State(stateId, [], '')
                currState = state
                states[stateId] = state
            elif "<transition" in line:
                parts = line.split(' ')
                target = ''
                event = ''
                after = ''
                for each in parts:
                    if "target" in each:
                        target = each[11:-1] #8 starts at 11 to remove the string b4 the name
                    elif "event" in each:
                        event = each[7:-1]
                    elif "after" in each:
                        after = each[7:-1]
                targetName = target
                transition = Transition(target, event, after)
                currState.addTransition(transition)
        self.fixTransitions(states)
        return (states, initialStateId)


    #associate transitions with the objects of their target states instead of simply the stateId 
    #should I do this or should I get the state from the states dictionary everytime im doing a transition?
    def fixTransitions(self, states):
        for state in states.values():
            for transition in state.transitions:
                targetName = transition.target
                transition.target = states[targetName]

    

    #para cada transicao. substituir o nome target pelo actual estado
    #ou criar um mapa para dar match na altura da execucao? execuçao mais lenta ou startup mais lento?