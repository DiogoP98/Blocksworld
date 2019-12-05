#!/usr/bin/python3

from node import Node
import methods
import sys, argparse
import matplotlib.pyplot as plt
import psutil

#use oned list instead of matrix to optimize space
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

def find_agent(initial, goal):
	start_agent = [None]*2
	end_agent = [None]*2
	for i in range(16):
		if initial[i] == 1:
			start_agent[0] = i%4
			start_agent[1] = i // 4
		
		if goal[i] == 1:
			end_agent[0] = i%4
			end_agent[1] = i // 4
	return start_agent, end_agent

def main():
	sol = False

	parser = argparse.ArgumentParser(description='A tutorial of argparse!')
	parser.add_argument("--m", choices=["BFS", "DFS", "IDS", "Bidirectional", "Astar", "Greedy"], required=True, type=str, help="Method to use")
	parser.add_argument("--l", default=None, type=int, help="Depth limit for depth-first search")
	parser.add_argument("--g", choices=[True, False], default=False, type=bool, help="Whether or not to use graph search")
	parser.add_argument("--h", choices=[True, False], default=False, type=bool, help="Whether or not to use improved heuristic, for heuristic searches")
	parser.add_argument("--d", choices=[True, False], default=False, type=bool, help="Whether or not to use improved descendants function")
	parser.add_argument("--s", choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], default=None, type=int, help="Optimal depth of the solution wanted to test")

	args = parser.parse_args()

	method = args.m
	limit = args.l
	graph_search = args.g
	improved_heuristic = args.h
	improved_descendants = args.d
	depth = args.s
	
	if depth == None:
		start_agent, end_agent = find_agent(initial_states[10], goal_state)
		start_node = Node(initial_states[10], start_agent, 0)
		start_node.count = 1
		end_node = Node(goal_state2, end_agent, 0) #used for bidirectional search
	elif depth <= 14:
		start_agent, end_agent = find_agent(initial_states[depth-1], goal_state)
		start_node = Node(initial_states[depth-1], start_agent, 0)
		start_node.count = 1
		end_node = Node(goal_state2, end_agent, 0) #used for bidirectional search
	else:
		start_agent, end_agent = find_agent(initial_states[depth-1], goal_state)
		start_node = Node(initial_states[depth-1], start_agent, 0)
		start_node.count = 1
		end_node = Node(goal_state, end_agent, 0) #used for bidirectional search

	if method == "DFS":
		sol = methods.dfs(start_node, goal_state, limit = limit, iterative = False, graphSearch = graph_search, improved_descendants = improved_descendants)
	elif method == "BFS":
		sol = methods.bfs(start_node, goal_state, graphSearch = graph_search, improved_descendants = improved_descendants)
	elif method == "IDS":
		sol = methods.idfs(start_node,goal_state, improved_descendants = improved_descendants)
	elif method == "Bidirectional":
		sol = methods.BidirectionalSearch(start_node, end_node, goal_state2, improved_descendants = improved_descendants)
	elif method == "Astar":
		sol = methods.Astar(start_node, goal_state, graphSearch = graph_search, improved_descendants = improved_descendants, improved_heuristic = improved_heuristic)
	elif method == "Greedy":
		sol = methods.Greedy(start_node, goal_state, improved_descendants = improved_descendants, improved_heuristic = improved_heuristic)
	else:
		print("Invalid method")
	
	if not(sol):
		print("No solution")

if __name__ == '__main__':
	main()
