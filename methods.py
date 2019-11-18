import numpy as np
import math
import matplotlib.pyplot as plt
from queue import PriorityQueue
import time
import os

def print_solution(state1, number_nodes_visited, state2 = None): #state2 only used for bidirectional
	print("Nodes visited ", number_nodes_visited)

	if state2 != None:
		total_depth = state1.depth + state2.depth
		print("Solution found at depth  ", total_depth)
	else:
		total_depth = state1.depth
		print("Solution found at depth  ", total_depth)

	dimensions = int(math.sqrt(total_depth)) + 1

	fig = plt.figure(figsize=[4 * dimensions, 4 * dimensions])

	state1.print_path(fig, dimensions, 1)

	if state2 != None:
		state2.parent.print_path_reserse(fig, dimensions, state1.depth + 2)
	
	plt.savefig('path.png')

def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem

def dfs(start_node, goal_state, limit = None, iterative = False, graphSearch = False, improved_descendants = False):
	fringe = [start_node]
	number_nodes_visited = 0
	number_nodes_expanded = 0

	t0 = time.time()

	if graphSearch:
		visited_nodes = set([start_node.build_hash()])

	total = 0
	while len(fringe) > 0:
		mem = memory_usage_psutil()
		total += mem
		node = fringe.pop()
		number_nodes_visited += 1

		node.count = number_nodes_visited

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			if iterative:
				return False, number_nodes_expanded, number_nodes_visited, 0
			else:
				return False
		
		if node.check_solution(goal_state):
			#print_solution(node, number_nodes_visited)
			if iterative:
				return True, number_nodes_expanded, number_nodes_visited, node.depth, total

			print("Total memory usage: " + str(total*1.049))
			# print("Expanded nodes: " + str(number_nodes_expanded))
			# print("Visited nodes: " + str(number_nodes_visited))
			# print("Found solution at depth: " + str(node.depth))
			return True

		if limit == None or node.depth < limit:
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
	
	if iterative:
		return False, number_nodes_expanded, number_nodes_visited, 0, total
			
	return False

def bfs(start_node, goal_state, graphSearch = False, improved_descendants = False):
	fringe = [start_node]
	number_nodes_visited = 0
	number_nodes_expanded = 0

	child_nodes = []

	if graphSearch:
		visited_nodes = set([start_node.build_hash()])

	t0 = time.time()
	total = 0
	while len(fringe) > 0:
		mem = memory_usage_psutil()
		total += mem

		node = fringe.pop(0)
		number_nodes_visited += 1

		node.count = number_nodes_visited

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			return False

		if node.check_solution(goal_state):
			#print_solution(node, number_nodes_visited)
			print("Total memory usage: " + str(total*1.049))
			# print("Expanded nodes: " + str(number_nodes_expanded))
			# print("Visited nodes: " + str(number_nodes_visited))
			# print("Found solution at depth: " + str(node.depth))
			return True

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

	return False

def idfs(start_node, goal_state, improved_descendants = False):
	number_nodes_expanded = 0
	number_nodes_visited = 0

	t0 = time.time()

	total_mem = 0
	for lim in range(21): #from depth 0 to 20
		solution, number_nodes_expanded_iter, number_nodes_visited_iter, depth, mem = dfs(start_node, goal_state, lim, True, improved_descendants)
		number_nodes_expanded += number_nodes_expanded_iter
		number_nodes_visited += number_nodes_visited_iter
		total_mem += mem
		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			return False

		if solution:
			print("Total memory usage: " + str(total_mem*1.049))
			# print("Expanded nodes: " + str(number_nodes_expanded))
			# print("Visited nodes: " + str(number_nodes_visited))
			# print("Found solution at depth: " + str(depth))
			return True
		
	return False

