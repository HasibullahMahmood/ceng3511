import sys

if len(sys.argv)!= 2:
	print("File Name not Entered")
	sys.exit(1)
if sys.argv[1] != "graph.txt":
	print("Incorrect File Name")
	sys.exit(1)

file = open(sys.argv[1], 'r')
graph = {}
for line in file.readlines():
	key = line[0]
	line = line.replace("\n","")
	line = line[3:-1]
	lists = []
	for i in line.split(", "):
		if int(i[2]) > 0:
			lists.append(i)
	graph[key] = lists
file.close()

def check(graph_to_search, start, end):
	if start not in graph_to_search:
		print("The Letter \"" + start + '\" Not Found In Graph !')
		sys.exit(1)
	if end not in graph_to_search:
		print("The Letter \"" + end + '\" Not Found In Graph !')
		sys.exit(1)

def bfs(graph_to_search, start, end):
	queue = [[start]]
	visited = set()

	while queue:
		# Gets the first path in the queue
		path = queue.pop(0)

		# Gets the last node in the path
		vertex = path[-1]

		# Checks if we got to the end
		if vertex == end:
			return path
		# We check if the current node is already in the visited nodes set in order not to recheck it
		elif vertex not in visited:
			# enumerate all adjacent nodes, construct a new path and push it into the queue
			for current_neighbour in graph_to_search.get(vertex, []):
				new_path = list(path)
				new_path.append(current_neighbour[0])
				queue.append(new_path)
			# Mark the vertex as visited
			visited.add(vertex)
	return 0


def dfs_paths(graph_to_search, start, goal):
	stack = [(start, [start])]
	visited = set()
	while stack:
		(vertex, path) = stack.pop()
		if vertex not in visited:
			if vertex == goal:
				return path
			visited.add(vertex)
			for neighbor in sorted(graph_to_search[vertex], reverse=True):
				stack.append((neighbor[0], path + [neighbor[0]]))
	return 0


def ucs(graph_to_search, start, end):
	queue = [(0,[start])]
	visited = set()
	while queue:
		path = queue.pop(0)
		vertex = path[1][-1]
		if vertex == end:
			return path[1]
		elif vertex not in visited:
			for current_neighbour in graph_to_search.get(vertex, []):
				new_path = list(path[1])
				new_path.append(current_neighbour[0])
				new_path = (path[0] + int(current_neighbour[2]), new_path)
				queue.append(new_path)
			queue.sort(key= lambda x:x[0])
			visited.add(vertex)
	return 0


start_state = input("Please enter the start state : ")
Goal_state = input("Please enter the goal state : ")

check(graph, start_state, Goal_state)
result_bfs = bfs(graph, start_state, Goal_state)
result_dfs = dfs_paths(graph, start_state, Goal_state)
result_ucs = ucs(graph, start_state, Goal_state)

print("BFS : ", end="")
if result_bfs == 0:
	print("No Path Exists Between The Two Nodes")
else:
	print(*result_bfs, sep=" - ")

print("DFS : ", end="")
if result_dfs == 0:
	print("No Path Exists Between The Two Nodes")
else:
	print(*result_dfs, sep=" - ")

print("UCS : ", end="")
if result_ucs == 0:
	print("No Path Exists Between The Two Nodes")
else:
	print(*result_ucs, sep=" - ")

sys.exit(0)