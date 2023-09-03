# -*- coding: utf-8 -*-
from State import *
from Transition import *
from Timer import *
import sys

class ModelExecuter():

    def executeModel(self, states, initialStateId):
        print("Started Execution")
        initialState = states[initialStateId]
        #finalState = states[1]
        finalState = states["state_B"]
        currState = initialState
        while currState != finalState:
            print("Current State: " + currState.name)
            transitionToExecute = self.checkSmallestTimer(currState.transitions)
            print(transitionToExecute.getPrintableObject())
            timer = Timer()
            timer.start()
            time.sleep(transitionToExecute.getTimerFloat())
            timer.stop()
            currState = transitionToExecute.target
        print("Finished Execution in state: " + currState.name)
        return states


    def checkSmallestTimer(self, transitions):
        smallest = sys.float_info.max
        for t in transitions:
            if t.getTimerFloat() < smallest:
                smallest = t.getTimerFloat()
                transition = t
        return transition
        

