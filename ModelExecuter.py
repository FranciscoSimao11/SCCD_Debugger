# -*- coding: utf-8 -*-
from __future__ import print_function
from State import *
from Transition import *
from Timer import *
import sys, threading, multiprocessing
import Queue

sync_event = threading.Event()

class ModelExecuter():    

    def executeModel(self, states, initialStateId, scaleFactor):
        print("Started Execution")
        initialState = states[initialStateId]
        #finalState = states["state_B"]
        currState = initialState
        #nextState = None
        while True: #currState != finalState
            print("Current State: " + currState.name)
            
            entryScript = currState.entryScript
            if entryScript != None:
                print ("Exec entry script")

            timedTransitionToExecute, possibleTransitionsWithEvents = self.checkSmallestTimer(currState.transitions)
            
            if timedTransitionToExecute != None and len(possibleTransitionsWithEvents) < 1: #TIMED TRANSITIONS ONLY
                print("Timed Transition to be executed: " + timedTransitionToExecute.getPrintableObject())
                
                mode = 0
                transitionToExecute = timedTransitionToExecute
                self.handleSleepTime(transitionToExecute.after, scaleFactor, mode)
                nextState = states[transitionToExecute.target[3:]]
                
            elif timedTransitionToExecute == None and len(possibleTransitionsWithEvents) > 0: #EVENTS ONLY
                print("\rPossible events: ", end="")
                for e in possibleTransitionsWithEvents.values():
                    print(e.event + "; ")
                    
                mode = 0
                eventQueue = Queue.Queue()
                self.requestEventInput(eventQueue, possibleTransitionsWithEvents, mode)
                transitionToExecute = self.processEventReception(eventQueue, possibleTransitionsWithEvents)
                nextState = states[transitionToExecute.target[3:]]
                
            elif timedTransitionToExecute != None and len(possibleTransitionsWithEvents) > 0: #TIMED TRANSITIONS AND EVENTS
                print("\rPossible events: ", end="")
                for e in possibleTransitionsWithEvents.values():
                    print(e.event + "; ")
                
                print("Timed Transition to be executed: " + timedTransitionToExecute.getPrintableObject())
                
                sleepTime = timedTransitionToExecute.after
                eventQueue = Queue.Queue()
                mode = 1
                transitionToExecute = self.threadsSetup(sleepTime, eventQueue, mode, scaleFactor)    
                nextState = states[transitionToExecute.target[3:]]

            else:
                print("Whoops, we've reached a dead end.")
            
            exitScript = currState.exitScript
            
            if exitScript != None:
                print ("Exec exit script")
                
            transitionScript = transitionToExecute.script
            if transitionScript != None:
                print ("Exec transition script")
            
            currState = nextState    
        
        print("Finished Execution in state: " + currState.name)
        return states
        

    def threadsSetup(self, sleepTime, eventQueue, scaleFactor, mode):
        thread1 = threading.Thread(target = self.handleSleepTime, args=(sleepTime, scaleFactor, mode, ))
        thread2 = threading.Thread(target = self.requestEventInput, args=(eventQueue, possibleTransitionsWithEvents, mode, ))
        
        thread1.start()
        thread2.start()
                
        time.sleep(1)  # Sleep for 1 second to ensure both threads have started
        sync_event.set()  # Set the synchronization event to release both threads
        
        # Wait for both threads to finish
        thread1.join()
        #thread2.join()
        print("Both finished")
        
        if not eventQueue.empty():
            transitionToExecute = self.processEventReception(eventQueue, possibleTransitionsWithEvents)
        else:
            print("No event received")
            transitionToExecute = timedTransitionToExecute
        return transitionToExecute

    def processEventReception(self, eventQueue, possibleTransitionsWithEvents):
        eventReceived = eventQueue.get()
        print("Received event " + eventReceived)
        transitionToExecute = possibleTransitionsWithEvents[eventReceived]
        print("Event Based Transition to be executed: " + transitionToExecute.getPrintableObject())
        return transitionToExecute

    # mode 0 - just sleep; mode 1 - concurrent sleep and input
    def handleSleepTime(self, sleepTime, scaleFactor, mode):
        if mode == 1:
            sync_event.wait()
        if scaleFactor == 0:
            sleepTime = 0
        else:
            sleepTime = sleepTime/scaleFactor
        print("Sleeping for {} seconds.".format(sleepTime))
        timer = Timer()
        timer.start()
        time.sleep(sleepTime)
        timer.stop() #isto so pode executar se a cena acabar

    # mode 0 - just input; mode 1 - concurrent sleep and input
    def requestEventInput(self, eventQueue, possibleTransitionsWithEvents, mode):
        if mode == 1:
            sync_event.wait()
        #while eventQueue.empty():  
        eventReceived = raw_input("> ")
        if eventReceived in possibleTransitionsWithEvents:
                eventQueue.put(eventReceived)

    def checkSmallestTimer(self, transitions):
        smallest = sys.float_info.max #this can never be the sleep time as it causes an overflow error
        possibleTransitionsWithEvents = {}
        smallestTimerTransition = None
        for t in transitions:
            if t.after < smallest and t.after > -1:
                smallest = t.after
                smallestTimerTransition = t
            elif t.after == -1:
                possibleTransitionsWithEvents[t.event] = t
        return (smallestTimerTransition, possibleTransitionsWithEvents)
        

