import pygame
from algorithms import bfs_solve
from Environment import Environment
myEnvironment = Environment()
def drawMenu(text,position,selected=False):
	font = pygame.font.Font(None,36)
	color = (255,255,0) if selected else (255,255,255)
	text_surface = font.render(text,True,color)
	text_rect = text_surface.get_rect(center=position)
	myEnvironment.screen.blit(text_surface,text_rect)
def drawText(text,position,size=26,color=(255,255,255)):
	font = pygame.font.Font(None,size)
	text_surface = font.render(text,True,color)
	text_rect = text_surface.get_rect(center=position)
	myEnvironment.screen.blit(text_surface,text_rect)
	pygame.display.flip()

def algorithm_menu():
	algorithms = {
		"BFS": bfs_solve	
	}
	selected = 0
	algo_names = list(algorithms.keys())
	while True:
		myEnvironment.screen.fill((0,0,0))
		drawMenu("Select an algorithm",(myEnvironment.size[0]/2,myEnvironment.size[1]/2-50))
		for i,algorithm in enumerate(algo_names):
			drawMenu(algorithm,(myEnvironment.size[0]/2,myEnvironment.size[1]/2+50+50*i),i==selected)
	
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					selected = (selected-1)%len(algorithms)
				elif event.key == pygame.K_DOWN:
					selected = (selected+1)%len(algorithms)
				elif event.key == pygame.K_RETURN:
					return algorithms[algo_names[selected]]
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
def level_menu():
	levels = [f"Level {i}" for i in range(1,11)]
	selected = 0
	while True:
		myEnvironment.screen.fill((0,0,0))
		drawMenu("Select a level",(myEnvironment.size[0]/2,50))
		for i,level in enumerate(levels):
			drawMenu(level,(myEnvironment.size[0]/2,100+50*i),i==selected)			
		pygame.display.flip()
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					selected = (selected-1)%len(levels)
				elif event.key == pygame.K_DOWN:
					selected = (selected+1)%len(levels)
				elif event.key == pygame.K_RETURN:
					return selected+1
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
def drawLevel(matrix_to_draw):
	# Load level images
	wall = pygame.image.load(myEnvironment.getPath() + '/themes/' + '/images/wall.png').convert()
	box = pygame.image.load(myEnvironment.getPath() + '/themes/' +  '/images/box.png').convert()
	box_on_target = pygame.image.load(myEnvironment.getPath() + '/themes/' +  '/images/box_on_target.png').convert()
	space = pygame.image.load(myEnvironment.getPath() + '/themes/' +  '/images/space.png').convert()
	target = pygame.image.load(myEnvironment.getPath() + '/themes/' +  '/images/target.png').convert()
	player = pygame.image.load(myEnvironment.getPath() + '/themes/' +  '/images/player.png').convert()

	images = {'#': wall, ' ': space, '$': box, '.': target, '@': player, '*': box_on_target, '+': player}
	
	# Get image size. Images are always squares so it doesn't care if you get width or height
	box_size = wall.get_width()
	
	# Iterate all Rows
	for i in range (0,len(matrix_to_draw)):
		# Iterate all columns of the row
		for c in range (0,len(matrix_to_draw[i])):
			myEnvironment.screen.blit(images[matrix_to_draw[i][c]], (c*box_size, i*box_size))

	pygame.display.update()