def BidirectionalSearch(start_node, end_node, improved_descendants = False):
	queue_down = [start_node]
	queue_up = [end_node]

	visited_nodes_down = set([])
	visited_nodes_up = set([])

	number_nodes_visited = 0
	number_nodes_expanded = 0

	child_nodes_down = []
	child_nodes_up = []

	hash_value_down = {}
	hash_value_up = {}

	t0 = time.time()

	total = 0

	while len(queue_down) > 0 and len(queue_up) > 0:
		mem = memory_usage_psutil()
		total += mem

		node_down = queue_down.pop(0)
		node_up = queue_up.pop(0)

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			return False

		number_nodes_visited += 2

		node_down.count = number_nodes_visited - 1
		node_up.count = number_nodes_visited

		node_down_hash = node_down.build_hash()
		node_up_hash = node_up.build_hash()

		if node_down_hash not in visited_nodes_down:
			visited_nodes_down.add(node_down_hash)
			hash_value_down[node_down_hash] = node_down

			child_nodes_down = node_down.descendants(improved_descendants)

			for i in range(len(child_nodes_down)):
				number_nodes_expanded += 1
				queue_down.append(child_nodes_down[i])
		else:
			child_nodes_down = []

		if node_up_hash not in visited_nodes_up:
			visited_nodes_up.add(node_up_hash)
			hash_value_up[node_up_hash] = node_up

			child_nodes_up = node_up.descendants(improved_descendants)
			
			for i in range(len(child_nodes_up)):
				number_nodes_expanded += 1
				queue_up.append(child_nodes_up[i])
		else:
			child_nodes_up = []

		if node_down_hash in visited_nodes_up: #if the node was also visited from the search up then a path was found
				#print_solution(node_down, number_nodes_visited, hash_value_up[node_down_hash])
				print("Total memory usage: " + str(total*1.049))
				print("Expanded nodes: " + str(number_nodes_expanded))
				print("Visited nodes: " + str(number_nodes_visited))
				print("Found solution at depth: " + str(node_down.depth + hash_value_up[node_down_hash].depth))
				return True

	return False

def Astar(start_node, goal_state, graphSearch = False, improved_descendants = False, improved_heuristic = False):
	prior_queue = PriorityQueue()
	prior_queue.put((start_node.heuristic_manhattan(goal_state, improved_heuristic), start_node)) #no need to had f, because depth is 0

	number_nodes_visited = 0
	number_nodes_expanded = 0

	t0 = time.time()

	if graphSearch:
			visited_nodes = set([start_node.build_hash()])

	total = 0
	while not prior_queue.empty():
		mem = memory_usage_psutil()
		total += mem
		node_f, current_node = prior_queue.get()
		number_nodes_visited += 1
			
		t1 = time.time()

		current_node.count = number_nodes_visited

		if (t1 - t0) > 900:
			print("It took more than 15 min")
			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			return False

		current_node.count = number_nodes_visited
		
		if current_node.check_solution(goal_state):
			#print_solution(current_node, number_nodes_visited)
			#print("Total memory usage: " + str(total*1.049))
			print("Expanded nodes: " + str(number_nodes_expanded))
			#print("Visited nodes: " + str(number_nodes_visited))
			#print("Found solution at depth: " + str(current_node.depth))
			return True
		
		
		child_nodes = current_node.descendants(improved_descendants)

		if graphSearch:
			for child in child_nodes:
				if child.build_hash() not in visited_nodes:
					child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
					child_f = child_h + child.depth
					number_nodes_expanded += 1
					prior_queue.put((child_f, child))
					visited_nodes.add(child.build_hash())
		else:
			for child in child_nodes:
				child_h = child.heuristic_manhattan(goal_state, improved_heuristic)
				child_f = child_h + child.depth
				number_nodes_expanded += 1
				prior_queue.put((child_f, child))

	return False

def Greedy(start_node, goal_state, improved_descendants = False, improved_heuristic = False):
	prior_queue = PriorityQueue()
	prior_queue.put((start_node.heuristic_manhattan(goal_state, improved_heuristic), start_node))

	number_nodes_visited = 0
	number_nodes_expanded = 0

	t0 = time.time()

	total = 0
	while not prior_queue.empty():
		mem = memory_usage_psutil()
		total += mem

		node_f, current_node = prior_queue.get()
		number_nodes_visited += 1
		
		current_node.count = number_nodes_visited

		t1 = time.time()

		if (t1 - t0) > 900:
			print("It took more than 15 min")

			print("Expanded nodes: " + str(number_nodes_expanded))
			print("Visited nodes: " + str(number_nodes_visited))
			return False
		
		current_node.count = number_nodes_visited

		if current_node.check_solution(goal_state):
			print("Total memory usage: " + str(total*1.049))
			#print_solution(current_node, number_nodes_visited)
			#print("Expanded nodes: " + str(number_nodes_expanded))
			#print("Visited nodes: " + str(number_nodes_visited))
			#print("Found solution at depth: " + str(current_node.depth))
			return True
		
		child_nodes = current_node.descendants(improved_descendants)

		for child in child_nodes:
			child_f = child.heuristic_manhattan(goal_state, improved_heuristic)
			number_nodes_expanded += 1
			prior_queue.put((child_f, child))

	return False		
