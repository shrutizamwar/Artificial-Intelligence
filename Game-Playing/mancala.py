import sys
from copy import deepcopy
MAX_PLAYER = 0
MIN_PLAYER = 0
PLAY_PITS = 0
MIN_SCORING_PIT = 0
MAX_SCORING_PIT = 0
TOTAL_PITS = 0
NEXT_MOVE = {}
PLAYER_NAME = { 1:'B', 2:'A'}
BEST_VALUE = -50000
POS_INFINITY = 50000
NEG_INFINITY = -50000
traverse = open("traverse_log.txt","w")

def toString(a):
	if a == POS_INFINITY:
		return "Infinity"
	elif a == NEG_INFINITY:
		return "-Infinity"
	else:
		return str(a)

def printNextMove(state):
	output = open("next_state.txt", "w")
	board2 = state[PLAY_PITS + 2 : PLAY_PITS * 2 + 2 ]
	board2 = board2[::-1]
	for i in range(0, len(board2)):
		output.write(str(board2[i])+" ")
	output.write("\n")
	for i in range(1, PLAY_PITS + 1):
		output.write(str(state[i])+" ")
	output.write("\n")
	output.write(str(state[0]))
	output.write("\n")
	output.write(str(state[1+PLAY_PITS]))
	output.close()

def getLegalMoves(node,player):
	moves = [];
	state = node['state']
	if player == 1:
		player_offset = 1
	else:
		player_offset = PLAY_PITS + 2

	for i in range(player_offset, player_offset + PLAY_PITS):
		if state[i] !=0 :
			moves.append(i)
	if player == 1:
		return moves
	else:
		return moves[::-1]

def gameOver(node,player):
	state = node['state']
	player_offset = 1
	pieces_left = 0
	for i in range(player_offset, player_offset + PLAY_PITS):
		pieces_left = pieces_left + state[i]
	if pieces_left == 0:
		score_pit = 0
		for i in range(PLAY_PITS+2, PLAY_PITS + PLAY_PITS + 2):
			state[score_pit] = state[score_pit] + state[i]
			state[i] = 0
		return 1

	player_offset = PLAY_PITS + 2
	pieces_left = 0
	for i in range(player_offset, player_offset + PLAY_PITS):
		pieces_left = pieces_left + state[i]
	if pieces_left == 0:
		score_pit = PLAY_PITS+1
		for i in range(1, PLAY_PITS + 1):
			state[score_pit] = state[score_pit] + state[i]
			state[i] = 0
		return 1
	return 0

def makeMove(move,player,node_state):
	node ={};
	state = deepcopy(node_state)
	position = move
	pieces = state[move]
	opposite_pit_flag = 0
	if player == MAX_PLAYER:
		skip_pit = MIN_SCORING_PIT
		score_pit = MAX_SCORING_PIT
	else:
		skip_pit = MAX_SCORING_PIT
		score_pit = MIN_SCORING_PIT

	if player == 1:
		node['move'] = PLAYER_NAME[player]+str(move+1)
	else:
		node['move'] = PLAYER_NAME[player] + str(TOTAL_PITS - move + 1)

	''' Collect beads from a legal move '''
	state[position] = 0

	''' Distribute the beads sequentially skipping opponents mancala '''
	while(pieces > 0):
		position = (position + 1) % TOTAL_PITS
		if position != skip_pit:
			state[position] = state[position] + 1
			pieces = pieces - 1
		
	''' Check if last bead reaches own mancala get an extra turn '''
	if position != score_pit:
		extraTurn = 0
		if player == 1:
			node['player'] = 2
		else:
			node['player'] = 1
	else:
		extraTurn = 1
		node['player'] = player

	''' check if last bead reached empty play pits'''
	if player == 1:
		if state[position] == 1 and (score_pit - position) > 0:
			opposite_pit = score_pit + score_pit - position
			opposite_pit_flag = 1        

	if player == 2:
		if state[position] == 1 and (skip_pit - position) < 0:
			opposite_pit = skip_pit + skip_pit - position
			opposite_pit_flag = 1

	'''If last bead in empty play pit, collect that last bead and opposite pit beads and add it to the mancala'''
	if opposite_pit_flag:
		state[score_pit] = state[score_pit] + 1
		state[position] = state[position] - 1
		state[score_pit] = state[score_pit] + state[opposite_pit]
		state[opposite_pit] = 0

	''' return the new state and whether the player gets extra turn '''
	node['state'] = state
	return (node,extraTurn)

def greedy(node,depth):
	global NEXT_MOVE
	global BEST_VALUE
	if gameOver(node,node['player']) or depth == 0:
		return node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
	value = NEG_INFINITY
	legal_moves = getLegalMoves(node,node['player'])
	for move in legal_moves:
		child,extraTurn = makeMove(move,node['player'],node['state'])
		if extraTurn == 1:
			value = max(value,greedy(child,depth))				
		elif extraTurn == 0:
			value = max(value,greedy(child,depth - 1))
		if value > BEST_VALUE and depth == DEPTH:
			BEST_VALUE = value
			NEXT_MOVE = child['state']
	return value

def max_eval(node,depth,cap):
	global NEXT_MOVE
	global BEST_VALUE
	global traverse
	if gameOver(node,node['player']) or depth == 0:
		if cap == 0:
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]) + "\n"
			traverse.write(traverse_log)
			return node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
		else:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
			value = node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
			
	else:
		if cap == 0:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
		else:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
		
	legal_moves = getLegalMoves(node,node['player'])
	for move in legal_moves:
		child,extraTurn = makeMove(move,node['player'],node['state'])
		if cap == 1:
			value = min(value,max_eval(child,depth,extraTurn))
		elif cap == 0:
			value = max(value,min_eval(child,depth - 1,extraTurn))
			if value > BEST_VALUE and depth == DEPTH:
				BEST_VALUE = value
				NEXT_MOVE = child['state']
		traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
		traverse.write(traverse_log)
	return value

