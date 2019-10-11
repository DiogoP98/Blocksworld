import numpy as np

def print_solution(state1, number_nodes_visited, state2 = None): #state2 only used for bidirectional
	print("Nodes visited ", number_nodes_visited)

	if state2 != None:
		print("Solution found at depth  ", state1.depth + state2.depth)
	else:
		print("Solution found at depth  ", state1.depth)

	state1.print_path()

	if state2 != None:
		state2.parent.print_path_reserse()

def dfs(start_node, goal_state, limit):
	stack = [start_node]
	number_nodes_visited = 0

	while len(stack) != 0:
		state = stack.pop()
		number_nodes_visited += 1

		if state.check_solution(goal_state):
			print_solution(state, number_nodes_visited)
			return True

		if(state.depth < limit):
			child_nodes = state.descendants()
			for i in range(len(child_nodes)):
				stack.append(child_nodes[i])

	return False

def bfs(start_node, goal_state, graphSearch = False):
	queue = [start_node]
	number_nodes_visited = 0

	if graphSearch:
		visited_nodes = set([])

	while len(queue) != 0:
		state = queue.pop(0)
		number_nodes_visited += 1

		if state.check_solution(goal_state):
			print_solution(state, number_nodes_visited)
			return True

		if graphSearch:
			state_hash = state.build_hash()
			if state_hash not in visited_nodes:
				visited_nodes.add(state_hash)
				child_nodes = state.descendants()
			else:
				child_nodes = []
		else:
			child_nodes = state.descendants()
		
		for i in range(len(child_nodes)):
			queue.append(child_nodes[i])

	return False

def idfs(start_node, goal_state):
	for lim in range(1,20):
		if dfs(start_node, goal_state, lim):
			return True
		print("Not found for depth ", lim)
	return False

def BidirectionalSearch(start_node, end_node):
	queue_down = [start_node]
	queue_up = [end_node]

	visited_nodes_down = set([])
	visited_nodes_up = set([])

	number_nodes_visited = 0

	hash_value_down = {}
	hash_value_up = {}

	while len(queue_down) != 0 and len(queue_up) != 0:
		state_down = queue_down.pop(0)
		state_up = queue_up.pop(0)

		number_nodes_visited += 2

		state_down_hash = state_down.build_hash()
		state_up_hash = state_up.build_hash()

		if state_down_hash not in visited_nodes_down:
			visited_nodes_down.add(state_down_hash)
			hash_value_down[state_down_hash] = state_down

			child_nodes_down = state_down.descendants()
			for i in range(len(child_nodes_down)):
				queue_down.append(child_nodes_down[i])
		else:
			child_nodes_down = []

		if state_up_hash not in visited_nodes_up:
			visited_nodes_up.add(state_up_hash)
			hash_value_up[state_up_hash] = state_up

			child_nodes_up = state_up.descendants()
			for i in range(len(child_nodes_up)):
				queue_up.append(child_nodes_up[i])
		else:
			child_nodes_up = []

		if state_down_hash in visited_nodes_up: #if the node was also visited from the search up then a path was found
				print_solution(state_down, number_nodes_visited, hash_value_up[state_down_hash])
				return True

	return False

def Astar():
	return False		