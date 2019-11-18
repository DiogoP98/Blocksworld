import csv
import re

f = open("heuristic_searches.txt", 'r')

searches = ["Bidirectional", "idfs", "BFS", "BFS graph", "DFS 15", "DFS 18"]
list_expanded = []
list_visited = []
list_depth = []
    

for depth in range(15):
    line = f.readline() # title
    print("A* graph misplaced normal descedants at depth " + str(15-depth))
    for _ in range(10):
        line = f.readline() #expanded
        expanded = [int(s) for s in line.split() if s.isdigit()][0]
        list_expanded.insert(0, expanded)
        line = f.readline() #visited
        visited = [int(s) for s in line.split() if s.isdigit()][0]
        list_visited.insert(0, visited)
        line = f.readline()
        depth_found = [int(s) for s in line.split() if s.isdigit()][0] #depth found
        list_depth.insert(0, depth_found)
        line = f.readline() #blank line
    
    print("Expanded:")
    for i in range(len(list_expanded)):
        print(list_expanded[i])

    print("Visited:")
    for i in range(len(list_visited)):
        print(list_visited[i])

    print("Depth:")
    for i in range(len(list_depth)):
        print(list_depth[i])

    list_expanded.clear()
    list_visited.clear()
    list_depth.clear()
    
    line = f.readline() #-------

    line = f.readline() #title
    print("A* graph misplaced improved descedants at depth " + str(15-depth))
    for _ in range(10):
        line = f.readline() #expanded
        expanded = [int(s) for s in line.split() if s.isdigit()][0]
        list_expanded.insert(0, expanded)
        line = f.readline() #visited
        visited = [int(s) for s in line.split() if s.isdigit()][0]
        list_visited.insert(0, visited)
        line = f.readline()
        depth_found = [int(s) for s in line.split() if s.isdigit()][0] #depth found
        list_depth.insert(0, depth_found)
        line = f.readline() #blank line
    
    print("Expanded:")
    for i in range(len(list_expanded)):
        print(list_expanded[i])

    print("Visited:")
    for i in range(len(list_visited)):
        print(list_visited[i])

    print("Depth:")
    for i in range(len(list_depth)):
        print(list_depth[i])

    list_expanded.clear()
    list_visited.clear()
    list_depth.clear()
    
    line = f.readline() #-------

    line = f.readline() #title
    print("A* graph misplaced boost normal descedants at depth " + str(15-depth))
    for _ in range(10):
        line = f.readline() #expanded
        expanded = [int(s) for s in line.split() if s.isdigit()][0]
        list_expanded.insert(0, expanded)
        line = f.readline() #visited
        visited = [int(s) for s in line.split() if s.isdigit()][0]
        list_visited.insert(0, visited)
        line = f.readline()
        depth_found = [int(s) for s in line.split() if s.isdigit()][0] #depth found
        list_depth.insert(0, depth_found)
        line = f.readline() #blank line
    
    print("Expanded:")
    for i in range(len(list_expanded)):
        print(list_expanded[i])

    print("Visited:")
    for i in range(len(list_visited)):
        print(list_visited[i])

    print("Depth:")
    for i in range(len(list_depth)):
        print(list_depth[i])

    list_expanded.clear()
    list_visited.clear()
    list_depth.clear()
    
    line = f.readline() #-------

    line = f.readline() #title
    print("A* graph misplaced boost improved descedants at depth " + str(15-depth))
    for _ in range(10):
        line = f.readline() #expanded
        expanded = [int(s) for s in line.split() if s.isdigit()][0]
        list_expanded.insert(0, expanded)
        line = f.readline() #visited
        visited = [int(s) for s in line.split() if s.isdigit()][0]
        list_visited.insert(0, visited)
        line = f.readline()
        depth_found = [int(s) for s in line.split() if s.isdigit()][0] #depth found
        list_depth.insert(0, depth_found)
        line = f.readline() #blank line
    
    print("Expanded:")
    for i in range(len(list_expanded)):
        print(list_expanded[i])

    print("Visited:")
    for i in range(len(list_visited)):
        print(list_visited[i])

    print("Depth:")
    for i in range(len(list_depth)):
        print(list_depth[i])

    list_expanded.clear()
    list_visited.clear()
    list_depth.clear()
    
    line = f.readline() #------

f.close()


