import pygame, sys, math
from queue import PriorityQueue

pygame.init()

NODESIZE = 10
GRIDWIDTH = 50
GRIDSIZE = GRIDWIDTH*NODESIZE


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

SCREEN = pygame.display.set_mode((GRIDSIZE, GRIDSIZE))

class node:
	def __init__(self, y, x, color):
		self.color = color
		self.x = x
		self.y = y
		self.neighbors = []
		self.diag_neighbors = []
		self.g_score = float("inf")
		self.came_from = None
		
	def draw(self):
		self.border_size = 1
		self.box = (self.x * NODESIZE + self.border_size, self.y * NODESIZE + self.border_size, NODESIZE - self.border_size * 2, NODESIZE - self.border_size * 2)
		pygame.draw.rect(SCREEN, self.color, self.box)
		
	def change_color(self, color):
		self.color = color
		self.draw()
	def update_neighbors(self, grid):
		row = self.y
		col = self.x
		if(row != 0):
			if(grid[row - 1][col].color != BLACK):
				self.neighbors.append(grid[row - 1][col])
		if(col != 0):
			if(grid[row][col - 1].color != BLACK):
				self.neighbors.append(grid[row][col - 1])
		if(row != GRIDWIDTH - 1):
			if(grid[row + 1][col].color != BLACK):
				self.neighbors.append(grid[row + 1][col])
		if(col != GRIDWIDTH - 1):
			if(grid[row][col + 1].color != BLACK):
				self.neighbors.append(grid[row][col + 1])
				
		if(row != 0 and col != 0 and grid[row - 1][col - 1].color != BLACK):
			if(grid[row - 1][col].color != BLACK or grid[row][col-1].color != BLACK):
				self.diag_neighbors.append(grid[row - 1][col - 1])	
		if(row != 0 and col != GRIDWIDTH - 1 and grid[row - 1][col + 1].color != BLACK):
			if(grid[row - 1][col].color != BLACK or grid[row][col+1].color != BLACK):
				self.diag_neighbors.append(grid[row - 1][col + 1])	
		if(row != GRIDWIDTH - 1 and col != 0 and grid[row + 1][col - 1].color != BLACK):
			if(grid[row + 1][col].color != BLACK or grid[row][col-1].color != BLACK):
				self.diag_neighbors.append(grid[row + 1][col - 1])	
		if(row != GRIDWIDTH - 1 and col != GRIDWIDTH - 1 and grid[row + 1][col + 1].color != BLACK):
			if(grid[row + 1][col].color != BLACK or grid[row][col+1].color != BLACK):
				self.diag_neighbors.append(grid[row + 1][col + 1])	
		
		
	def __lt__(self, other):
		return False
	def reset(self):
		self.change_color(WHITE)
		self.neighbors = []
		self.diag_neighbor = []
		self.g_score = float("inf")
		self.came_from = None
	def soft_reset(self):
		if(not self.color in (BLACK, BLUE, YELLOW)):
			self.change_color(WHITE)
		self.neighbors = []
		self.diag_neighbors = []
		self.g_score = float("inf")
		self.came_from = None


def make_grid():
	grid = []
	#draws the initial Grid
	for i in range(GRIDWIDTH):
		this_layer = []
		for j in range(GRIDWIDTH):
			new_node = node(i, j, WHITE);
			this_layer.append(new_node)
			new_node.draw();
		grid.append(this_layer)
	return grid
	
def h(node1, node2):
	return math.sqrt(math.pow(node1.x - node2.x, 2) + math.pow(node1.y - node2.y, 2))
	
def draw_path(curr, start):
	if(curr == start):
		return
	curr.change_color(PURPLE)
	pygame.display.update()		
	draw_path(curr.came_from, start)
	
def run_algorithm(start, end):
	open_set = PriorityQueue()
	start.g_score = 0
	open_set.put((h(start, end), 0, start))
	open_set_size = 1
	tick_speed = 60
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_SPACE):
					tick_speed *= 2
		current_node = open_set.get()[2]
		if(current_node == end):
			end.change_color(BLUE)
			draw_path(end.came_from, start)
			return
		else:
			for neighbor in current_node.neighbors:
				if(current_node.g_score + 1 < neighbor.g_score):
					neighbor.change_color(GREEN)
					neighbor.g_score = current_node.g_score + 1
					neighbor.came_from = current_node
					open_set.put((neighbor.g_score + h(neighbor, end), open_set_size, neighbor))
					open_set_size += 1
			for neighbor in current_node.diag_neighbors:
				if(current_node.g_score + math.sqrt(2) < neighbor.g_score):
					neighbor.change_color(GREEN)
					neighbor.g_score = current_node.g_score + math.sqrt(2)
					neighbor.came_from = current_node
					open_set.put((neighbor.g_score + h(neighbor, end), open_set_size, neighbor))
					open_set_size += 1
			if(current_node != start):
				current_node.change_color(RED)
		pygame.display.update()		
		pygame.time.Clock().tick(tick_speed)

			


def main():
	grid = make_grid()
	
	
	
	
	
	start = None
	end = None
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				
			if event.type == pygame.KEYDOWN:
				if (event.key == pygame.K_SPACE and start and end):
					for line in grid:
						for n in line:
							n.update_neighbors(grid)
					run_algorithm(start, end)
				if(event.key == pygame.K_c):
					print("test")
					start = None
					end = None
					for line in grid:
						for n in line:
							n.reset()
	
				if(event.key == pygame.K_r):
					for line in grid:
						for n in line:
							n.soft_reset()
					
		if(pygame.mouse.get_pressed()[0]):
			x = pygame.mouse.get_pos()[0] // NODESIZE
			y = pygame.mouse.get_pos()[1] // NODESIZE
			if(not start and grid[y][x] != end):
				grid[y][x].change_color(YELLOW)
				start = grid[y][x]
			elif(not end and grid[y][x] != start):
				grid[y][x].change_color(BLUE)
				end = grid[y][x]
			elif(start != grid[y][x] and end != grid[y][x]):
				grid[y][x].change_color(BLACK)
		if(pygame.mouse.get_pressed()[2]):
			x = pygame.mouse.get_pos()[0] // NODESIZE
			y = pygame.mouse.get_pos()[1] // NODESIZE
			if(grid[y][x] == start):
				start = None
			elif(grid[y][x] == end):
				end = None
			grid[y][x].reset()
		pygame.time.Clock().tick(60)
		pygame.display.update()		
main()