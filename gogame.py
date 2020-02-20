

class Game:
	def __init__(self, size):
		self.gamesize = size
		self.board = [[0 for i in range(self.gamesize)] for j in range(self.gamesize)]
		self.turn = -1
		#self.previousmove = (-1,-1)
		#self.prevprevmove = (-1,-1)
		self.previousboard = [row.copy() for row in self.board]
		self.prevprevboard = [row.copy() for row in self.board]

	def makeMove(self, x, y):
		"""Tries to make a move on the board if it's legal."""
		print("Making move: {},{} by player {}".format(x,y,self.turn))
		if self.board[y][x] == 0:
			changed_group = self.createGroup(x,y,self.turn)
			opponent_groups = self.createSurroundingOpponentGroups(changed_group, self.turn)
			self.board[y][x] = self.turn #Put the stone in place to test if it is legal
			for opponent_group in opponent_groups:#Delete groups that were surrounded by the move
				if self.isSurrounded(opponent_group):
					self.deleteGroup(opponent_group)
			if self.isSurrounded(changed_group):#Check if the move is a suicide
				self.board[y][x] = 0
				print("Move illegal: Suicide!")
				return False
			if self.boardsEqual(self.board, self.prevprevboard):#Check for ko rule
				print("Move illegal: Ko rule!")
				for opponent_group in opponent_groups:
					self.restoreGroup(opponent_group, -self.turn)
				self.board[y][x] = 0
				return False
			self.turn = -self.turn
			self.prevprevboard = self.previousboard
			self.previousboard = [row.copy() for row in self.board]
			return True
		else:
			print("Move illegal: Cell full!")
			return False

	def boardsEqual(self, board1, board2):
		for y in range(len(board1)):
			for x in range(len(board1)):
				if board1[y][x] != board2[y][x]:
					return False
		return True

	def restoreGroup(self, group, player):
		for (y,x) in group:
			self.board[y][x] = player

	def createSurroundingOpponentGroups(self,group,player):
		stones_considered = set()
		opponent_groups = []
		for (y,x) in group:
			if x > 0 and self.board[y][x-1] == -player and not (y,x-1) in stones_considered:
				opponent_groups.append(self.createGroup(x-1,y,-player))
			if x < self.gamesize - 1 and self.board[y][x+1] == -player and not (y,x+1) in stones_considered:
				opponent_groups.append(self.createGroup(x+1,y,-player))
			if y > 0 and self.board[y-1][x] == -player and not (y-1,x) in stones_considered:
				opponent_groups.append(self.createGroup(x,y-1,-player))
			if y < self.gamesize - 1 and self.board[y+1][x] == -player and not (y+1,x) in stones_considered:
				opponent_groups.append(self.createGroup(x,y+1,-player))
		return opponent_groups

	def createGroup(self,x,y,player):
		return self.createGroupRec(x,y,player,set())

	def createGroupRec(self,x,y,player,group_so_far):
		returnset = group_so_far.copy()
		returnset.add((y,x))
		if x > 0 and self.board[y][x-1] == player and not (y,x-1) in returnset:
			returnset = self.createGroupRec(x-1,y,player,returnset)
		if x < self.gamesize - 1 and self.board[y][x+1] == player and not (y,x+1) in returnset:
			returnset = self.createGroupRec(x+1,y,player,returnset)
		if y > 0 and self.board[y-1][x] == player and not (y-1,x) in returnset:
			returnset = self.createGroupRec(x,y-1,player,returnset)
		if y < self.gamesize - 1 and self.board[y+1][x] == player and not (y+1,x) in returnset:
			returnset = self.createGroupRec(x,y+1,player,returnset)
		return returnset

	def isSurrounded(self,stone_group):
		"""This doesn't require knowing the player since by definition, the group shouldn't have neighbors that are
		the same color."""
		for (y,x) in stone_group:
			if x > 0 and self.board[y][x-1] == 0:
				return False
			elif x < self.gamesize - 1 and self.board[y][x+1] == 0:
				return False
			elif y > 0 and self.board[y-1][x] == 0:
				return False
			elif y < self.gamesize - 1 and self.board[y+1][x] == 0:
				return False
		return True

	def deleteGroup(self,stone_group):
		for (y,x) in stone_group:
			self.board[y][x] = 0

	def makeCapturesAll(self):
		"""Searches through the board and makes all captures in some arbitrary order. Not really needed for normal play."""
		stone_groups = []
		stones_considered = set()#The locations of stones that have already been considered

		print("Making captures")

		group_index = 0
		changed_group_index = -1
		for x in range(self.gamesize):
			for y in range(self.gamesize):
				new_group = set()
				if self.board[y][x] > 0 and not (y,x) in stones_considered:
					new_group = self.createGroup(x, y, 1)
				elif self.board[y][x] < 0 and not (y,x) in stones_considered:
					new_group = self.createGroup(x, y, -1)
				stones_considered.update(new_group)
				#Make sure that the group that was changed or added is the last one  TODO: simplify
				if len(new_group) > 0:
					stone_groups.append(new_group)
					if (latest_y, latest_x) in new_group:
						changed_group_index = group_index
					group_index += 1

		for group in stone_groups:
			if isSurrounded(group):
				deleteGroup(group)
		if isSurrounded(changed_group):#TODO: Should change so that the move isn't legal in the first place if this happens
			deleteGroup(changed_group)
