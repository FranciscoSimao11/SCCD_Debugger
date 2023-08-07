from State import *
from Transition import *
from ModelParser import *

def main():
    f = open("counter.xml", "r")
    mp = ModelParser()
    states = mp.parseModel(f)
    for state in states:
        print state.getPrintableObject()



if __name__ == '__main__':
    main()