import numpy as np


def dfs(start_node, end_node, limit):
	stack = [start_node]

	while len(stack) != 0:
		state = stack.pop()

		state.print_board()

		if state.check_solution(end_node):
			print("Solution found at depth  ", state.depth)
			state.print_board()
			return True

		if(state.depth < limit):
			child_nodes = state.descendants()
			for i in range(len(child_nodes)):
				stack.insert(0,child_nodes[i])

	return False