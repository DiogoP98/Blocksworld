import numpy as np

class Node:

	def __init__(self, board, agent, depth, parent=None):
		self.board = board
		self.agent = agent
		self.depth = depth
		self.parent = parent

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
			
			desc.append(Node(board,new_agent,self.depth+1,self))
				
		return desc

	def build_hash(self):
		board_hash = ""
		for i in range(0,16):
			board_hash += str(self.board[i])
		return board_hash

	def compare_nodes(self, other_board):
		letters = ['A', 'B', 'C']
		flag = 0
		for i in range(16):
			if self.board[i] != other_board[i]:
				if (self.board[i] in letters) or (other_board[i] in letters):
					return 1
				else:
					flag = 2 #when its only the agent out of position
					continue
		return flag

	def check_solution(self, end_state):
		same = self.compare_nodes(end_state)
		return (same==2) or (same==0)

	def print_board(self):
		for i in range(16):
			print(self.board[i], end = ' ')

			if i % 4 == 3:
				print("\n")

		print("--------")

	def print_path(self):
		if self.parent != None:
			self.parent.print_path()

		self.print_board()

	def print_path_reserse(self):
		self.print_board()

		if self.parent != None:
			self.parent.print_path_reserse()