def min_eval(node,depth,cap):
	global NEXT_MOVE
	global BEST_VALUE
	global traverse
	if gameOver(node,node['player']) or depth == 0:
		if cap == 0:
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT])+"\n"
			traverse.write(traverse_log)
			return node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
		else:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
			value = node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
			
	else:
		if cap == 0:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
		else:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
			traverse.write(traverse_log)
		
	legal_moves = getLegalMoves(node,node['player'])
	for move in legal_moves:
		child,extraTurn = makeMove(move,node['player'],node['state'])
		if cap == 1:
			value = max(value,min_eval(child,depth,extraTurn))
			if value > BEST_VALUE and depth == DEPTH - 1:
				BEST_VALUE = value
				NEXT_MOVE = child['state']
		elif cap == 0:
			value = min(value,max_eval(child,depth - 1,extraTurn))
		traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+"\n"
		traverse.write(traverse_log)
	return value


def alpha_beta_max(node,depth,cap,alpha,beta):
	global NEXT_MOVE
	global BEST_VALUE
	global traverse
	if gameOver(node,node['player']) or depth == 0:
		if cap == 0:
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT])+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
			return node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
		else:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
			value = node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
	else:
		if cap == 0:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
		else:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
		
	legal_moves = getLegalMoves(node,node['player'])
	for move in legal_moves:
		child,extraTurn = makeMove(move,node['player'],node['state'])
		if cap == 1:
			value = min(value,alpha_beta_max(child,depth,extraTurn,alpha,beta))
			if value <= alpha:
				traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
				traverse.write(traverse_log)
				return value
			beta = min(beta,value)
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)

		elif cap == 0:
			value = max(value,alpha_beta_min(child,depth - 1,extraTurn,alpha,beta))
			if value > BEST_VALUE and depth == DEPTH:
				BEST_VALUE = value
				NEXT_MOVE = child['state']			
			if value >= beta:
				traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
				traverse.write(traverse_log)
				return value
			alpha = max(alpha, value)
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
	return value

def alpha_beta_min(node,depth,cap,alpha,beta):
	global NEXT_MOVE
	global BEST_VALUE
	global traverse
	if gameOver(node,node['player']) or depth == 0:
		if cap == 0:
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT])+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
			return node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
		else:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
			value = node['state'][MAX_SCORING_PIT] - node['state'][MIN_SCORING_PIT]
	else:
		if cap == 0:
			value = POS_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
		else:
			value = NEG_INFINITY
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
	legal_moves = getLegalMoves(node,node['player'])
	for move in legal_moves:
		child,extraTurn = makeMove(move,node['player'],node['state'])
		if cap == 1:
			value = max(value,alpha_beta_min(child,depth,extraTurn,alpha,beta))
			if value > BEST_VALUE and depth == DEPTH - 1:
				BEST_VALUE = value
				NEXT_MOVE = child['state']
			if value >= beta:
				traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
				traverse.write(traverse_log)
				return value
			alpha = max(alpha, value)
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)

		elif cap == 0:
			value = min(value,alpha_beta_max(child,depth - 1,extraTurn,alpha,beta))
			if value <= alpha:
				traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
				traverse.write(traverse_log)
				return value
			beta = min(beta,value)
			traverse_log = node['move']+","+str(DEPTH - depth)+","+toString(value)+","+toString(alpha)+","+toString(beta)+"\n"
			traverse.write(traverse_log)
	return value

def main():
	global MAX_PLAYER
	global MIN_PLAYER
	global MIN_SCORING_PIT
	global MAX_SCORING_PIT
	global PLAY_PITS
	global TOTAL_PITS
	global DEPTH
	global NEXT_MOVE
	global traverse
	input_file = open(sys.argv[2], "r")
	task = int(input_file.readline())
	MAX_PLAYER = int(input_file.readline())
	DEPTH = int(input_file.readline())
	board2 = input_file.readline().split()
	board2 = board2[::-1]
	board1 = input_file.readline().split()
	mancala2 = int(input_file.readline())
	mancala1 = int(input_file.readline())
	PLAY_PITS = len(board2)
	TOTAL_PITS = PLAY_PITS * 2 + 2;

	if MAX_PLAYER == 1:
		MIN_PLAYER = 2
		MAX_SCORING_PIT = PLAY_PITS + 1
		MIN_SCORING_PIT = 0
	else:
		MIN_PLAYER = 1
		MAX_SCORING_PIT = 0
		MIN_SCORING_PIT = PLAY_PITS + 1

	state = []
	state.append(mancala2)
	for i in range(0,len(board1)):
		state.append(int(board1[i]))
	state.append(mancala1)
	for i in range(0,len(board2)):
		state.append(int(board2[i]))

	node = {};
	node['move'] = "root"
	node['player'] = MAX_PLAYER
	node['state'] = state

	if task == 1:
		DEPTH = 1
		val = greedy(node, DEPTH)
		printNextMove(NEXT_MOVE)

	if task == 2:
		traverse.write("Node,Depth,Value\n")
		val = max_eval(node,DEPTH,0)
		printNextMove(NEXT_MOVE)

	if task == 3:
		traverse.write("Node,Depth,Value,Alpha,Beta\n")
		val = alpha_beta_max(node, DEPTH,0,NEG_INFINITY,POS_INFINITY)
		printNextMove(NEXT_MOVE)
		
	input_file.close()
	traverse.close()
if __name__ == "__main__":
    main()
