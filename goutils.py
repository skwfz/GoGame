

def boardsEqual(board1, board2):
	for y in range(len(board1)):
		for x in range(len(board1)):
			if board1[y][x] != board2[y][x]:
				return False
	return True

def createSurroundingOpponentGroups(board,group,player):
	stones_considered = set()
	gamesize = len(board)
	opponent_groups = []
	for (y,x) in group:
		if x > 0 and board[y][x-1] == -player and not (y,x-1) in stones_considered:
			opponent_groups.append(createGroup(board,x-1,y,-player))
		if x < gamesize - 1 and board[y][x+1] == -player and not (y,x+1) in stones_considered:
			opponent_groups.append(createGroup(board,x+1,y,-player))
		if y > 0 and board[y-1][x] == -player and not (y-1,x) in stones_considered:
			opponent_groups.append(createGroup(board,x,y-1,-player))
		if y < gamesize - 1 and board[y+1][x] == -player and not (y+1,x) in stones_considered:
			opponent_groups.append(createGroup(board,x,y+1,-player))
	return opponent_groups

def createGroup(board,x,y,player):
	return createGroupRec(board,x,y,player,set())

def createGroupRec(board,x,y,player,group_so_far):
	returnset = group_so_far.copy()
	returnset.add((y,x))
	gamesize = len(board)
	if x > 0 and board[y][x-1] == player and not (y,x-1) in returnset:
		returnset = createGroupRec(board,x-1,y,player,returnset)
	if x < gamesize - 1 and board[y][x+1] == player and not (y,x+1) in returnset:
		returnset = createGroupRec(board,x+1,y,player,returnset)
	if y > 0 and board[y-1][x] == player and not (y-1,x) in returnset:
		returnset = createGroupRec(board,x,y-1,player,returnset)
	if y < gamesize - 1 and board[y+1][x] == player and not (y+1,x) in returnset:
		returnset = createGroupRec(board,x,y+1,player,returnset)
	return returnset

def deleteGroup(board,stone_group):
	for (y,x) in stone_group:
		board[y][x] = 0

def isSurrounded(board,stone_group):
	"""This doesn't require knowing the player since by definition, the group shouldn't have neighbors that are
	the same color."""
	gamesize = len(board)
	for (y,x) in stone_group:
		if x > 0 and board[y][x-1] == 0:
			return False
		elif x < gamesize - 1 and board[y][x+1] == 0:
			return False
		elif y > 0 and board[y-1][x] == 0:
			return False
		elif y < gamesize - 1 and board[y+1][x] == 0:
			return False
	return True