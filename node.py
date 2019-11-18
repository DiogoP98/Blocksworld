import numpy as np
import matplotlib.pyplot as plt
import random

class Node:

	def __init__(self, board, agent, depth, parent = None, move = None):
		self.board = board
		self.agent = agent
		self.depth = depth
		self.count = 0 #keep track of number of nodes visited, for debug purposes
		self.parent = parent
		self.move = move #keeps track of the move made previously, so that doens't make the symmetric move after, we would be going backwards if that happened
	
	def __lt__(self, other): #for A*: when they have same value, the tiebracker is the distance at which the agent is to the closest tile 
		letters_list = ['A', 'B', 'C']
		dist_1 = 10
		dist_2 = 10
		for tile in range(0,16):
			if self.board[tile] in letters_list:
				current_x =  tile % 4
				current_y =  tile // 4
				distance_to_agent = abs(current_x - self.agent[0]) + abs(current_y - self.agent[1])
				dist_1 = min(dist_1, distance_to_agent)
			if other.board[tile] in letters_list:
				current_x =  tile % 4
				current_y =  tile // 4
				distance_to_agent = abs(current_x - other.agent[0]) + abs(current_y - other.agent[1])
				dist_2 = min(dist_2, distance_to_agent)

		if dist_2 > dist_1:
			return True
		else:
			return False
	
	#find all possible descendants
	def descendants(self, improved):
		desc = []
		possibleMoves = [(0,1),(0,-1),(1,0),(-1,0)] #go up, down, right and left

		random.shuffle(possibleMoves) #randomize chosen moves

		for i in range(4):
			if improved and self.move != None: 
				if possibleMoves[i] == tuple(np.multiply((-1,-1), self.move)): #if move is symmetric to the one done previously
					continue
			
			current_x_position = self.agent[0]
			current_y_position = self.agent[1]

			new_x_position = current_x_position + possibleMoves[i][0]
			new_y_position = current_y_position + possibleMoves[i][1]
			
			if new_x_position < 0 or new_y_position < 0 or new_x_position > 3 or new_y_position > 3:
				continue

			board = self.board.copy()

			old_value = board[new_y_position * 4 + new_x_position] #check the value before change

			if(old_value == 'O'): #obstacle, cannot pass
				continue
			board[current_y_position * 4 + current_x_position] = old_value
			board[new_y_position * 4 + new_x_position] = 1

			new_agent = [new_x_position,new_y_position]
			
			if improved:
				desc.append(Node(board,new_agent,self.depth+1,self,possibleMoves[i]))
			else:
				desc.append(Node(board,new_agent,self.depth+1,self))
				
		return desc

	def heuristic_manhattan(self, end_state, boost):
		value = 0
		letters_accounted = 0
		agent_distance_to_misplaced_tile = 0

		final_pos = self.get_position(end_state)

		for tile in range(0,16):
			value_of_tile = self.board[tile]
			if value_of_tile == 'A':
				final_tile = final_pos[0]
			elif value_of_tile == 'B':
				final_tile = final_pos[1]
			elif value_of_tile == 'C':
				final_tile = final_pos[2]
			else:
				continue
						
			current_x =  tile % 4
			current_y =  tile // 4

			final_x = final_tile % 4
			final_y = final_tile // 4

			distance = abs(current_x - final_x) + abs(current_y - final_y)
			value += distance

			if distance != 0:
				agent_distance_to_misplaced_tile = max(agent_distance_to_misplaced_tile, abs(current_x - self.agent[0]) + abs(current_y - self.agent[1]))

			letters_accounted += 1
			if letters_accounted == 3: # no need to stay in the loop if already found the 3 letters
				break
		
		if boost: #improved heuristic, that also takes into account the location of the agent
			return value + agent_distance_to_misplaced_tile
		else:
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

	def check_solution(self, end_state):
		letters = ['A', 'B', 'C']
		for i in range(16):
			if self.board[i] != end_state[i]:
				if (self.board[i] in letters) or (end_state[i] in letters):
					return False
		return True

	def print_board(self, fig, dimensions, count):
		ax = fig.add_subplot(dimensions, dimensions, count)

		for x in range(5):
			ax.plot([x, x], [0,4], 'k')
		for y in range(5):
			ax.plot([0, 4], [y,y], 'k')
		
		agent = plt.imread('Images/agent.png')
		obstacle = plt.imread('Images/block.jpg')
		A = plt.imread('Images/A_letter.png')
		B = plt.imread('Images/B_letter.png')
		C = plt.imread('Images/C_letter.png')
		extent = np.array([-0.3, 0.3, -0.3, 0.3])
		ax.set_axis_off()

		for i in range(16):
			x_coord = i % 4 + 0.5
			y_coord = 3.5 - i // 4
			if(self.board[i] == 'A'):
				ax.imshow(A, extent=extent + [x_coord, x_coord, y_coord, y_coord])
			elif(self.board[i] == 'B'):
				ax.imshow(B, extent=extent + [x_coord, x_coord, y_coord, y_coord])
			elif(self.board[i] == 'C'):
				ax.imshow(C, extent=extent + [x_coord, x_coord, y_coord, y_coord])
			elif(self.board[i] == 'O'):
				ax.imshow(obstacle, extent=extent + [x_coord, x_coord, y_coord, y_coord])
			elif(self.board[i] == 1):
				ax.imshow(agent, extent=extent + [x_coord, x_coord, y_coord, y_coord])
	
		ax.set(xticks=[], yticks=[])
		ax.axis('image')
		if self.parent != None:
			ax.set_title("Node: " + str(self.count) + ", Parent: " + str(self.parent.count) + ", Depth: " + str(self.depth))
		else:
			ax.set_title("Node: " + str(self.count) + ", Parent: None" + ", Depth: " + str(self.depth))

	def print_path(self, fig, dimensions, count):
		if self.parent != None:
			self.parent.print_path(fig, dimensions, count = count + 1)
		
		self.print_board(fig, dimensions, count)

	def print_path_reserse(self, fig, dimensions, count):
		self.print_board(fig, dimensions, count)

		if self.parent != None:
			self.parent.print_path_reserse(fig, dimensions, count = count + 1)







