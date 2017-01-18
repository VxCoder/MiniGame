import pygame
import numpy as np
from pygame.locals import *
from scipy import ndimage

WORLD_SIZE = None
FACTOR = 10
WEIGHTS = np.array([[1,1,1], [1,10,1], [1,1,1]])
CLICK_SIZE = 50
FRAME = 180

def world_rand_init(size):
	return (np.random.randint(0, FACTOR, size) < 1).astype(int)

def world_init(size):

	return np.zeros(size)

def next_world(world, weight):
	states = ndimage.convolve(world, weight, mode='wrap')
	results = (states==13) | (states==12) | (states==3)
	return results.astype(int)

def set_cmd_flag(cmd_flag, cmd):
	#cmd_flag = {cmd_key : False for cmd_key in cmd_flag }
	cmd_flag[cmd] = not cmd_flag[cmd]

def main():
	global WORLD_SIZE

	pygame.init()
	clock = pygame.time.Clock()
	pygame.display.set_mode((0,0), pygame.FULLSCREEN)

	world_surface = pygame.display.get_surface()
	WORLD_SIZE = world_surface.get_size()
	world_data = world_init(WORLD_SIZE)

	RunFlag = False
	LineFlag = False
	MouseDown = False
	CMD_FLAG = {
		ord('l'): False
	}

	while True:
		if RunFlag:
			world_data = next_world(world_data, WEIGHTS)

		pygame.surfarray.blit_array(world_surface, world_data*(256**3-1))
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN:
				MouseDown = True
				pos = pygame.mouse.get_pos()
				world_data[pos[0]-CLICK_SIZE:pos[0]+CLICK_SIZE , pos[1]-CLICK_SIZE:pos[1]+CLICK_SIZE] = 1

			elif event.type == MOUSEBUTTONUP:
				MouseDown = False

			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					return
				elif event.key == ord('r'):
					world_data = world_rand_init(WORLD_SIZE)
				elif event.key == ord('c'):
					world_data[:,:] = 0
				elif event.key == ord('s'):
					RunFlag = not RunFlag
				elif event.key == ord('l'):
					world_data[pos[0]-CLICK_SIZE: pos[0]+CLICK_SIZE, pos[1]] = 1
				elif event.key == ord('v'):
					world_data[pos[0], pos[1]-CLICK_SIZE: pos[1]+CLICK_SIZE] = 1
				elif event.key == ord('x'):
					world_data[pos[0]-CLICK_SIZE: pos[0]+CLICK_SIZE, pos[1]] = 1
					world_data[pos[0], pos[1]-CLICK_SIZE: pos[1]+CLICK_SIZE] = 1
				elif event.key == ord('a'):
					world_data[pos[0]-CLICK_SIZE: pos[0]+CLICK_SIZE: 1, pos[1]] = 1

		pos = pygame.mouse.get_pos()
		if MouseDown:
			world_data[pos[0] , pos[1]] = 1


		clock.tick(FRAME)

if __name__ == "__main__":
	main()