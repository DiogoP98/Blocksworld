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

			changed_x = current_x_position + possibleMoves[i][0]
			changed_y = current_y_position + possibleMoves[i][1]
			
			new_x_position = changed_x % 4
			new_y_position = round(changed_y / 4) - 1

			if new_y_position > 3:
				continue

			board = self.board.copy()

			old_value = board[new_y_position * 4 + new_x_position] #check the value before change
			board[current_y_position * 4 + current_x_position] = old_value
			board[new_y_position * 4 + new_x_position] = 1

			new_agent = [new_x_position,new_y_position]

			desc.append(node(board,new_agent,self.depth+1))

		return desc



