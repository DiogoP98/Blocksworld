import numpy as np


def dfs(start_node, goal_state, limit):
	stack = [start_node]
	count_nodes = 0

	while len(stack) != 0:
		state = stack.pop()
		count_nodes += 1

		if state.check_solution(goal_state):
			print("Solution found at depth  ", state.depth)
			print("Nodes visited ", count_nodes)
			state.print_path()
			return True

		if(state.depth < limit):
			child_nodes = state.descendants()
			for i in range(len(child_nodes)):
				stack.append(child_nodes[i])

	return False

def bfs(start_node, goal_state):
	queue = [start_node]
	count_nodes = 0
	visited_nodes = set([])

	while len(queue) != 0:
		state = queue.pop(0)
		count_nodes += 1

		visited_nodes.add(state.build_hash())

		if state.check_solution(goal_state):
			print("Solution found at depth  ", state.depth)
			print("Nodes visited: ", count_nodes)
			state.print_path()
			return True

		child_nodes = state.descendants(visited_nodes)
		for i in range(len(child_nodes)):
			queue.append(child_nodes[i])

	return False

def idfs(start_node, goal_state):
	for lim in range(1,20):
		if dfs(start_node, goal_state, lim):
			return True
		print("Not found for depth ", lim)
	return False

def Astar():
	return False		