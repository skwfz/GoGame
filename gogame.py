import numpy as np

class Game:
	def __init__(self, size):
		self.gamesize = size
		self.board = [[0 for i in range(self.gamesize)] for j in range(self.gamesize)]
		self.turn = -1
		self.previousboard = [row.copy() for row in self.board]
		self.prevprevboard = [row.copy() for row in self.board]

		self.black_captured = 0
		self.white_captured = 0

		self.movesPassed = 0

		self.info_on = False

	def createCopy(self):
		"""Creates a copy of the game object"""
		new_game = Game(self.gamesize)
		new_game.board = [row.copy() for row in self.board]
		new_game.turn = self.turn
		new_game.previousboard = [row.copy() for row in self.previousboard]
		new_game.prevprevboard = [row.copy() for row in self.prevprevboard]
		new_game.black_captured = self.black_captured
		new_game.white_captured = self.white_captured
		new_game.movesPassed = self.movesPassed
		return new_game

	def makeMove(self, x, y):
		"""Tries to make a move on the board if it's legal."""
		if (x,y) == (-1,-1):
			self.passMove()
		else:
			if self.info_on:
				print("Making move: {},{} by player {}".format(x,y,self.turn))
			if self.board[y][x] == 0:
				amount_captured = 0
				changed_group = self.createGroup(x,y,self.turn)
				opponent_groups = self.createSurroundingOpponentGroups(changed_group, self.turn)
				self.board[y][x] = self.turn #Put the stone in place to test if it is legal
				for opponent_group in opponent_groups:#Delete groups that were surrounded by the move
					if self.isSurrounded(opponent_group):
						amount_captured += len(opponent_group)
						self.deleteGroup(opponent_group)
				if self.isSurrounded(changed_group):#Check if the move is a suicide
					self.board[y][x] = 0
					if self.info_on:
						print("Move illegal: Suicide!")
					return False
				if self.boardsEqual(self.board, self.prevprevboard):#Check for ko rule
					if self.info_on:
						print("Move illegal: Ko rule!")
					for opponent_group in opponent_groups:
						self.restoreGroup(opponent_group, -self.turn)
					self.board[y][x] = 0
					return False
				#Move successful
				if self.turn == 1:
					self.black_captured += amount_captured
				else:
					self.white_captured += amount_captured
				self.turn = -self.turn
				self.prevprevboard = self.previousboard
				self.previousboard = [row.copy() for row in self.board]
				self.movesPassed = 0
				return True
			else:
				if self.info_on:
					print("Move illegal: Cell full!")
				return False

	def passMove(self):
		"""Gives the other player the turn."""
		if self.info_on:
			print("Pass from player {}".format(self.turn))
		self.turn = -self.turn
		self.movesPassed += 1

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
		return self.createGroupRec(x,y,set(),lambda color: color == player)

	def createGroupGeneral(self,x,y,belongs_to_group):
		return self.createGroupRec(x,y,set(),belongs_to_group)

	def createGroupRec(self,x,y,group_so_far,belongs_to_group):
		returnset = group_so_far.copy()
		returnset.add((y,x))
		if x > 0 and belongs_to_group(self.board[y][x-1]) and not (y,x-1) in returnset:
			returnset = self.createGroupRec(x-1,y,returnset,belongs_to_group)
		if x < self.gamesize - 1 and belongs_to_group(self.board[y][x+1]) and not (y,x+1) in returnset:
			returnset = self.createGroupRec(x+1,y,returnset,belongs_to_group)
		if y > 0 and belongs_to_group(self.board[y-1][x]) and not (y-1,x) in returnset:
			returnset = self.createGroupRec(x,y-1,returnset,belongs_to_group)
		if y < self.gamesize - 1 and belongs_to_group(self.board[y+1][x]) and not (y+1,x) in returnset:
			returnset = self.createGroupRec(x,y+1,returnset,belongs_to_group)
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

	def findAllGroups(self, player):
		stones_considered = set()
		stone_groups = []
		for x in range(self.gamesize):
			for y in range(self.gamesize):
				new_group = set()
				if self.board[y][x] == player and not (y,x) in stones_considered:
					new_group = self.createGroup(x, y, player)
				stones_considered.update(new_group)
				if len(new_group) > 0:
					stone_groups.append(new_group)
		return stone_groups

	def findPartionedRegions(self,groups,player):
		"""Finds the region sets that are partioned by the list of groups 'groups' that are of the color 'player'"""
		all_positions = {(y,x) for y in range(self.gamesize) for x in range(self.gamesize)}
		player_positions = {pos for group in groups for pos in group}
		not_player_positions = all_positions.difference(player_positions)
		stones_considered = set()
		partitioned_regions = []
		for (y,x) in not_player_positions:
			if not (y,x) in stones_considered:
				new_region = self.createGroupGeneral(x,y,lambda color: color != player)
				partitioned_regions.append(new_region)
				stones_considered.update(new_region)
		return partitioned_regions

	def filterSmallRegions(self,regions,player):
		"""Filters 'small' regions from all regions partitioned by the player groups
		 according to Bensons algorithm."""
		result = []
		for region in regions:
			isSmall = True
			for (y,x) in region:
				if self.board[y][x] == 0 \
				and not ((x > 0 and self.board[y][x-1] == player) or (x < self.gamesize - 1 and self.board[y][x+1] == player) \
				or (y > 0 and self.board[y-1][x] == player) or (y < self.gamesize - 1 and self.board[y+1][x] == player)):
					isSmall = False
					break
			if isSmall:
				result.append(region)
		return result

	def findVitalCounts(self,X,R):
		"""Related to Bensons algorithm."""
		vitals_to = []
		for region in R:
			vital_to = [True for i in range(len(X))]
			for (y,x) in region:
				for i in range(len(X)):
					if vital_to[i] and not ((x > 0 and (y,x-1) in X[i]) or (x < self.gamesize - 1 and (y,x+1) in X[i]) \
					or (y > 0 and (y-1,x) in X[i]) or (y < self.gamesize - 1 and (y+1,x) in X[i])):
						vital_to[i] = False
			vitals_to.append(vital_to)
		if len(R) > 0:
			vitals_to = np.array(vitals_to)
			vital_counts = vitals_to.sum(axis=0)
			return vital_counts
		else:
			return [0 for i in range(len(X))]

	def filterSmallRegionsBasedOnX(self,R,X,player):
		"""Related to Bensons algorithm. """
		result = []
		flat_X = {pos for group in X for pos in group}
		for region in R:
			stays_in_R = True
			for (y,x) in region:
				if ((x > 0 and self.board[y][x-1] == player and not (y,x-1) in flat_X) \
				or (x < self.gamesize - 1 and self.board[y][x+1] == player and not (y,x+1) in flat_X) \
				or (y > 0 and self.board[y-1][x] == player and not (y-1,x) in flat_X) \
				or (y < self.gamesize - 1 and self.board[y+1][x] == player and not (y+1,x) in flat_X)):
					stays_in_R = False
					continue
			if stays_in_R:
				result.append(region)
		return result

	def findUnconditionallyAliveGroups(self, player):
		"""Finds unconditionally alive groups according to Bensons algorithm"""
		X = self.findAllGroups(player)
		partitioned_regions = self.findPartionedRegions(X, player)
		R = self.filterSmallRegions(partitioned_regions, player)

		X_old = X
		R_old = R
		vital_counts = self.findVitalCounts(X,R)
		X = [group for (i,group) in enumerate(X) if vital_counts[i] >= 2]
		R = self.filterSmallRegionsBasedOnX(R,X,player)

		while len(X) < len(X_old) or len(R) < len(R_old):
			X_old = X
			R_old = R
			vital_counts = self.findVitalCounts(X,R)
			X = [group for (i,group) in enumerate(X) if vital_counts[i] >= 2]
			R = self.filterSmallRegionsBasedOnX(R,X,player)

		if len(R) > 0:
			return X, R
		else:
			return [],[]

	def calculateScoresUnconditionalLife(self):
		_, black_areas = self.findUnconditionallyAliveGroups(-1)
		_, white_areas = self.findUnconditionallyAliveGroups(1)
		black_areas = {pos for sublist in black_areas for pos in sublist}#Flatten
		white_areas = {pos for sublist in white_areas for pos in sublist}
		black_area_points = sum((2 if self.board[y][x] != 0 else 1 for (y,x) in black_areas))
		white_area_points = sum((2 if self.board[y][x] != 0 else 1 for (y,x) in white_areas))
		return (black_area_points + self.white_captured, white_area_points + self.black_captured)

	def checkWinnerUnconditionalLife(self):
		"""Returns the winner of the game by evaluating the board according to the unconditional life method"""
		black_points, white_points = self.calculateScoresUnconditionalLife()
		balance = black_points - white_points
		if balance > 0:
			return -1
		elif balance < 0:
			return 1
		else:
			return 0
		 
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
