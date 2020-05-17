from pygame import image
import os

dirname = os.path.dirname(__file__)

BOX_IMAGE = image.load(os.path.join(dirname, 'images\\box.png'))
FREE_CELL_IMAGE = image.load(os.path.join(dirname, 'images\\free_cell.png'))
PLAYER_IMAGE_UP = image.load(os.path.join(dirname, 'images\\player_up.png'))
PLAYER_IMAGE_LEFT = image.load(os.path.join(dirname, 'images\\player_left.png'))
PLAYER_IMAGE_RIGHT = image.load(os.path.join(dirname, 'images\\player_right.png'))
PLAYER_IMAGE_DOWN = image.load(os.path.join(dirname, 'images\\player.png'))
BOX_CELL_IMAGE = image.load(os.path.join(dirname, 'images\\box_cell.png'))
WALL_IMAGE = image.load(os.path.join(dirname, 'images\\wall.png'))
