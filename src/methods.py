import numpy as np
import math
import matplotlib.pyplot as plt
from queue import PriorityQueue
import time
import os

def print_solution(state1, number_nodes_expanded, goal_state, state2 = None): 
	"""When solution is found, this method is called to print the solution path
	
	Arguments:
		state1 {Node} -- The final node of the search, where the solution was found
		number_nodes_expanded {int} -- Total number of nodes expanded during search
		goal_state {Node} -- final layout of the board, used for Bidirectional search to find actual depth of solution 
	
	Keyword Arguments:
		state2 {Node} -- If the search used was Bidirectional search, it returns a second node, correspondent to the final
		node in the bottom-up search (default: {None})
	"""		

	#print("Expanded nodes: " + str(number_nodes_expanded))

	if state2 != None:
		total_depth = state1.depth + state2.depth
	else:
		total_depth = state1.depth
		#print("Solution found at depth: " + str(total_depth))

	#dimensions = int(math.sqrt(total_depth)) + 1

	#fig = plt.figure(figsize=[4 * 4, 4 * 4])

	#state1.print_path(fig, 3, state1.depth + 1)

	if state2 != None:
		#state2.parent.print_path_reserse(fig, 3, state1.depth + 2)
		depth = 0
		found = False
		while not(found):
			if state1.check_solution(goal_state):
				depth += state1.depth
				found = True
			else:
				depth += 1
				state1 = state1.parent

		state2 = state2.parent
		while not(found):
			if state2.check_solution(goal_state):
				depth += 1
				found = True
			else:
				depth += 1
				state2 = state2.parent
		#print("Solution found at depth: " + str(depth))
		return depth
	else:
		return None
	
	#plt.savefig('../Results/path.png')

def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def dfs(start_node, goal_state, limit = None, iterative = False, graphSearch = False, improved_descendants = False):
	"""This method runs depth-first tree search.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		limit {int} -- Limits the depth to which DFS goes. (default: {None})
		iterative {bool} -- When set to True, uses DFS as the search method in iterative deepening search (default: {False})
		graphSearch {bool} -- When set to True, does DFS graph search, where it doesn't expanded previously expanded noded (default: {False})
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
	
	Returns:
		{bool} -- if iterative argument is set to False, Returns True if it was able to find a solution, and False otherwise.
		{bool, int, int} - if iterative argument is set to True, returns True or False, 
		depending if it is able to find a solution or not, and number of nodes expanded and depth of solution
	"""	
	fringe = [start_node]
	number_nodes_expanded = 0

	t0 = time.time()

	memory_max = 0

	if graphSearch:
		visited_nodes = {} #hash_map
		visited_nodes[start_node.build_hash] = 0

	while len(fringe) > 0:
		node = fringe.pop()

		memory_max = max(memory_max, memory_usage_psutil())

		node.count = number_nodes_expanded + 1

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			if iterative:
				return False, number_nodes_expanded, 0, memory_max*1.049
			else:
				return False, number_nodes_expanded, 0, memory_max*1.049
		
		if node.check_solution(goal_state):
			x = print_solution(node, number_nodes_expanded, goal_state)
			if iterative:
				return True, number_nodes_expanded, node.depth, memory_max*1.049
			return True, number_nodes_expanded, node.depth, memory_max*1.049 


		number_nodes_expanded += 1
		if limit == None or node.depth < limit:
			child_nodes = node.descendants(improved_descendants)

			if graphSearch:
				for i in range(len(child_nodes)):
					node_hash = child_nodes[i].build_hash()
					node_depth = child_nodes[i].depth
					if node_hash not in visited_nodes or visited_nodes[node_hash] > node_depth: #can also add if it's found i at smaller depth. Grants solution every time
						fringe.append(child_nodes[i])
						visited_nodes[node_hash] = node_depth
			else:
				for i in range(len(child_nodes)):
					fringe.append(child_nodes[i])
	
	if iterative:
		return False, number_nodes_expanded, 0, memory_max*1.049
			
	return False, number_nodes_expanded, 0, memory_max*1.049


