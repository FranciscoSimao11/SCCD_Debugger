from __future__ import print_function
from State import *
from Transition import *
from ModelParser import *
from ModelExecuter import *
import sys
 
def main():
    f = open(sys.argv[1], "r")
    print("Parsing model...\n")
    mp = ModelParser()
    classes, statecharts, statesPerLevel, miscInfo = mp.parseModel(f)
    simulationModes = ["Real-Time Simulation", "Scaled Real-Time Simulation", "As-fast-as-Possible Simulation"]
    
    for c in classes.values():
        print (c.getPrintableObject())
        c.genFile()
    for statechart in statecharts.values():
        print (statechart.getPrintableObject())
    
    for s in statecharts.values():
        print("Possible Simulation Modes: ")
        counter = 1
        for sm in simulationModes:
            print(str(counter) + ". " + sm + "; ")
            counter += 1
        chosenMode = float(raw_input("\nChoose the number corresponding to the simulation mode you would like to execute.\n> "))
        
        if chosenMode == 1:
            scaleFactor = 1
        elif chosenMode == 2:
            scaleFactor = float(raw_input("Please select the scale factor. (write how faster it should be; e.g. 2 -> 2 times faster) \n> "))
        elif chosenMode == 3:
            scaleFactor = 0
            
        #debugMode = raw_input("Enable debug mode? (write yes or no)\n> ")
        nextAction = raw_input("Start_Simulation? (write yes or no)\n> ")
        if nextAction == "yes" or nextAction == "y" or nextAction == "":
            print("Loading Model Executer...")
            me = ModelExecuter()
            print("Scale Factor: {}".format(scaleFactor))
            me.executeModel(s.states, s.initialState, scaleFactor, statesPerLevel)
        else:
            print("Exiting...")


if __name__ == '__main__':
    main()