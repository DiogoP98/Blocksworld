import numpy as np

class Node:

	def __init__(self, board, agent, depth):
		self.board = board
		self.agent = agent
		self.depth = depth

	#find all possible descendants
	def descendants(self):
		desc = []
		possibleMoves = [(0,1),(0,-1),(1,0),(-1,0)] #go up, down, right and left

		for i in range(4):
			current_x_position = self.agent[0]
			current_y_position = self.agent[1]

			new_x_position = current_x_position + possibleMoves[i][0]
			new_y_position = current_y_position + possibleMoves[i][1]
			
			if new_x_position < 0 or new_y_position < 0 or new_x_position > 3 or new_y_position > 3:
				continue

			board = self.board.copy()

			old_value = board[new_y_position * 4 + new_x_position] #check the value before change
			board[current_y_position * 4 + current_x_position] = old_value
			board[new_y_position * 4 + new_x_position] = 1

			new_agent = [new_x_position,new_y_position]

			desc.append(Node(board,new_agent,self.depth+1))

		return desc

	def compare_nodes(self, other_node):
		letters = ['A', 'B', 'C']
		for i in range(16):
			if self.board[i] != other_node.board[i]:
				if (self.board[i] in letters) or (other_node.board[i] in letters):
					return False
		return True

	def check_solution(self, goal_state):
		return self.compare_nodes(goal_state)

	def print_board(self):
		for i in range(16):
			print(self.board[i], end = ' ')

			if i % 4 == 3:
				print("\n")

		print("--------") 