def bfs(start_node, goal_state, graphSearch = False, improved_descendants = False):
	"""This method runs breadth-first tree search.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		graphSearch {bool} -- When set to True, does BFS graph search, where it doesn't expanded previously expanded noded (default: {False})
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	fringe = [start_node]
	number_nodes_expanded = 0

	child_nodes = []

	if graphSearch:
		visited_nodes = set([start_node.build_hash()])

	t0 = time.time()
	memory_max = 0
	while len(fringe) > 0:		
		node = fringe.pop(0)

		node.count = number_nodes_expanded + 1

		memory_max = max(memory_max, memory_usage_psutil())

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, 0, memory_max*1.049

		if node.check_solution(goal_state):
			x = print_solution(node, number_nodes_expanded, goal_state)
			return True, number_nodes_expanded, node.depth, memory_max*1.049 

		number_nodes_expanded += 1
		child_nodes = node.descendants(improved_descendants)

		if graphSearch:
			for i in range(len(child_nodes)):
				if child_nodes[i].build_hash() not in visited_nodes:
					fringe.append(child_nodes[i])
					number_nodes_expanded += 1
					visited_nodes.add(child_nodes[i].build_hash())
		else:
			for i in range(len(child_nodes)):
				number_nodes_expanded += 1
				fringe.append(child_nodes[i])

	return False, number_nodes_expanded, 0, memory_max*1.049

def idfs(start_node, goal_state, improved_descendants = False):
	"""[summary]
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	number_nodes_expanded = 0
	t0 = time.time()
	memory_max = 0
	for lim in range(21): #from depth 0 to 20
		solution, number_nodes_expanded_iter, depth, mem = dfs(start_node, goal_state, lim, iterative= True, improved_descendants= improved_descendants)
		number_nodes_expanded += number_nodes_expanded_iter
		memory_max = max(mem, memory_max)
		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, 0, memory_max*1.049

		if solution:
			return True, number_nodes_expanded, depth, memory_max*1.049
		
	return False, number_nodes_expanded, 0, memory_max*1.049


