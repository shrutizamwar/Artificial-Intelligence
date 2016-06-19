

import sys

''' BFS implementation'''
def BFS(initial_state, goal_state,children,start_time):
	frontier = []
	explored =[]
	frontier.append({'state':initial_state,'parent':0,'cost':start_time})	
	while len(frontier) > 0:
		node = frontier.pop(0)
		explored.append(node)
		if node['state'] in children:
			actions = children[node['state']]
			for i in range(0,len(actions)):
				explored_flag = 0
				frontier_flag = 0
				child = {'state':actions[i]['name'],'parent':node['state'],'cost': node['cost']+1}
				for item in frontier:
					if item['state'] == child['state']:
						frontier_flag = 1
						break	
				for item in explored:
					if item['state'] == child['state']:
						explored_flag = 1
						break						
				if explored_flag == 0 and frontier_flag == 0:
					if child['state'] in goal_state:
						return child['state'] + " " + str(child['cost']%24)
					frontier.append(child)
	return "None"

'''DFS Implementation '''
def DFS(initial_state, goal_state,children,start_time):
	node = {'state':initial_state,'parent':0,'cost':start_time}
	frontier = []
	frontier.append(node)
	explored =[]
	while len(frontier) > 0:
		node = frontier.pop(-1)
		if node['state'] in goal_state:
			return node['state'] + " " + str(node['cost']%24)
		explored.append(node['state'])
		if node['state'] in children:
			actions = sorted(children[node['state']],key=lambda k: k['name'], reverse=True)
			for i in range(0,len(actions)):
				child = {'state':actions[i]['name'],'parent':node['state'],'cost': node['cost']+1}		
				if child['state'] not in explored:
					frontier.append(child)
	return "None"

def UCS(initial_state, goal_state,children,start_time):
	node = {'state':initial_state,'parent':0,'cost':start_time}
	frontier = []
	frontier.append(node)
	explored =[]
	time = start_time
	current_node = 0
	while len(frontier) > 0:
		print frontier
		current_node = frontier.pop(0)
		if current_node['state'] in goal_state:
			return current_node['state'] + " " + str(current_node['cost']%24)
		explored.append(current_node)
		if current_node['state'] in children:
			actions = children[current_node['state']]
			for i in range(0,len(actions)):
				off_periods = actions[i]['off']
				off_flag = 0
				if len(off_periods) > 0:
					for off in off_periods:
						offs = off.split("-")
						if int(offs[0]) <= (current_node['cost'])%24 <= int(offs[1]):
							off_flag = 1
							break
				if off_flag == 0:
					explored_flag = 0
					frontier_flag = 0
					child = {'state':actions[i]['name'],'parent':current_node['state'],'cost': current_node['cost']+int(actions[i]['cost'])}
					for item in frontier:
						if item['state'] == child['state']:
							frontier_flag = 1
							break	
					for item in explored:
						if item['state'] == child['state']:
							explored_flag = 1
							break					
					if explored_flag == 0:
						if frontier_flag == 0:
							frontier.append(child)
						else:
							for node in frontier:
								if node['state'] == child['state']:
									if node['cost'] > child['cost']:
										frontier.remove(node)
										frontier.append(child)

				frontier = sorted(frontier, key=lambda k: k['state'])
				frontier = sorted(frontier, key=lambda k: k['cost'])
	return "None"

#open input file
input_file = open(sys.argv[2], "r")
output = open("output.txt", "w")
testcases = int(input_file.readline())
for i in range(0,testcases):
	algorithm = input_file.readline().strip()
	source_node = input_file.readline().strip()
	destination_nodes = input_file.readline().split()
	middle_nodes = input_file.readline().split()
	num_pipes = int(input_file.readline())
	children ={}
	for j in range(0,num_pipes):
		connection = input_file.readline().split()
		child = {'name':connection[1],'cost':connection[2]}
		
		num_off_periods = int(connection[3])
		if num_off_periods !=0:
			child['off'] = connection[4:]
		else:
			child['off'] = []

		if connection[0] in children:
			children[connection[0]].append(child)
		else:
			list = [child];
			children[connection[0]] = list
	for key, value in children.items():
		children[key] = sorted(value, key=lambda k: k['name'])
	start_time = int(input_file.readline())
	
	input_file.readline()
	solutions = []
	if algorithm == "BFS":
		solution = BFS(source_node , destination_nodes , children , start_time)
	elif algorithm == "DFS":
		solution = DFS(source_node , destination_nodes , children , start_time)
	elif algorithm == "UCS":
		solution = UCS(source_node , destination_nodes , children , start_time)
	output.write(solution+"\n")
input_file.close()
output.close()


