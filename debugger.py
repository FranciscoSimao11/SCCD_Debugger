from State import *
from Transition import *
from ModelParser import *
from ModelExecuter import *
import sys
 
def main():
    f = open(sys.argv[1], "r")
    mp = ModelParser()
    classes, statecharts = mp.parseModel(f)
    
    #states, classes, initialStateId = mp.parseModel(f)
    
    for c in classes.values():
        print c.getPrintableObject()
    for statechart in statecharts.values():
        print statechart.getPrintableObject()
    
    for s in statecharts.values():
        nextAction = raw_input("Start_Simulation? (write yes or no)\n> ")
        if nextAction == "yes":
            print("Loading Model Executer...")
            me = ModelExecuter()
            me.executeModel(s.states, s.initialState)
        else:
            print("Exiting...")


if __name__ == '__main__':
    main()