def BidirectionalSearch(start_node, end_node, goal_state, improved_descendants = False):
	"""This method runs Bidirectional Search, with BFS search in each of the directions.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		end_node {Node} -- Goal Node, which is the node with the goal board layout, first on the bottom-up search.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	queue_down = [start_node]
	queue_up = [end_node]

	visited_nodes_down = set([])
	visited_nodes_up = set([])

	number_nodes_expanded = 0

	child_nodes_down = []
	child_nodes_up = []

	hash_value_down = {}
	hash_value_up = {}

	t0 = time.time()
	memory_max = 0

	while len(queue_down) > 0 or len(queue_up) > 0:
		top_expanded = False
		bottom_expanded = False

		memory_max = max(memory_max, memory_usage_psutil())

		if len(queue_down) > 0:
			node_down = queue_down.pop(0)
			bottom_expanded = True
			node_down.count = number_nodes_expanded + 1

		
		if len(queue_up) > 0:
			node_up = queue_up.pop(0)
			top_expanded = True
			if bottom_expanded:
				node_up.count = number_nodes_expanded + 2
			else:
				node_down.count = number_nodes_expanded + 1

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, 0, memory_max*1.049

		if bottom_expanded:
			node_down_hash = node_down.build_hash()

			if node_down_hash not in visited_nodes_down:
				visited_nodes_down.add(node_down_hash)
				hash_value_down[node_down_hash] = node_down

				child_nodes_down = node_down.descendants(improved_descendants)

				for i in range(len(child_nodes_down)):
					queue_down.append(child_nodes_down[i])
			else:
				child_nodes_down = []

		if top_expanded:
			node_up_hash = node_up.build_hash()
			if node_up_hash not in visited_nodes_up:
				visited_nodes_up.add(node_up_hash)
				hash_value_up[node_up_hash] = node_up

				child_nodes_up = node_up.descendants(improved_descendants)
			
				for i in range(len(child_nodes_up)):
					queue_up.append(child_nodes_up[i])
			else:
				child_nodes_up = []

		if bottom_expanded and top_expanded:
			number_nodes_expanded += 2
		else:
			number_nodes_expanded += 1

		if (bottom_expanded and (node_down_hash in visited_nodes_up)) or (top_expanded and (node_up_hash in visited_nodes_down)): #if the node was also visited on other search then a path was found
				if bottom_expanded and (node_down_hash in visited_nodes_up):
					depth_found = print_solution(node_down, number_nodes_expanded, goal_state, hash_value_up[node_down_hash])
				else:
					depth_found = print_solution(hash_value_down[node_up_hash], number_nodes_expanded, goal_state, node_up)
				
				return True, number_nodes_expanded, depth_found, memory_max*1.049
				
	return False, number_nodes_expanded, 0, memory_max*1.049

def Astar(start_node, goal_state, graphSearch = False, improved_descendants = False, improved_heuristic = False):
	"""Runs A-star tree search.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		graphSearch {bool} -- When set to True, does BFS graph search, where it doesn't expanded previously expanded noded (default: {False})
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
		improved_heuristic {bool} -- When set to True, uses the improved version of manhattan distance heuristic (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	prior_queue = PriorityQueue()
	prior_queue.put((start_node.heuristic_manhattan(goal_state, improved_heuristic), start_node)) #no need to had f, because depth is 0

	number_nodes_expanded = 0

	t0 = time.time()
	memory_max = 0

	if graphSearch:
			visited_nodes = set([start_node.build_hash()])

	while not prior_queue.empty():
		node_f, current_node = prior_queue.get()

		memory_max = max(memory_max, memory_usage_psutil())
			
		t1 = time.time()

		current_node.count = number_nodes_expanded + 1

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, 0, memory_max*1.049
		
		if current_node.check_solution(goal_state):
			print_solution(current_node, number_nodes_expanded, goal_state)
			return True, number_nodes_expanded, current_node.depth, memory_max*1.049 
		
		number_nodes_expanded += 1

		child_nodes = current_node.descendants(improved_descendants)

		if graphSearch:
			for child in child_nodes:
				if child.build_hash() not in visited_nodes:
					child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
					child_f = child_h + child.depth
					prior_queue.put((child_f, child))
					visited_nodes.add(child.build_hash())
		else:
			for child in child_nodes:
				child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
				child_f = child_h + child.depth
				prior_queue.put((child_f, child))

	return False, number_nodes_expanded, 0, memory_max*1.049

def Greedy(start_node, goal_state, improved_descendants = False, improved_heuristic = False):
	"""Runs Greedy tree search.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
		improved_heuristic {bool} -- When set to True, uses the improved version of manhattan distance heuristic (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	prior_queue = PriorityQueue()
	prior_queue.put((start_node.heuristic_manhattan(goal_state, improved_heuristic), start_node))

	number_nodes_expanded = 0

	t0 = time.time()
	memory_max = 0
	while not prior_queue.empty():
		node_f, current_node = prior_queue.get()
		
		current_node.count = number_nodes_expanded + 1

		memory_max = max(memory_max, memory_usage_psutil())

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, 0, memory_max*1.049
		
		if current_node.check_solution(goal_state):
			print_solution(current_node, number_nodes_expanded, goal_state)
			return True, number_nodes_expanded, current_node.depth, memory_max*1.049 

		number_nodes_expanded += 1
		
		child_nodes = current_node.descendants(improved_descendants)

		for child in child_nodes:
			child_f = child.heuristic_manhattan(goal_state, improved_heuristic)
			prior_queue.put((child_f, child))

	return False, number_nodes_expanded, 0, memory_max*1.049		
