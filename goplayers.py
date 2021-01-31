import random
from goutils import createGroup, createSurroundingOpponentGroups, isSurrounded, boardsEqual, deleteGroup
from gogame import Game

class randomPlayer():
	def __init__(self, game, color):
		self.game = game
		self.color = color

	def generateMove(self):
		#TODO: Think about restructuring the utility functions somehow sensibly
		flatBoard = [stone for sublist in self.game.board for stone in sublist]
		emptyCells = [i for i,stone in zip(range(len(flatBoard)), flatBoard) if stone == 0]
		random.shuffle(emptyCells)
		continueSearch = True
		for i in emptyCells:
			y = i // self.game.gamesize
			x = i % self.game.gamesize
			testboard = [row.copy() for row in self.game.board]
			changed_group = self.game.createGroup(x,y,self.color)
			opponent_groups = self.game.createSurroundingOpponentGroups(changed_group, self.color)
			testboard[y][x] = self.color
			for opponent_group in opponent_groups:#Delete groups that were surrounded by the move
				if isSurrounded(testboard, opponent_group):
					deleteGroup(testboard, opponent_group)
			if isSurrounded(testboard, changed_group):#Check if the move is a suicide
				continue
			if boardsEqual(testboard, self.game.prevprevboard):#Check for ko rule
				continue
			return (y,x)
		raise Exception("No possible move to make!")

class randomPlayerV2():
	def __init__(self, game, color):
		self.game = game
		self.color = color

	def generateMove(self):
		"""Generates a random move but not in a region that is already unconditionally alive"""
		_, aliveWhiteRegions = self.game.findUnconditionallyAliveGroups(1)
		_, aliveBlackRegions = self.game.findUnconditionallyAliveGroups(-1)
		aliveWhiteRegions = {pos for sublist in aliveWhiteRegions for pos in sublist}#Flatten
		aliveBlackRegions = {pos for sublist in aliveBlackRegions for pos in sublist}
		allPositions = ((x,y) for x in range(self.game.gamesize) for y in range(self.game.gamesize))
		emptyCells = [(y,x) for (y,x) in allPositions if self.game.board[y][x] == 0 and 
			not (y,x) in aliveWhiteRegions and not (y,x) in aliveBlackRegions]
		random.shuffle(emptyCells)
		for (y,x) in emptyCells:
			testboard = [row.copy() for row in self.game.board]
			changed_group = self.game.createGroup(x,y,self.color)
			opponent_groups = self.game.createSurroundingOpponentGroups(changed_group, self.color)
			testboard[y][x] = self.color
			for opponent_group in opponent_groups:#Delete groups that were surrounded by the move
				if isSurrounded(testboard, opponent_group):
					deleteGroup(testboard, opponent_group)
			if isSurrounded(testboard, changed_group):#Check if the move is a suicide
				continue
			if boardsEqual(testboard, self.game.prevprevboard):#Check for ko rule
				continue
			return (y,x)
		return (-1,-1)#Pass

class monteCarloUnconditionalLifePlayer():
	def __init__(self, game, color):
		self.game = game
		self.color = color

	def getPlausibleMoves(self,game):
		_, aliveWhiteRegions = game.findUnconditionallyAliveGroups(1)
		_, aliveBlackRegions = game.findUnconditionallyAliveGroups(-1)
		aliveWhiteRegions = {pos for sublist in aliveWhiteRegions for pos in sublist}#Flatten
		aliveBlackRegions = {pos for sublist in aliveBlackRegions for pos in sublist}
		allPositions = ((x,y) for x in range(game.gamesize) for y in range(game.gamesize))
		emptyCells = [(y,x) for (y,x) in allPositions if game.board[y][x] == 0 and 
			not (y,x) in aliveWhiteRegions and not (y,x) in aliveBlackRegions]
		return emptyCells

	def getAllowedMoves(self,game):
		"""Gets all allowed moves that are also sensible with respect to unconditionally alive regions"""
		plausible_moves = self.getPlausibleMoves(game)
		allowed_moves = []
		for (y,x) in plausible_moves:
			testboard = [row.copy() for row in game.board]
			changed_group = game.createGroup(x,y,game.turn)
			opponent_groups = game.createSurroundingOpponentGroups(changed_group, game.turn)
			testboard[y][x] = game.turn
			for opponent_group in opponent_groups:#Delete groups that were surrounded by the move
				if isSurrounded(testboard, opponent_group):
					deleteGroup(testboard, opponent_group)
			if isSurrounded(testboard, changed_group):#Check if the move is a suicide
				continue
			if boardsEqual(testboard, game.prevprevboard):#Check for ko rule
				continue
			allowed_moves.append((y,x))
		return allowed_moves

	def sampleWinner(self,x,y):
		"""TODO: quite inefficient right now"""
		sampleGame = self.game.createCopy()
		allowed_moves = self.getAllowedMoves(sampleGame)
		random.shuffle(allowed_moves)
		while(len(allowed_moves) > 0):
			for (y,x) in allowed_moves:
				sampleGame.makeMove(x,y)
			allowed_moves = self.getAllowedMoves(sampleGame)
			random.shuffle(allowed_moves)
		winner = sampleGame.checkWinnerUnconditionalLife()
		return winner

	def generateMove(self):
		"""The strategy: Do monte carlo search on on all the different moves."""
		allowed_moves = self.getAllowedMoves(self.game)
		player = self.game.turn
		if len(allowed_moves) > 0:
			wins_with_move = {pos:0 for pos in allowed_moves}
			K = 10
			for (y,x) in allowed_moves:
				print("Sampling {},{}".format(x,y))
				for i in range(K):
					winner = self.sampleWinner(x,y)
					wins_with_move[(y,x)] += winner*player#If player is -1, then the count gets flipped as it should
			best_move = max(wins_with_move, key=wins_with_move.get)
			print("Estimated balance with move: {}".format(wins_with_move[best_move]))
			return best_move
		else:
			return (-1,-1)