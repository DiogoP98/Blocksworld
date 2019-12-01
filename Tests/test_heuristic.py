import sys

sys.path.insert(1, '../src/')

import numpy as np
from node import Node
import methods
import main

states = []
states.append(['A',0,'O',0,0,0,0,'O',0,'B','C',0,0,0,0,1]) #depth 15
states.append([0,0,'O',0,0,0,0,'O',0,0,0,0,'A','B','C',1]) #depth 14
states.append(['A',0,'O',0,0,0,0,'O',0,'B','C',0,0,0,0,1]) #depth 13
states.append(['A',0,'O',0,0,0,0,'O','B',0,0,0,0,0,'C',1]) #depth 12
states.append([0,'A','O',0,0,0,0,'O',0,'B','C',0,0,0,0,1]) #depth 11
states.append([0,0,'O',0,0,'A',0,'O',0,0,0,'B','C',0,0,1]) #depth 10
states.append([1,0,'O',0,0,0,'A','O','B',0,0,0,0,0,'C',0]) #depth 9
states.append([0,0,'O',0,0,'A',0,'O',0,'C',0,'B',0,0,0,1]) #depth 8
states.append([0,0,'O',0,0,0,'A','O','B',0,0,0,0,'C',0,1]) #depth 7
states.append([0,0,'O',0,0,0,'A','O',0,'B',0,0,'C',0,1,0]) #depth 6
states.append([0,0,'O',0,'A',0,0,'O',0,'B',0,0,0,'C',0,1]) #depth 5
states.append([0,0,'O',0,0,0,'A','O',0,'B',0,0,1,'C',0,0]) #depth 4
states.append([1,0,'O',0,0,0,'A','O',0,'B',0,0,0,'C',0,0]) #depth 3
states.append([0,0,'O',0,1,0,'A','O',0,'B',0,0,0,'C',0,0]) #depth 2
states.append([0,0,'O',0,0,1,'A','O',0,'B',0,0,0,'C',0,0]) #depth 1
goal_state = [0,0,'O',0,0,'A',0,'O',0,'B',0,0,0,'C',0,1] #Agent position doesnt matter

if __name__ == '__main__':
    #A*

    searches = ["A*", "Greedy"]
    for search in searches:
        for depth in range(15):
            count_falses = 0
            print(search + " misplaced normal descedants at depth " + str(15-depth) + ": ")
            start_agent, end_agent = main.find_agent(states[depth], goal_state)
            start_node = Node(states[depth], start_agent, 0)
            total_mem = 0
            for i in range(10):
                if search == "A*":
                    sol, memory = methods.Astar(start_node, goal_state)
                    total_mem += memory
                    print("")
                else:
                    if (15 - depth) > 4:
                        print("pass")
                        continue
                    sol, memory = methods.Greedy(start_node, goal_state)
                    total_mem += memory
                    if sol == False:
                        count_falses += 1
                    if count_falses == 1:
                        break
                    print("")
            total_mem /= 10
            print("Total memory = " + str(total_mem))


     
