import pygame
import sys
import random
WHITE = (255, 255, 255)
BLACK = (165, 42, 42)
RED = (255, 0, 0)
GREEN = (210, 105, 30)
BLUE = (0, 0, 255)
BROWN = (105, 105, 105)

from pygame.locals import (
    K_w,
    K_s,
    K_a,
    K_d,
    K_i,
    K_k,
    K_j,
    K_l,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 500

gun1_image = pygame.image.load("gun2.png")
gun2_image=pygame.image.load("gun.png")
gun1_image = pygame.transform.scale(gun1_image, (50, 50))
gun2_image=pygame.transform.scale(gun2_image,(50,50))
background_picture=pygame.image.load("background_picture.jpg")
background_picture= pygame.transform.scale(background_picture, (800,500))
target_image=pygame.image.load("target.png")
target_image = pygame.transform.scale(target_image, (50, 50))

players_shots=[]
player1_shot=[]
player2_shot=[]                                                                                              
targets=[]

screen= pygame.display.set_mode((800,500))

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Shoting")
        self.state=1
        self.buttons= self.main_menu()
        self.click=False
        self.running=True
        self.font=pygame.font.Font(None,28)
        self.run()
    def main_menu(self):
        buttons=[Button("New Game",(300,80),(200,80),BLACK,BLACK,GREEN,2),
                 Button("LeaderBoard",(300,170),(200,80),BLACK,BLACK,GREEN,3),
                 Button("Quit",(300,260),(200,80),BLACK,BLACK,GREEN,4)]
        return buttons
    def run(self):
        while True:
            screen.blit(background_picture, (0, 0))
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONUP:
                    self.click=True
                else:
                    self.click=False
            if self.state==1:
                for button in self.buttons:
                    pos=pygame.mouse.get_pos()
                    self.state=button.update(screen,pos,self.state,self.click)
            elif self.state==2:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                self.running = False
                        if event.type == QUIT:
                            self.running=False
                            pygame.quit()
                            sys.exit()
            elif self.state==4:
                pygame.quit()
                sys.exit()
            pygame.display.update()
class Button:
    def __init__(self,text,location,size,text_color,background_color,face_color,ch_state):
        self.text=text
        self.text_color=text_color
        self.font=pygame.font.Font(None,40)
        self.rect_text=self.font.render(text,True,text_color)
        self.ch_state=ch_state
        self.location=location
        self.width,self.height=size
        self.text_color=text_color
        self.background_color=background_color
        self.face_color=face_color
        self.rect1=pygame.Rect(*location,*size)
        self.rect2=pygame.Rect(*[i+3 for i in location],*[i-6 for i in size])
    def normal(self,Surface):
        self.rect_text=self.font.render(self.text,True,self.text_color)
        pygame.draw.rect(Surface,self.background_color,self.rect1,border_radius=9)
        pygame.draw.rect(Surface,self.face_color,self.rect2,border_radius=9)
        Surface.blit(self.rect_text,(self.location[0]+(self.width-self.rect_text.get_width())/2,
                                     self.location[1]+(self.height-self.rect_text.get_height())//2))

    def hover(self,Surface):
        self.rect_text=self.font.render(self.text,True,(210, 105, 30))
        pygame.draw.rect(Surface,(210, 105, 30),self.rect1,border_radius=9)
        pygame.draw.rect(Surface,BLACK,self.rect2,border_radius=9)
        Surface.blit(self.rect_text,(self.location[0]+(self.width-self.rect_text.get_width())/2,
                                     self.location[1]+(self.height-self.rect_text.get_height())//2))
    def update(self,Surface,pos,statue,click=False):
        if self.rect1.collidepoint(pos) and click:
            return self.ch_state

        elif self.rect1.collidepoint(pos):
            self.hover(Surface)
        else:
            self.normal(Surface)
        return statue
new_game=Game()
