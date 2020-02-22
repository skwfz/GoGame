import random
from goutils import createGroup, createSurroundingOpponentGroups, isSurrounded, boardsEqual, deleteGroup

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