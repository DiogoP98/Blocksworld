import numpy as np
import time, sys 
import math
import matplotlib.pyplot as plt
from queue import PriorityQueue

sys.setrecursionlimit(9000)

def print_solution(state1, number_nodes_expanded, goal_state, state2 = None): 
	"""When solution is found, this method is called to print the solution path
	
	Arguments:
		state1 {Node} -- The final node of the search, where the solution was found
		number_nodes_expanded {int} -- Total number of nodes expanded during search
		goal_state {Node} -- final layout of the board, used for Bidirectional search to find actual depth of solution 
	
	Keyword Arguments:
		state2 {Node} -- If the search used was Bidirectional search, it gives a second node, correspondent to the final
		node in the bottom-up search (default: {None})

	Returns:
		{int} -- In case the search was Bidirectional, it calculates the actual depth of the solution.
	"""

	if state2 != None:
		total_depth = state1.depth + state2.depth
	else:
		total_depth = state1.depth
		print("Solution found at depth: " + str(total_depth))

	dimensions = int(math.sqrt(total_depth)) + 1

	fig = plt.figure(figsize=[4 * dimensions, 4 * dimensions])

	state1.print_path(fig, dimensions, state1.depth + 1)

	if state2 != None:
		state2.parent.print_path_reserse(fig, dimensions, state1.depth + 2)
		middle_depth = state1.depth
		found = False
		while True:
			if state1.check_solution(goal_state):
				middle_depth = state1.depth
				found = True
				#check if the solution can still be find in previous nodes
				state1 = state1.parent
			else:
				if state1.parent == None:
					break
				else:
					state1 = state1.parent

		state2 = state2.parent
		while not(found):
			if state2.check_solution(goal_state):
				middle_depth += 1
				found = True
			else:
				middle_depth += 1
				state2 = state2.parent
		
		print("Solution found at depth: " + str(middle_depth))
		plt.show()
		return middle_depth
	else:
		plt.show()
		return None

def bfs(start_node, goal_state, graphSearch = False, improved_descendants = False):
	"""Runs breadth-first search.
	
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
	number_nodes_visited = 1

	child_nodes = []

	if graphSearch:
		closed = set()

	t0 = time.time()
	while len(fringe) > 0:		
		node = fringe.pop(0)
		node.count = number_nodes_visited
		number_nodes_visited += 1

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False

		if node.check_solution(goal_state):
			print("Expanded nodes: " + str(number_nodes_expanded))
			_ = print_solution(node, number_nodes_expanded, goal_state)
			return True 

		if graphSearch:
			if node.build_hash() not in closed:
				closed.add(node.build_hash())
				number_nodes_expanded += 1
				child_nodes = node.successors(improved_descendants)
				for i in range(len(child_nodes)):
					fringe.append(child_nodes[i])
					
		else:
			number_nodes_expanded += 1
			child_nodes = node.successors(improved_descendants)
			for i in range(len(child_nodes)):
				fringe.append(child_nodes[i])

	return False

def dfs(start_node, goal_state, limit = None, iterative = False, graphSearch = False, improved_descendants = False):
	"""Runs depth-first tree search.
	
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
	number_nodes_visited = 0

	t0 = time.time()

	if graphSearch:
		closed = {} #hash_map

	while len(fringe) > 0:
		number_nodes_visited += 1
		node = fringe.pop()
		node.count = number_nodes_visited

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			if iterative:
				return False
			else:
				return False
		
		if node.check_solution(goal_state):
			_ = print_solution(node, number_nodes_expanded, goal_state)
			if iterative:
				return True, number_nodes_visited
			print("Expanded nodes: " + str(number_nodes_expanded))
			return True 


		if limit == None or node.depth < limit:
			if graphSearch:
				node_hash = node.build_hash()
				node_depth = node.depth
				#can also add if it's found i at smaller depth. Grants solution every time
				if node_hash not in closed or closed[node_hash] > node_depth:
					closed[node_hash] = node_depth
					number_nodes_expanded += 1
					child_nodes = node.successors(improved_descendants)
					for i in range(len(child_nodes)):
						fringe.append(child_nodes[i])
			else:
				number_nodes_expanded += 1
				child_nodes = node.successors(improved_descendants)
				for i in range(len(child_nodes)):
					fringe.append(child_nodes[i])
	
	if iterative:
		return False, number_nodes_visited
			
	return False

