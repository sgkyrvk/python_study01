import pygame

#屏幕大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

#颜色
COLOR_GREY = (150,150,150)
COLOR_WHITE = (255,255,255)
COLOR_BLUE = (0,0,200)
COLOR_RED = (255,0,0)

#网格大小
BLOCK_SIZE = 20

#移动方向字典
DIRECTION_LIST = {
    pygame.K_w:(0,-BLOCK_SIZE),
    pygame.K_s:(0,BLOCK_SIZE),
    pygame.K_a:(-BLOCK_SIZE,0),
    pygame.K_d:(BLOCK_SIZE,0),
}

#方向元组
LR = (pygame.K_a,pygame.K_d)
UD = (pygame.K_w,pygame.K_s)

#旋转方向字典
HEAD_DICT = {
    pygame.K_w:180,
    pygame.K_s:0,
    pygame.K_a:270,
    pygame.K_d:90,
}
