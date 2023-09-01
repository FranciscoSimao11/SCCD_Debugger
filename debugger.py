from State import *
from Transition import *
from ModelParser import *
from ModelExecuter import *
import sys

def main():
    f = open(sys.argv[1], "r")
    mp = ModelParser()
    states = mp.parseModel(f)
    for state in states:
        print state.getPrintableObject()
    nextAction = raw_input("Start_Simulation? (write yes or no)\n> ")
    if nextAction == "yes":
        print("Loading Model Executer...")
        me = ModelExecuter()
        me.executeModel(states)


if __name__ == '__main__':
    main()