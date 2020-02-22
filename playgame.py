import pygame
from pygame.locals import *
from gogame import Game
from goplayers import randomPlayer

BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (244,164,96)
GREY = (150,150,150)

# define a main function
def main():
	 
	# initialize the pygame module
	pygame.init()
	# load and set the logo
	pygame.display.set_caption("Go game")
	
	gamesize = 19
	circleradius = 20
	circlediameter = 2*circleradius

	screen = pygame.display.set_mode((gamesize*circlediameter,gamesize*circlediameter))
	screen.fill(BROWN)
	
	def drawBoard(board, blackAlive, whiteAlive):
		for y, row in enumerate(board):
			for x, element in enumerate(row):
				if element < 0:
					pygame.draw.circle(screen, BLACK, (circlediameter*x+circleradius,circlediameter*y+circleradius), circleradius)
				elif element > 0:
					pygame.draw.circle(screen, WHITE, (circlediameter*x+circleradius,circlediameter*y+circleradius), circleradius)
				else:
					pygame.draw.rect(screen, BROWN, pygame.Rect(circlediameter*x, circlediameter*y, circlediameter, circlediameter))
					pygame.draw.rect(screen, GREY, pygame.Rect(circlediameter*x+circleradius-2, circlediameter*y, 5, circlediameter))
					pygame.draw.rect(screen, GREY, pygame.Rect(circlediameter*x, circlediameter*y+circleradius-2, circlediameter, 5))
		for (y,x) in blackAlive:
			pygame.draw.rect(screen, BLACK, pygame.Rect(circlediameter*x + 10, circlediameter*y + 10, 20, 20))
		for (y,x) in whiteAlive:
			pygame.draw.rect(screen, WHITE, pygame.Rect(circlediameter*x + 10, circlediameter*y + 10, 20, 20))

	game = Game(gamesize)

	drawBoard(game.board,[],[])

	pygame.display.update()
	# define a variable to control the main loop
	running = True

	first_player = randomPlayer(game, -1)
	opponent = randomPlayer(game, 1)
	

	blackAlive = {}
	whiteAlive = {}
	# main loop
	while running:
		# event handling, gets all event from the event queue
		for event in pygame.event.get():
			# only do something if the event is of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				click_x, click_y = event.pos
				board_x, board_y = click_x // circlediameter, click_y // circlediameter
				move_succesful = game.makeMove(board_x,board_y)
				#(first_y, first_x) = first_player.generateMove()
				#print(first_x, first_y)
				#move_succesful = game.makeMove(first_x, first_y)
				if move_succesful:
					#print("Unconditionally alive groups:", game.findUnconditionallyAliveGroups(-1))
					(opponent_y, opponent_x) = opponent.generateMove()
					game.makeMove(opponent_x, opponent_y)
					X,R = game.findUnconditionallyAliveGroups(-1)
					blackAlive = {pos for group in R for pos in group}
					X,R = game.findUnconditionallyAliveGroups(1)
					whiteAlive = {pos for group in R for pos in group}

			drawBoard(game.board, blackAlive, whiteAlive)
			pygame.display.update()

	 
	 
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()
