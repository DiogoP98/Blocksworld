from node import Node
import methods
import sys

#use oned list instead of matrix to optimize space
initial_state_20 = ([0,'A','C',0,0,0,0,0,0,0,1,0,'B',0,0,0]) #depth 20
initial_state_19 = ([0,'A','C',0,0,0,1,0,0,0,0,0,'B',0,0,0]) #depth 19
initial_state_18 = ([1,0,'A',0,0,0,'C',0,0,0,0,0,'B',0,0,0]) #depth 18
initial_state_17 = ([0,0,'A',0,0,0,'C',0,1,0,0,0,'B',0,0,0]) #depth 17
initial_state_16 = ([0,0,'A',0,0,0,'C',0,'B',0,0,0,1,0,0,0]) #depth 16
initial_state_15 = ([0,0,'A',0,0,0,'C',0,'B',0,0,0,0,0,0,1]) #depth 15
initial_state_14 = [0,0,'O',0,0,0,0,'O',0,0,0,0,'A','B','C',1] #depth 14
initial_state_13 = ['A',0,'O',0,0,0,0,'O',0,'B','C',0,0,0,0,1] #depth 13
initial_state_12 = ['A',0,'O',0,0,0,0,'O','B',0,0,0,0,0,'C',1] #depth 12
initial_state_11 = [0,'A','O',0,0,0,0,'O',0,'B','C',0,0,0,0,1] #depth 11
initial_state_10 = [0,0,'O',0,0,0,'A','O',0,0,0,'B','C',0,0,1] #depth 10
initial_state_9 = [1,0,'O',0,0,0,'A','O','B',0,0,0,0,0,'C',0] #depth 9
initial_state_8 = [0,0,'O',0,0,'A',0,'O',0,'C',0,'B',0,0,0,1] #depth 8
initial_state_7 = [0,0,'O',0,0,0,'A','O','B',0,0,0,0,'C',0,1] #depth 7
initial_state_6 = [0,0,'O',0,0,0,'A','O',0,'B',0,0,'C',0,1,0] #depth 6
initial_state_5 = [0,0,'O',0,'A',0,0,'O',0,'B',0,0,0,'C',0,1] #depth 5
initial_state_4 = [0,0,'O',0,0,0,'A','O',0,'B',0,0,1,'C',0,0] #depth 4
initial_state_3 = [1,0,'O',0,0,0,'A','O',0,'B',0,0,0,'C',0,0] #depth 3
initial_state_2 = [0,0,'O',0,1,0,'A','O',0,'B',0,0,0,'C',0,0] #depth 2
initial_state_1 = [0,0,'O',0,0,1,'A','O',0,'B',0,0,0,'C',0,0] #depth 1
goal_state = [0,0,0,0,0,'A',0,0,0,'B',0,0,0,'C',0,1] #Agent position doesnt matter

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
	start_agent, end_agent = find_agent(initial_state_16, goal_state)
	start_node = Node(initial_state_16, start_agent, 0)
	start_node.count = 1
	end_node = Node(goal_state, end_agent, 0) #used for bidirectional search

	method = str(sys.argv[1])
	
	sol = False

	if method == "dfs":
		sol = methods.dfs(start_node, goal_state, limit= 18)
	elif method == "bfs":
		if str(sys.argv[2]) == "normal":
			print("Normal BFS: ")
			sol = methods.bfs(start_node, goal_state)
		else: 
			print("BFS graph search: ")
			sol = methods.bfs(start_node, goal_state, True)
	elif method == "idfs":
		sol = methods.idfs(start_node,goal_state)
	elif method == "bidirec":
		sol = methods.BidirectionalSearch(start_node, end_node) #might need hash
	elif method == "astar":
		if str(sys.argv[2]) == "normal":
			print("A*: ")
			sol = methods.Astar(start_node, goal_state, improved_heuristic= True)
		else: 
			print("A* graph search: ")
			sol = methods.Astar(start_node, goal_state, True)
	elif method == "greedy":
		sol = methods.Greedy(start_node, goal_state, improved_heuristic= True)
	else:
		print("Invalid method")
	
	if not(sol):
		print("No solution")

if __name__ == '__main__':
	main()
