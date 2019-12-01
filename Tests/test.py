import sys

sys.path.insert(1, '../src/')

import numpy as np
from node import Node
import methods
import sys
import main

from memory_profiler import memory_usage 

states = []
states.append([0,'A','C',0,0,0,0,0,0,0,1,0,'B',0,0,0]) #depth 20
states.append([0,'A','C',0,0,0,1,0,0,0,0,0,'B',0,0,0]) #depth 19
states.append([1,0,'A',0,0,0,'C',0,0,0,0,0,'B',0,0,0]) #depth 18
states.append([0,0,'A',0,0,0,'C',0,1,0,0,0,'B',0,0,0]) #depth 17
states.append([0,0,'A',0,0,0,'C',0,'B',0,0,0,1,0,0,0]) #depth 16
states.append([0,0,'A',0,0,0,'C',0,'B',0,0,0,0,0,0,1]) #depth 15
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
goal_state = [0,0,0,0,0,'A',0,0,0,'B',0,0,0,'C',0,1] #Agent position doesnt matter
goal_state2 = [0,0,'O',0,0,'A',0,'O',0,'B',0,0,0,'C',0,1] #Agent position doesnt matter

if __name__ == '__main__':
    searches = ["Bidirec", "DFS"]

    for search in searches:
        for depth in range(20):
            count_falses = 0
            print(search + " normal descedants at depth " + str(20-depth) + ": ")
            start_agent, end_agent = main.find_agent(states[depth], goal_state)
            start_node = Node(states[depth], start_agent, 0)
            if 20-depth > 14:
                end_node = Node(goal_state, end_agent, 0) #used for bidirectional search
            else:
                end_node = Node(goal_state2, end_agent, 0)
            
            expandedt = 0
            memoryt = 0
            count = 0
            for i in range(10):
                if search == "BFS":
                    if (20 - depth) > 11:
                        break
                    sol, expanded, memory, depthf = methods.bfs(start_node, goal_state)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "DFS 15":
                    if (20 - depth) > 15:
                        break
                    sol, expanded, memory, depthf = methods.dfs(start_node, goal_state, limit= 15)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "DFS 18":
                    if (20 - depth) > 14:
                        break
                    sol, expanded, memory, depthf = methods.dfs(start_node, goal_state, limit= 18)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "IDS":
                    if (20 - depth) > 15:
                        break
                    sol, expanded, memory, depthf = methods.idfs(start_node, goal_state)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "A*":
                    if (20 - depth) > 18:
                        break
                    sol, expanded, memory, depthf = methods.Astar(start_node, goal_state)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "Greedy":
                    if (20 - depth) > 4:
                        break
                    sol, expanded, memory, depthf = methods.Greedy(start_node, goal_state)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "Bidirec":
                    sol, expanded, memory, depthf = methods.BidirectionalSearch(start_node, end_node)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory
                elif search == "DFS":
                    sol, expanded, memory, depthf = methods.dfs(start_node, goal_state)
                    if sol:
                        count += 1
                        expandedt += expanded
                        memoryt += memory

            if count > 0:
                expandedt /= count
                memoryt /= count
                print("Average expanded = " + str(expandedt))
                print("Average memory = " + str(memoryt))



     
