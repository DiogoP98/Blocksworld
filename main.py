import numpy as np
import node
import methods

initial_state = [0,0,0,0,0,0,0,0,0,0,0,0,'A','B','C',1] #1 represents the agent
goal_state = [0,0,0,0,0,'A',0,0,0,'B',0,0,0,'C',0,1] #Agent position doesnt matter

def find_agent():
	agent = [None]*2
	for i in range(16):
		if initial_state[i] == 1:
			agent[0] = i%4
			agent[1] = round(i/4)-1
			break
	return agent

def main():
	agent = find_agent()
	start_node = node.Node(initial_state, agent, 0)

if __name__ == '__main__':
	main()