def idfs(start_node, goal_state, improved_descendants = False):
	"""Runs iterative-deepening depth-first search.
	
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

	for lim in range(21): #from depth 0 to 20
		solution, number_nodes_expanded_iter = dfs(start_node, goal_state,  lim, iterative= True, improved_descendants= improved_descendants)
		number_nodes_expanded += number_nodes_expanded_iter

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False

		if solution:
			print("Expanded nodes: " + str(number_nodes_expanded))
			return True
		
	return False


def BidirectionalSearch(start_node, end_node, goal_state, improved_descendants = False):
	"""Runs Bidirectional Search, with BFS search in each of the directions.
	
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

	visited_nodes_down = set()
	visited_nodes_up = set()

	number_nodes_expanded = 0
	number_nodes_visited = 0

	child_nodes_down = []
	child_nodes_up = []

	hash_value_down = {}
	hash_value_up = {}

	t0 = time.time()
	
	while len(queue_down) > 0 or len(queue_up) > 0:
		top_expanded = False
		bottom_expanded = False

		#if the search down still has nodes to expand
		if len(queue_down) > 0:
			node_down = queue_down.pop(0)
			bottom_expanded = True
			number_nodes_visited += 1
			node_down.count = number_nodes_visited
		
		#if the search up still has nodes to expand
		if len(queue_up) > 0:
			node_up = queue_up.pop(0)
			top_expanded = True
			number_nodes_visited += 1
			node_up.count = number_nodes_visited

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False

		if bottom_expanded:
			node_down_hash = node_down.build_hash()

			if node_down_hash not in visited_nodes_down:
				number_nodes_expanded += 1
				visited_nodes_down.add(node_down_hash)
				hash_value_down[node_down_hash] = node_down
				child_nodes_down = node_down.successors(improved_descendants)

				for i in range(len(child_nodes_down)):
					queue_down.append(child_nodes_down[i])
			else:
				child_nodes_down = []

		if top_expanded:
			node_up_hash = node_up.build_hash()
			if node_up_hash not in visited_nodes_up:
				visited_nodes_up.add(node_up_hash)
				hash_value_up[node_up_hash] = node_up

				number_nodes_expanded += 1
				child_nodes_up = node_up.successors(improved_descendants)
			
				for i in range(len(child_nodes_up)):
					queue_up.append(child_nodes_up[i])
			else:
				child_nodes_up = []

		#The node expanded on the search down was already expanded in the search up or vice-versa
		if bottom_expanded and (node_down_hash in visited_nodes_up):
			print("Expanded nodes: " + str(number_nodes_expanded))
			depth_found = print_solution(node_down, number_nodes_expanded, goal_state, hash_value_up[node_down_hash])
			return True
		elif top_expanded and (node_up_hash in visited_nodes_down):
			print("Expanded nodes: " + str(number_nodes_expanded))
			depth_found = print_solution(hash_value_down[node_up_hash], number_nodes_expanded, goal_state, node_up)
			return True
				
	return False

