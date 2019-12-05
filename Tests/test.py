import sys

sys.path.insert(1, '../src/')

import numpy as np
from node import Node
import methods
import main

initial_states = []
initial_states.insert(0, [0,'A','C',0,0,0,0,0,0,0,1,0,'B',0,0,0]) #depth 20
initial_states.insert(0, [0,'A','C',0,0,0,1,0,0,0,0,0,'B',0,0,0]) #depth 19
initial_states.insert(0, [1,0,'A',0,0,0,'C',0,0,0,0,0,'B',0,0,0]) #depth 18
initial_states.insert(0, [0,0,'A',0,0,0,'C',0,1,0,0,0,'B',0,0,0]) #depth 17
initial_states.insert(0, [0,0,'A',0,0,0,'C',0,'B',0,0,0,1,0,0,0]) #depth 16
initial_states.insert(0, [0,0,'A',0,0,0,'C',0,'B',0,0,0,0,0,0,1]) #depth 15
initial_states.insert(0, [0,0,'O',0,0,0,0,'O',0,0,0,0,'A','B','C',1]) #depth 14
initial_states.insert(0, ['A',0,'O',0,0,0,0,'O',0,'B','C',0,0,0,0,1]) #depth 13
initial_states.insert(0, [0,0,'O',0,0,'A','C','O','B',0,0,0,0,0,1,0]) #depth 12
initial_states.insert(0, [0,'A','O',0,0,0,0,'O',0,'B','C',0,0,0,0,1]) #depth 11
initial_states.insert(0, [0,0,'O',0,0,'A',0,'O',0,0,0,'B','C',0,0,1]) #depth 10
initial_states.insert(0, [1,0,'O',0,0,0,'A','O','B',0,0,0,0,0,'C',0]) #depth 9
initial_states.insert(0, [0,0,'O',0,0,'A',0,'O',0,'C',0,'B',0,0,0,1]) #depth 8
initial_states.insert(0, [0,0,'O',0,0,0,'A','O','B',0,0,0,0,'C',0,1]) #depth 7
initial_states.insert(0, [0,0,'O',0,0,0,'A','O',0,'B',0,0,'C',0,1,0]) #depth 6
initial_states.insert(0, [0,0,'O',0,'A',0,0,'O',0,'B',0,0,0,'C',0,1]) #depth 5
initial_states.insert(0, [0,0,'O',0,0,0,'A','O',0,'B',0,0,1,'C',0,0]) #depth 4
initial_states.insert(0, [1,0,'O',0,0,0,'A','O',0,'B',0,0,0,'C',0,0]) #depth 3
initial_states.insert(0, [0,0,'O',0,1,0,'A','O',0,'B',0,0,0,'C',0,0]) #depth 2
initial_states.insert(0, [0,0,'O',0,0,1,'A','O',0,'B',0,0,0,'C',0,0]) #depth 1
goal_state = [0,0,0,0,0,'A',0,0,0,'B',0,0,0,'C',0,1] #Use for depth bigger than 14
goal_state2 = [0,0,'O',0,0,'A',0,'O',0,'B',0,0,0,'C',0,1] #use for depth lower or equal to 14

