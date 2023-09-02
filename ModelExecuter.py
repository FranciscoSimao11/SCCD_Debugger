# -*- coding: utf-8 -*-
from State import *
from Transition import *
from Timer import *

class ModelExecuter():

    # def __init__(self):
    #          self.states = []
    

    def executeModel(self, states, initialStateId):
        print("Started Execution")
        initialState = states[0]
        #initialState = states[initialStateId]
        finalState = states[1]
        currState = initialState
        while currState != finalState:
            print("Current State: " + currState.name)
            for t in currState.transitions: #threads? if there are several transitions
                print(t.getPrintableObject())
                timer = Timer()
                timer.start()
                time.sleep(t.getTimerFloat())
                timer.stop()
                firstStop = t #this doesnt work with more than 1 state, ideas?
            currState = firstStop.target
        print("Finished Execution in state: " + currState.name)
        return states