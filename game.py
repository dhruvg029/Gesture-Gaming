import pygame, sys
import random
import cv2
import numpy as np
from gesture import gest

class game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen_w = 1280
        self.screen_h = 960

        self.screen = pygame.display.set_mode((self.screen_w,self.screen_h))
        pygame.display.set_caption(("Save the Farm"))
        
        self.bg_color = pygame.Color((0,200,0))
        self.insects = set()
        self.time = 0
        self.banner = pygame.Rect(0,0,1280,50)
        #self.best_score = 0
        self.score = 0
        self.bug = pygame.image.load('bug.png')
        self.bug = pygame.transform.scale(self.bug, (150,150))
        self.speed = 7
        self.ad = 80
        self.add = set()
        self.remove = set()
        self.boom = pygame.image.load('boom.png')
        self.boom = pygame.transform.scale(self.boom, (150,150))
        self.cross = pygame.image.load('cross.png')
        self.cross = pygame.transform.scale(self.cross, (100,100))

        self.cross_x = -100
        self.cross_y = -100

        self.cam= cv2.VideoCapture(0)

        self.pinchFlag=0
        self.game = True
        self.run()

    class insect:
        def __init__(self,speed):
            self.object = pygame.Rect(random.randint(100,1100),-50,150,150)
            self.speed = speed

    def destroy(self):
        x = self.cross_x
        y = self.cross_y
        self.screen.blit(self.boom,pygame.Rect(x-75,y-75,150,150))
        for i in self.insects:
            cx = i.object.x + 75
            cy = i.object.y + 75
            if abs(cy-y)<150 and abs(cx-x)<150:
                self.remove.add(i)
                self.score = self.score + 100
                #self.best_score = max(self.score , self.best_score)
    
    def frame(self):

        font = pygame.font.SysFont(None, 40)
        score_img = font.render('Score: '+str(self.score), True, 'white')
        font = pygame.font.SysFont(None, 40)
        #best_score_img = font.render('Best Score: '+str(self.best_score), True, 'white')

        self.remove.clear()
        self.add.clear()

        temp = gest(self.cam)

        if self.time%int(self.ad) == 0:
            self.ad = ((self.ad*(self.ad + 199) + 20)/(self.ad +200))
            self.add.add(self.insect(self.speed))
            self.speed = ((self.speed*self.speed + 100*self.speed)/(self.speed + 99))

        for i in self.insects:
            self.screen.blit(self.bug,i.object)
            i.object.y = i.object.y + i.speed
            if i.object.y > 900:
                self.game = False

        if temp[2]==0:
            self.cross_x = temp[0]*(1280/400)
            self.cross_y = temp[1]*(960/300)
        else:
            self.destroy()

        self.screen.blit(self.cross,pygame.Rect(self.cross_x-50,self.cross_y-50,100,100))

        for i in self.remove:
            self.insects.remove(i)
        
        for i in self.add:
            self.insects.add(i)

        pygame.draw.rect(self.screen,(0,150,0),self.banner)
        self.screen.blit(score_img, (1000, 10))
        #self.screen.blit(best_score_img, (50, 10))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill(self.bg_color)
            if self.game:
                self.frame()
            else:
                cv2.destroyAllWindows()
                font = pygame.font.SysFont(None, 200)
                game_over_img = font.render('Game Over', True, 'Red')
                font = pygame.font.SysFont(None, 100)
                score_fin_img = font.render('Your Score: '+str(self.score), True, 'Orange')
                self.screen.blit(game_over_img,(260,400))
                self.screen.blit(score_fin_img,(380,550))
                self.screen.blit(self.bug,pygame.Rect(200,200,150,150))
                self.screen.blit(self.bug,pygame.Rect(700,300,150,150))
                self.screen.blit(self.bug,pygame.Rect(900,50,150,150))
                self.screen.blit(self.bug,pygame.Rect(100,800,150,150))
                self.screen.blit(self.bug,pygame.Rect(800,600,150,150))
                self.screen.blit(self.bug,pygame.Rect(300,700,150,150))
                self.screen.blit(self.bug,pygame.Rect(1000,800,150,150))

            pygame.display.flip()
            self.time = self.time + 1
            self.clock.tick(60)

g = game()