if __name__ == '__main__':
    searches = ["BFS", "DFS", "IDS", "Bidirec", "A*", "Greedy"]
    graph = [True, False]
    heuristic = [True, False]
    limit = [None, 15, 18]

    for depth in range(len(initial_states)):
        print()
        print()
        print("Depth " + str(depth + 1))
        start_agent, end_agent = main.find_agent(initial_states[depth], goal_state)
        start_node = Node(initial_states[depth], start_agent, 0)
        start_node.count = 1
        if depth <= 13:
            end_node = Node(goal_state2, end_agent, 0) #used for bidirectional search
        else:
            end_node = Node(goal_state, end_agent, 0) #used for bidirectional search
        for search in searches:
            if search == "BFS":
                for value in graph:
                    print()
                    print(search + " with graph " + str(value))
                    expanded_total = 0
                    depth_total = 0
                    memory_total = 0
                    fail_total = 0
                    true_total = 0
                    for _ in range(10):
                        sol, expanded, depth_found, memory = methods.bfs(start_node, goal_state, graphSearch=value)
                        if sol:
                            true_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        else:
                            fail_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        if fail_total == 2:
                            break
                    print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                    print("Average depth: " + str(depth_total/(fail_total+true_total)))
                    print("Average memory: " + str(memory_total/(fail_total+true_total)))
                
                print()
                print(search + " with improved descendants")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.bfs(start_node, goal_state, improved_descendants=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))

            elif search == "DFS":
                for l in limit:
                    for value in graph:
                        print()
                        print(search + " with limit " + str(l) + " with graph " + str(value))
                        expanded_total = 0
                        depth_total = 0
                        memory_total = 0
                        fail_total = 0
                        true_total = 0
                        for _ in range(10):
                            sol, expanded, depth_found, memory = methods.dfs(start_node, goal_state, limit=l, graphSearch=value)
                            if sol:
                                true_total += 1
                                expanded_total += expanded
                                depth_total += depth_found
                                memory_total += memory
                            else:
                                fail_total += 1
                                expanded_total += expanded
                                depth_total += depth_found
                                memory_total += memory
                            if fail_total == 2:
                                break
                        print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                        print("Average depth: " + str(depth_total/(fail_total+true_total)))
                        print("Average memory: " + str(memory_total/(fail_total+true_total)))
                    
                    print()
                    print(search + " with limit " + str(l) + " with improved descendants ")
                    expanded_total = 0
                    depth_total = 0
                    memory_total = 0
                    fail_total = 0
                    true_total = 0
                    for _ in range(10):
                        sol, expanded, depth_found, memory = methods.dfs(start_node, goal_state, limit=l, improved_descendants=True)
                        if sol:
                            true_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        else:
                            fail_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        if fail_total == 2:
                            break
                        print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                        print("Average depth: " + str(depth_total/(fail_total+true_total)))
                        print("Average memory: " + str(memory_total/(fail_total+true_total)))

            elif search == "IDS":
                print()
                print(search)
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.idfs(start_node, goal_state)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))
                
                print()
                print(search + " with improved descendants")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.idfs(start_node, goal_state, improved_descendants=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))
            
            elif search == "Bidirec":
                print()
                print(search)
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    if depth <= 13:
                        sol, expanded, depth_found, memory = methods.BidirectionalSearch(start_node, end_node, goal_state2)
                    else:
                        sol, expanded, depth_found, memory = methods.BidirectionalSearch(start_node, end_node, goal_state)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))
                
                print()
                print(search + " with improved descendants")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    if depth <= 13:
                        sol, expanded, depth_found, memory = methods.BidirectionalSearch(start_node, end_node, goal_state2, improved_descendants=True)
                    else:
                        sol, expanded, depth_found, memory = methods.BidirectionalSearch(start_node, end_node, goal_state, improved_descendants=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))

            elif search == "A*":
                for value in graph:
                    print()
                    print(search + " with graph " + str(value))
                    expanded_total = 0
                    depth_total = 0
                    memory_total = 0
                    fail_total = 0
                    true_total = 0
                    for _ in range(10):
                        sol, expanded, depth_found, memory = methods.Astar(start_node, goal_state, graphSearch=value)
                        if sol:
                            true_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        else:
                            fail_total += 1
                            expanded_total += expanded
                            depth_total += depth_found
                            memory_total += memory
                        if fail_total == 2:
                            break
                    print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                    print("Average depth: " + str(depth_total/(fail_total+true_total)))
                    print("Average memory: " + str(memory_total/(fail_total+true_total)))
                
                print()
                print(search + " with improved descendants")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.Astar(start_node, goal_state, improved_descendants=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))

                print()
                print(search + " with improved heuristic")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.Astar(start_node, goal_state, improved_heuristic=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))
            
            elif search == "Greedy":
                print()
                print(search)
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.Greedy(start_node, goal_state)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))
                
                print()
                print(search + " with improved descendants")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.Greedy(start_node, goal_state, improved_descendants=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))

                print()
                print(search + " with improved heuristic")
                expanded_total = 0
                depth_total = 0
                memory_total = 0
                fail_total = 0
                true_total = 0
                for _ in range(10):
                    sol, expanded, depth_found, memory = methods.Greedy(start_node, goal_state, improved_heuristic=True)
                    if sol:
                        true_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    else:
                        fail_total += 1
                        expanded_total += expanded
                        depth_total += depth_found
                        memory_total += memory
                    if fail_total == 2:
                        break
                print("Average Nodes expanded: " + str(expanded_total/(fail_total+true_total)))
                print("Average depth: " + str(depth_total/(fail_total+true_total)))
                print("Average memory: " + str(memory_total/(fail_total+true_total)))

    


     
