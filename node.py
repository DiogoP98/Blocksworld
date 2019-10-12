import numpy as np

class Node:

	def __init__(self, board, agent, depth, parent=None):
		self.board = board
		self.agent = agent
		self.depth = depth
		self.parent = parent
	
	def __lt__(self, other): #for A*: when they have same value, the tiebracker is the distance at which the agent is to the closest tile 
		letters_list = ['A', 'B', 'C']
		dist_1 = 10
		dist_2 = 10
		for tile in range(0,16):
			if self.board[tile] in letters_list:
				current_x =  tile % 4
				current_y =  round(tile / 4) - 1
				distance_to_agent = abs(current_x - self.agent[0]) + abs(current_y - self.agent[1])
				dist_1 = min(dist_1, distance_to_agent)
			if other.board[tile] in letters_list:
				current_x =  tile % 4
				current_y =  round(tile / 4) - 1
				distance_to_agent = abs(current_x - self.agent[0]) + abs(current_y - self.agent[1])
				dist_2 = min(dist_2, distance_to_agent)

		if dist_2 > dist_1:
			return True
		else:
			return False
	
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

	def heuristic_manhattan(self, end_state):
		value = 0
		letters_accounted = 0

		final_pos = self.get_position(end_state)
		final_tile = 0

		for tile in range(0,16):
			if self.board[tile] == 0:
				continue
			elif self.board[tile] == 'A':
				final_tile = final_pos[0]
			elif end_state[tile] == 'B':
				final_tile = final_pos[1]
			elif end_state[tile] == 'C':
				final_tile = final_pos[2]
						
			current_x =  tile % 4
			current_y =  round(tile / 4) - 1

			final_x = final_tile % 4
			final_y = round(final_tile / 4) - 1

			value += abs(current_x - final_x) + abs(current_y - final_y)

			letters_accounted += 1
			if letters_accounted == 3: # no need to stay in the loop if already found the 3 letters
				break
	
		return value
	
	def get_position(self, end_state):
		list_posi = [None] * 3
		
		for tile in range(0,16):
			if end_state[tile] == 'A':
				list_posi[0] = tile
			elif end_state[tile] == 'B':
				list_posi[1] = tile
			elif end_state[tile] == 'C':
				list_posi[2] = tile
		
		return list_posi

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







