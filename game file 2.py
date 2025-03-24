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
                while True:
                    screen.fill(BROWN)
                    timer_text1=self.font.render(f"Player 1    time:{player[0].time}  Bullets:{player[0].bullet}  score:{player[0].score}",True,WHITE)
                    screen.blit(timer_text1,(20,20))
                    timer_text2=self.font.render(f"Player 2    time:{player[1].time}  Bullets:{player[1].bullet}   score:{player[1].score}",True,WHITE)
                    screen.blit(timer_text2,(20,50))
    
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            gun1_player=player[0]
                            gun2_player=player[1]
                            if event.key == K_ESCAPE:
                                self.running = False                             
                            elif event.key== K_w:
                                gun1_player.position=(gun1_player.position[0],gun1_player.position[1]-10)
                            elif event.key== K_d:
                                gun1_player.position=(gun1_player.position[0]+10,gun1_player.position[1])
                            elif event.key == K_a:
                                gun1_player.position=(gun1_player.position[0]-10,gun1_player.position[1])
                            elif event.key== K_s:
                                gun1_player.position=(gun1_player.position[0],gun1_player.position[1]+10)
                            #Second palyer commands
                            elif event.key== K_i:
                                gun2_player.position=(gun2_player.position[0],gun2_player.position[1]-10)
                            elif event.key== K_l:
                                gun2_player.position=(gun2_player.position[0]+10,gun2_player.position[1])
                            elif event.key == K_j:
                                gun2_player.position=(gun2_player.position[0]-10,gun2_player.position[1])
                            elif event.key== K_k:
                                gun2_player.position=(gun2_player.position[0],gun2_player.position[1]+10)
                        if event.type == QUIT:
                            self.running=False
                            pygame.quit()
                            sys.exit()
            elif self.state==4:
                pygame.quit()
                sys.exit()
            pygame.display.update()
class Player():
    def __init__(self,kind,position,bullet=10,death=False,score=0,time=120):
        self.kind=kind
        self.death=death
        self.time=time
        self.position=position
        self.score=score
        self.bullet=bullet
        self.start_time=0
    def death_check(self):
        timer=(pygame.time.get_ticks()-self.start_time)//1000 
        self.time=max(120-timer,0)
        if self.time==0:
            self.death=True
player=[Player(gun1_image,(random.randint(50,WIDTH-50),random.randint(50,HEIGHT-50))),
        Player(gun2_image,(random.randint(50,WIDTH-50),random.randint(50,HEIGHT-50)))]

class Target(Player):
    def __init__(self):
        self.target_x = random.randint(30, WIDTH - 30)
        self.target_y = random.randint(30, HEIGHT - 30)
        self.active = True
        self.score=0 
    def calculate_score(self,kind):
            if kind==gun1_image:
                shotx,shoty=player1_shot[-2]
                return (abs(self.target_x - shotx ) // 10 )  +  (abs(self.target_y - shoty ) // 10)
            if kind==gun2_image:
                shotx,shoty=player2_shot[-2]
                return (abs(self.target_x - shotx ) // 10 )  +  (abs(self.target_y - shoty ) // 10)


    def draw(self):
        if self.active:

            screen.blit(target_image, (self.target_x, self.target_y))


    def hit(self,shot):
        if self.active and abs(self.target_x - shot.x) < 25 and abs(self.target_y - shot.y) < 25:
            self.active = False
            return True
        return False
    

    def new(self):
        targets.append(Target())
        return Target()
    
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
    
for _ in range(3):
    targets.append(Target())
new_game=Game()
