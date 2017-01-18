# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 10:51:34 2017

@author: vxcode
"""

import os
import time
import pygame
import numpy as np

from pygame.locals import *

CEIL_LEN = 40

WHITE   = np.array((255, 255, 255))
BLACK   = np.array((0, 0, 0))
RED     = np.array((255, 0, 0))
GREEN   = np.array((0, 255, 0))
BLUE    = np.array((0, 0, 255))
CYAN    = np.array((0, 255, 255))
PURPLE  = np.array((128, 0, 128))
YELLOW  = np.array((255, 255, 0))
ORANGE  = np.array((255, 128, 0))
SILVERY = WHITE / 2


GAME_LAYOUT = np.array((
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
))

SCREEN_HEIGHT, SCREEN_WIDTH = GAME_LAYOUT.shape[0]*CEIL_LEN, GAME_LAYOUT.shape[1]*CEIL_LEN
PLAY_REGION_START = 1
PLAY_REGION_WIDTH = 10
PLAY_REGION_END = PLAY_REGION_START + PLAY_REGION_WIDTH

def loadPng(name):
    fullname = os.path.join('Resource', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

    except pygame.error as message:
        print("Cannot load image.", fullname)
        raise SystemExit(message)

    return image, image.get_rect()

class Element():

    def __init__(self, panel_info, pos):
        self.size = len(self.data)
        self.real_data = self.data.sum()
        self.panel_info = panel_info
        self.pos = pos

    def leftMove(self):
        self.pos[1] -= 1
        
        if not self.panel_info.checkElement(self):
            self.pos[1] += 1

    def rightMove(self):
        self.pos[1] += 1

        if not self.panel_info.checkElement(self):
            self.pos[1] -= 1

    def rotate(self):
        
        self.old = self.data

        self.data = np.rot90(self.data)
        for index in range(self.size):
            if sum(self.data[:,index]) != 0:
                break
        self.data = np.hstack((self.data[:, index:], self.data[:,:index]))

        if not self.panel_info.checkElement(self):
            self.data = self.old

    def down(self):
        self.pos[0] += 1

        if not self.panel_info.checkElement(self):
            self.pos[0] -= 1
            self.panel_info.addElement(self)
            return False
        else:
            return True

    def draw(self):
        self.panel_info.drawElement(self)

class IElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((1,1,1,1), 
                              (0,0,0,0), 
                              (0,0,0,0), 
                              (0,0,0,0)))
        self.block = panel_info.CYAN_BLOCK
        super().__init__(panel_info, pos)

class JElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((1,1,1), 
                              (0,0,1), 
                              (0,0,0)))
        self.block = panel_info.BLUE_BLOCK
        super().__init__(panel_info, pos)

class LElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((0,0,1), 
                              (1,1,1), 
                              (0,0,0)))
        self.block = panel_info.ORANGE_BLOCK
        super().__init__(panel_info, pos)

class OElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((1,1,0), 
                              (1,1,0), 
                              (0,0,0)))
        self.block = panel_info.YELLOW_BLOCK
        super().__init__(panel_info, pos)

    def rotate(self):
        pass

class SElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((0,1,1), 
                              (1,1,0), 
                              (0,0,0)))
        self.block = panel_info.GREEN_BLOCK
        super().__init__(panel_info, pos)

class TElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((1,1,1), 
                              (0,1,0), 
                              (0,0,0)))
        self.block = panel_info.PURPLE_BLOCK
        super().__init__(panel_info, pos)

class ZElement(Element):
    def __init__(self, panel_info, pos):
        self.data = np.array(((1,1,0), 
                              (0,1,1), 
                              (0,0,0)))
        self.block = panel_info.RED_BLOCK
        super().__init__(panel_info, pos)

class ShowPanel():

    NumberImage = {}

    def __init__(self, screen, pos):
        self.initResource()

        self.data = 0
        self.pos = pos
        self.screen = screen

    def initResource(self):

        if len(self.NumberImage): 
            return

        for i in range(10):
            self.NumberImage[i], _= loadPng('{0}.png'.format(i))
            self.NumberImage[i] = pygame.transform.scale(self.NumberImage[i], (CEIL_LEN, CEIL_LEN))
        
    def addInfo(self, data):
        self.data += datqa
        self.updateInfo()

    def setInfo(self, data):
        self.data = data
        self.updateInfo()

    def updateInfo(self):

        temp = self.data
        nums = []

        if temp > 0:
            while temp > 0:
                nums.append(temp%10)
                temp //= 10
        else:
            nums.append(0)

        surface = pygame.Surface((len(nums)*CEIL_LEN, CEIL_LEN)).convert()

        [surface.blit(self.NumberImage[num], (index*CEIL_LEN, 0)) for index, num in enumerate(nums[::-1])]

        temp_pos = self.pos.copy()
        temp_pos[1] = temp_pos[1]+4-len(nums)
        self.screen.blit(surface, switchPos(temp_pos))

def switchPos(pos):
    """将矩阵坐标转换为绘图坐标"""
    return pos[::-1]*CEIL_LEN

class Score(ShowPanel):

    Row2Score = [0, 1, 4, 8, 16]

    def __init__(self, screen, pos):
        super().__init__(screen, pos)
        
    def addInfo(self, data):
        self.data += self.Row2Score[data]
        self.updateInfo()    

class TetrisPanel():

    Element_Dict = {
        0:IElement, 1:JElement, 2:LElement,
        3:OElement, 4:SElement, 5:TElement,
        6:ZElement,
    }
    Element_Num = len(Element_Dict)

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.initBlock()

        self.score = Score(self.screen, np.array((6, 13)))
        self.level = ShowPanel(self.screen, np.array((8, 13)))

        self.clear_regions = []

        self.next_block = None
        self.next_clear_regions = []
        
    def genBlock(self, color):
        block = pygame.Surface((CEIL_LEN, CEIL_LEN)).convert()
        self.drawBaiscBlock(block, color, np.zeros(2), CEIL_LEN)
        return block

    def initBlock(self):
        self.RED_BLOCK = self.genBlock(RED)
        self.GREEN_BLOCK = self.genBlock(GREEN)
        self.BLUE_BLOCK = self.genBlock(BLUE)
        self.CYAN_BLOCK = self.genBlock(CYAN)
        self.PURPLE_BLOCK = self.genBlock(PURPLE)
        self.YELLOW_BLOCK = self.genBlock(YELLOW)
        self.ORANGE_BLOCK = self.genBlock(ORANGE)
        self.SILVERY_BLOCK = self.genBlock(SILVERY)

        self.ground_block = pygame.Surface((CEIL_LEN, CEIL_LEN)).convert()
        self.ground_block.fill(BLACK)

    def drawBaiscBlock(self, surface, color, pos, width):
        factor = 0.2*CEIL_LEN
        outRect = pygame.Rect(pos, (width,)*2)
        inRect = pygame.Rect(pos+factor, (width-2*factor,)*2)

        pygame.draw.rect(surface, color, outRect)
        pygame.draw.rect(surface, color/1.2, inRect)
        pygame.draw.polygon(surface, color/1.5, [outRect.topleft, inRect.topleft, inRect.bottomleft, outRect.bottomleft])
        pygame.draw.polygon(surface, color/3, [outRect.topright, inRect.topright, inRect.bottomright, outRect.bottomright])
        pygame.draw.polygon(surface, color/2, [outRect.bottomleft, inRect.bottomleft, inRect.bottomright, outRect.bottomright])

    def initBackGround(self):
        background = pygame.Surface(self.screen.get_size()).convert()
        background.fill(BLACK)

        for row in range(0, SCREEN_HEIGHT//CEIL_LEN):
            for col in range(0, SCREEN_WIDTH//CEIL_LEN):
                if GAME_LAYOUT[row][col] == 1:
                    background.blit(self.SILVERY_BLOCK, switchPos(np.array((row,col))))

        self.screen.blit(background, (0,0))

    def genElement(self):
        return self.Element_Dict[np.random.randint(self.Element_Num)](self, np.array([1, 3]))

    def getNewElement(self):
            
            now_block = self.next_block if self.next_block != None else self.genElement()

            if self.checkElement(now_block):
                self.next_block = self.genElement()
                self.next_clear_regions = self._drawElement(self.next_block, self.next_clear_regions, pos=np.array((1,13)))
                return now_block
            else:
                #game over
                return None

    def checkElement(self, element):
        iter_count = 0
        for row in range(element.size):
            for col in range(element.size):
                if element.data[row][col] == 0:
                    continue

                if GAME_LAYOUT[element.pos[0]+row][element.pos[1]+col] == 1:
                    return False

                iter_count += 1
                if iter_count == element.real_data:
                    return True

    def showBlink(self, row):
        surface_black = pygame.Surface((CEIL_LEN*PLAY_REGION_WIDTH, CEIL_LEN)).convert()
        surface_black.fill(BLACK)
        surface_old = pygame.Surface((CEIL_LEN*PLAY_REGION_WIDTH, CEIL_LEN)).convert()
        surface_old.blit(self.screen, (0,0), area=(CEIL_LEN, row*CEIL_LEN , PLAY_REGION_WIDTH*CEIL_LEN, CEIL_LEN))

        showTime = 4
        while showTime > 0:
            showTime -= 1
            self.screen.blit(surface_black, (CEIL_LEN, row*CEIL_LEN)) if (showTime & 1) else self.screen.blit(surface_old, (CEIL_LEN, row*CEIL_LEN))
            self.gameDraw()
            time.sleep(0.25)

    def addElement(self, element):
        iter_count = 0
        add_row = set()

        self.clear_regions = []

        #将方块数据加入游戏面板
        for row in range(element.size):
            for col in range(element.size):
                if element.data[row][col] == 1:
                    GAME_LAYOUT[element.pos[0]+row][element.pos[1]+col] = 1
                    iter_count += 1
                    add_row.add(element.pos[0]+row)

            if iter_count == element.real_data:
                break

        #计算可消除的行
        complete_row = []
        for row in add_row:
            total = GAME_LAYOUT[row][PLAY_REGION_START: PLAY_REGION_END].sum()
            if total == PLAY_REGION_WIDTH:
                complete_row.append(row)

        if len(complete_row) == 0:
            return

        #添加积分
        self.score.addInfo(len(complete_row))
        self.level.setInfo(self.score.data//100+1)

        #消除已完成的行
        complete_row.sort()
        for row in complete_row:
            self.showBlink(row)
            #更新游戏界面
            move_region = pygame.Rect(CEIL_LEN, CEIL_LEN, PLAY_REGION_WIDTH*CEIL_LEN, (row-1)*CEIL_LEN)
            self.screen.blit(self.screen, (move_region.left, move_region.top+CEIL_LEN), area=move_region)   
            #更新后台数据
            GAME_LAYOUT[2:row+1, PLAY_REGION_START:PLAY_REGION_END] = GAME_LAYOUT[1:row, PLAY_REGION_START: PLAY_REGION_END]
            GAME_LAYOUT[1, PLAY_REGION_START: PLAY_REGION_END] = 0

    def _drawElement(self, element, clear_regions, pos=None):
        [self.screen.blit(self.ground_block, clear_region) for clear_region in clear_regions]

        iter_count = 0
        new_clear_regions = []
        pos = element.pos if(pos is None) else pos
        for row in range(element.size):
            for col in range(element.size):
                if element.data[row][col] == 0: 
                    continue

                draw_regions = np.array(switchPos(pos)+switchPos(np.array((row,col))))
                self.screen.blit(element.block, draw_regions)
                new_clear_regions.append(draw_regions)

                iter_count += 1
                if iter_count == element.real_data:
                    return new_clear_regions

    def drawElement(self, element):
        self.clear_regions = self._drawElement(element, self.clear_regions)

    def gameDraw(self):
        pygame.display.flip()

    def gameOver(self):
        pass

def main():
    pygame.init()
    clock = pygame.time.Clock()

    panel = TetrisPanel()
    panel.initBackGround()
    panel.score.updateInfo()
    panel.level.setInfo(1)
    panel.level.updateInfo()
    panel.gameDraw()

    element = panel.getNewElement()

    game_frame = 99
    game_count = 0
    game_rate = game_frame - panel.level.data

    KeyDelay = -1
    DownKey = None
    HandleKey = None
    KeyMapFunc = {
        K_UP: Element.rotate,
        K_RIGHT: Element.rightMove,
        K_LEFT: Element.leftMove,
    }

    while True:
        game_count += 1

        if KeyDelay >= 0:
            if KeyDelay == 0 :
                DownKey = HandleKey
            else:
                KeyDelay -= 1

        element.draw()
        panel.gameDraw()

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    game_rate = 0

                elif event.key == K_ESCAPE:
                    return

                elif(event.key in {K_UP, K_RIGHT, K_LEFT}):
                    DownKey = event.key
                    HandleKey = DownKey
                    KeyDelay = 10
                    
            elif event.type == KEYUP:
                DownKey = None
                HandleKey = None
                KeyDelay = -1

                if event.key == K_DOWN:
                    game_rate = game_frame - panel.level.data

        if DownKey:
            KeyMapFunc[DownKey](element)
            DownKey = None

        if game_count >= game_rate:
            game_count = 0
            if element.down() == False:
                element = panel.getNewElement()
                if element is None:
                    break

                game_rate = game_frame - panel.level.data

        clock.tick(game_frame)

    panel.gameOver()

if __name__ == "__main__":
    main()