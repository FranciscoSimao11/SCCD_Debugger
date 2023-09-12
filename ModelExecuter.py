# -*- coding: utf-8 -*-
from State import *
from Transition import *
from Timer import *
import sys, threading, multiprocessing
import Queue

class ModelExecuter():

    def executeModel(self, states, initialStateId):
        print("Started Execution")
        initialState = states[initialStateId]
        #finalState = states["state_B"]
        currState = initialState
        while True: #currState != finalState
            #print("Current State: " + currState.name)

            transitionToExecute, possibleTransitionsWithEvents = self.checkSmallestTimer(currState.transitions)
            
            if transitionToExecute != None and len(possibleTransitionsWithEvents) < 1: #TIMED TRANSITIONS ONLY
                print("Timed Transition to be executed: " + transitionToExecute.getPrintableObject())
                self.handleSleepTime(transitionToExecute.after)
                currState = states[transitionToExecute.target[3:]]
                
            elif transitionToExecute == None and len(possibleTransitionsWithEvents) > 0: #EVENTS ONLY
                print("Possible events: ")
                for e in possibleTransitionsWithEvents.values():
                    print(e.event + "; ")
                user_input_queue = Queue.Queue()
                receivedEvent = self.requestEventInput(user_input_queue, possibleTransitionsWithEvents)
                print("Received event " + receivedEvent)
                currState = states[possibleTransitionsWithEvents[receivedEvent].target[3:]]
                
            elif transitionToExecute != None and len(possibleTransitionsWithEvents) > 0: #TIMED TRANSITIONS AND EVENTS
                #
                print("Timed Transition to be executed: " + transitionToExecute.getPrintableObject())
                print("Possible events: ")
                for e in possibleTransitionsWithEvents.values():
                    print(e.event + "; ")
                    
                user_input_queue = Queue.Queue()
                
                # Create events to track completion and termination of threads
                completion_event = threading.Event()
                terminate_event = multiprocessing.Event()

                input_thread = threading.Thread(target=self.eventInputThread, args=(user_input_queue, possibleTransitionsWithEvents, completion_event, terminate_event))
                sleep_thread = threading.Thread(target=self.sleepThread, args=(transitionToExecute.after, completion_event, terminate_event))
                
                input_thread.start()
                sleep_thread.start()

                completion_event.wait()

                # Check if the other thread needs to be forcibly terminated
                if not terminate_event.is_set():
                    terminate_event.set()  # Terminate the other thread

                if not user_input_queue.empty():
                    user_input = user_input_queue.get()

                currState = transitionToExecute.target #CHANGE
            #else:
                #print("Whoops, we've reached a dead end.")
        print("Finished Execution in state: " + currState.name)
        return states


    def sleepThread(self, sleepTime, completion_event, termination_event):
        self.handleSleepTime(sleepTime)
        completion_event.set() # Signal that this thread is done
        if not completion_event.is_set():
            terminate_event.set()

    def handleSleepTime(self, sleepTime):
        timer = Timer()
        timer.start()
        time.sleep(sleepTime)
        timer.stop() #isto so pode executar se a cena acabar

    def eventInputThread(self, eventQueue, possibleTransitionsWithEvents, completion_event, termination_event):
        self.requestEventInput(user_input_queue, possibleTransitionsWithEvents)
        completion_event.set() # Signal that this thread is done
        if not completion_event.is_set():
            terminate_event.set()
        print ("\n")

    def requestEventInput(self, eventQueue, possibleTransitionsWithEvents):
        while eventQueue.empty():
            eventReceived = raw_input("> ")
            if eventReceived in possibleTransitionsWithEvents:
                eventQueue.put(eventReceived)
        return eventQueue.get()

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
        

