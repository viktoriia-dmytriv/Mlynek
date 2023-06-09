import pygame

WIDTH = 352*3//2 + 8
HEIGHT = 352
BOARD_WIDTH = 456
BOARD_HEIGHT = 352
PLAYER_COLORS = [None, (255, 0, 0), (0, 0, 255)]
CHIP_IMAGES = [None, pygame.image.load("resources\white.png"), pygame.image.load("resources\\black.png")]
CHIP_SPRITE_POS = [None, (96, 0), (64, 0)]
SUPERCHIP_SPRITE_POS = [None, (32, 0), (0, 0)]
CHIP_RADIUS = 16

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

_FIRST_LAYER = 48
_SECOND_LAYER = 96
_THIRD_LAYER = 144

CHIP_POSITIONS = [
    [(_FIRST_LAYER, 0), (_SECOND_LAYER, 0), (_THIRD_LAYER, 0)],
    [(_FIRST_LAYER, _FIRST_LAYER), (_SECOND_LAYER, _SECOND_LAYER), (_THIRD_LAYER, _THIRD_LAYER)],
    [(0, _FIRST_LAYER), (0, _SECOND_LAYER), (0, _THIRD_LAYER)],
    [(-_FIRST_LAYER, _FIRST_LAYER), (-_SECOND_LAYER, _SECOND_LAYER), (-_THIRD_LAYER, _THIRD_LAYER)],
    [(-_FIRST_LAYER, 0), (-_SECOND_LAYER, 0), (-_THIRD_LAYER, 0)],
    [(-_FIRST_LAYER, -_FIRST_LAYER), (-_SECOND_LAYER, -_SECOND_LAYER), (-_THIRD_LAYER, -_THIRD_LAYER)],
    [(0, -_FIRST_LAYER), (0, -_SECOND_LAYER), (0, -_THIRD_LAYER)],
    [(_FIRST_LAYER, -_FIRST_LAYER), (_SECOND_LAYER, -_SECOND_LAYER), (_THIRD_LAYER, -_THIRD_LAYER)]
]

_REMAINING_LAYERS =[
    4*32,
    3*32,
    2*32,
    1*32,
    0*32,
    -1*32,
    -2*32,
    -3*32,
    -4*32,
]
_REMAINING_X = [-198, 198]
REMAINING_CHIPS_POSITIONS = [
    [],
    [(_REMAINING_X[0], _REMAINING_LAYERS[i]) for i in range(0, 9)],
    [(_REMAINING_X[1], _REMAINING_LAYERS[i]) for i in range(0, 9)],
]

BUTTONS_POSITIONS = [
    None,
    (-248, 0),
    (248, 0),
]

BUTTON_SPRITE_POS = [
    None,
    [(32, 0), (96, 0)],
    [(0, 0), (64, 0)],
]

BUTTON_RADIUS = 16