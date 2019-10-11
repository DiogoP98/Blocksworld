import numpy as np
from node import Node
import methods

initial_state = [0,0,0,0,0,0,0,0,0,0,0,0,'A','B','C',1] #1 represents the agent
goal_state = [0,0,0,0,0,'A',0,0,0,'B',0,0,0,'C',0,1] #Agent position doesnt matter

def find_agent():
	start_agent = [None]*2
	end_agent = [None]*2
	for i in range(16):
		if initial_state[i] == 1:
			start_agent[0] = i%4
			start_agent[1] = round(i/4)-1
		
		if goal_state[i] == 1:
			end_agent[0] = i%4
			end_agent[1] = round(i/4)-1
	return start_agent, end_agent

def main():
	start_agent, end_agent = find_agent()
	start_node = Node(initial_state, start_agent, 0)
	end_node = Node(goal_state, end_agent, 0) #used for bidirectional search
	#sol = methods.dfs(start_node, goal_state, 10)
	#sol = methods.bfs(start_node, goal_state)
	sol = methods.bfs(start_node, goal_state, True)
	#sol = methods.idfs(start_node,goal_state)
	#sol = methods.BidirectionalSearch(start_node, end_node) #might need hash
	if not(sol):
		print("No solution")

if __name__ == '__main__':
	main()