def Astar(start_node, goal_state, graphSearch = False, improved_descendants = False, improved_heuristic = False):
	"""Runs A* tree search.
	
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
	prior_queue.put((start_node.heuristic_manhattan(goal_state, improved_heuristic), start_node))

	number_nodes_expanded = 0
	number_nodes_visited = 0

	t0 = time.time()

	if graphSearch:
			closed = set()

	while not prior_queue.empty():
		_, node = prior_queue.get()			
		number_nodes_visited += 1
		node.count = number_nodes_visited

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False
		
		if node.check_solution(goal_state):
			print("Expanded nodes: " + str(number_nodes_expanded))
			_ = print_solution(node, number_nodes_expanded, goal_state)
			return True 

		if graphSearch:
			if node.build_hash() not in closed:
				closed.add(node.build_hash())
				number_nodes_expanded += 1
				child_nodes = node.successors(improved_descendants)
				for child in child_nodes:
					child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
					child_f = child_h + child.depth
					prior_queue.put((child_f, child))
		else:
			number_nodes_expanded += 1
			child_nodes = node.successors(improved_descendants)
			for child in child_nodes:
				child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
				child_f = child_h + child.depth
				prior_queue.put((child_f, child))

	return False

def DFSAstar(start_node, goal_state, threshold, improved_descendants = False, improved_heuristic = False):
	"""Runs the different depth-first searches for IDA*.
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
		threshold {int} -- Threshold for the search. Nodes with bigger heuristic value that this are cut-off.
	
	Keyword Arguments:
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
		improved_heuristic {bool} -- When set to True, uses the improved version of manhattan distance heuristic (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
		{int} -- Number of nodes expanded in the depth-first search
	"""	
	fringe = [start_node]
	number_nodes_expanded = 0
	number_nodes_visited = 0
	child_nodes = []
	
	t0 = time.time()
	new_threshold = sys.maxsize

	while len(fringe) > 0:
		node = fringe.pop()
		number_nodes_visited += 1
		node.count = number_nodes_visited

		t1 = time.time()
		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False, number_nodes_expanded, new_threshold

		if node.check_solution(goal_state):
			_ = print_solution(node, number_nodes_expanded, goal_state)
			return True, number_nodes_expanded, new_threshold 

		child_nodes = node.successors(improved_descendants)
		number_nodes_expanded += 1

		for child in child_nodes:
			child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
			child_f = child_h + child.depth

			if child_f <= threshold:
				fringe.append(child)
			else:
				new_threshold = min(new_threshold, child_f)

	return False, number_nodes_expanded, new_threshold

def IDAstar(start_node, goal_state, improved_descendants = False, improved_heuristic = False):
	"""Runs Iterative-deppening A* .
	
	Arguments:
		start_node {Node} -- Start node, which describes where the search starts.
		goal_state {list} -- Goal state, which represents the final layout of the board.
	
	Keyword Arguments:
		improved_descendants {bool} -- When set to True, uses the improved version of descendants function (default: {False})
		improved_heuristic {bool} -- When set to True, uses the improved version of manhattan distance heuristic (default: {False})
	
	Returns:
		{bool} -- Returns True if it was able to find a solution, and False otherwise.
	"""	
	threshold = start_node.heuristic_manhattan(goal_state, improved_heuristic)
	number_nodes_expanded = 0
	t0 = time.time()

	while True:
		sol, number_nodes, new_treshold = DFSAstar(start_node, goal_state, threshold, improved_descendants, improved_heuristic)
		number_nodes_expanded += number_nodes
		t1 = time.time()

		if (t1 - t0) > 900:
			print("Took more than 15 minutes")
			return False
		
		if new_treshold == sys.maxsize:
			return False
		
		if sol:
			print("Number of nodes: " + str(number_nodes_expanded))
			return True
		else:
			threshold = new_treshold
	
	return False

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
	number_nodes_visited = 0

	t0 = time.time()

	while not prior_queue.empty():
		_, node = prior_queue.get()
		number_nodes_visited += 1
		node.count = number_nodes_visited

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			return False
		
		if node.check_solution(goal_state):
			print("Expanded nodes: " + str(number_nodes_expanded))
			_ = print_solution(node, number_nodes_expanded, goal_state)
			return True 

		number_nodes_expanded += 1
		
		child_nodes = node.successors(improved_descendants)

		for child in child_nodes:
			child_f = child.heuristic_manhattan(goal_state, improved_heuristic)
			prior_queue.put((child_f, child))

	return False		
