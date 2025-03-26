import pygame
import sys
import random
import hashlib
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pygame.init()

DATABASE_URL = 'sqlite:///local.db'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "usersap"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    score = Column(Integer, default=0)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    try:
        hashed_pw = hash_password(password)
        new_user = User(username=username, password=hashed_pw)
        session.add(new_user)
        session.commit()
        return True, "Registration successful!"
    except Exception as e:
        session.rollback()
        return False, "Username already exists" if "UNIQUE constraint" in str(e) else "Registration failed"

def login_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.password == hash_password(password):
        return True, "Login successful!", user
    return False, "Invalid username or password", None

def update_user_score(user, new_score):
    if new_score > user.score:
        user.score = new_score
        session.commit()

WHITE = (255, 255, 255)
BLACK = (165, 42, 42)
RED = (255, 0, 0)
GREEN = (210, 105, 30)
BLUE = (0, 0, 255)
BROWN = (105, 105, 105)


WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

gun1_image = pygame.image.load("gun2.png")
gun2_image = pygame.image.load("gun.png")
gun1_image = pygame.transform.scale(gun1_image, (50, 50))
gun2_image = pygame.transform.scale(gun2_image, (50, 50))
background_picture = pygame.image.load("background_picture.jpg")
background_picture = pygame.transform.scale(background_picture, (WIDTH, HEIGHT))
target_image = pygame.image.load("target.png")
target_image = pygame.transform.scale(target_image, (50, 50))
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (60, 60))

batman_music = pygame.mixer.Sound("Titoli.mp3")
gun1_music = pygame.mixer.Sound("gunshot1.mp3")
gun2_music = pygame.mixer.Sound("shotgun2.mp3")

players_shots = []
player1_shot = []
player2_shot = []
targets = []

class Button:
    def __init__(self, text, location, size, text_color, background_color, face_color, ch_state):
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 40)
        self.ch_state = ch_state
        self.location = location
        self.width, self.height = size
        self.background_color = background_color
        self.face_color = face_color
        self.rect1 = pygame.Rect(*location, *size)
        self.rect2 = pygame.Rect(location[0] + 3, location[1] + 3, size[0] - 6, size[1] - 6)

    def normal(self, Surface):
        rect_text = self.font.render(self.text, True, self.text_color)
        pygame.draw.rect(Surface, self.background_color, self.rect1, border_radius=9)
        pygame.draw.rect(Surface, self.face_color, self.rect2, border_radius=9)
        Surface.blit(rect_text, (self.location[0] + (self.width - rect_text.get_width()) / 2,
                                 self.location[1] + (self.height - rect_text.get_height()) // 2))

    def hover(self, Surface):
        rect_text = self.font.render(self.text, True, (210, 105, 30))
        pygame.draw.rect(Surface, (210, 105, 30), self.rect1, border_radius=9)
        pygame.draw.rect(Surface, BLACK, self.rect2, border_radius=9)
        Surface.blit(rect_text, (self.location[0] + (self.width - rect_text.get_width()) / 2,
                                 self.location[1] + (self.height - rect_text.get_height()) // 2))

    def update(self, Surface, pos, state, click=False):
        if self.rect1.collidepoint(pos) and click:
            return self.ch_state
        elif self.rect1.collidepoint(pos):
            self.hover(Surface)
        else:
            self.normal(Surface)
        return state

class RegisterScreen:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.confirm = ""
        self.active_field = None 
        self.message = ""
        self.message_color = BLACK
        self.register_button = Button("Register", (WIDTH//2 - 100, 320), (200, 40), BLACK, BLACK, GREEN, "register")
        self.back_button = Button("Back", (WIDTH//2 - 100, 440), (200, 40),  BLACK, BLACK, GREEN, "back")
        self.running = True

    def run(self):
        while self.running:
            screen.fill(WHITE)
            title = small_font.render("REGISTER", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
            
            fields = [
                ("Username:", self.username, 70),
                ("Password:", "*" * len(self.password), 150),
                ("Confirm Password:", "*" * len(self.confirm), 230)
            ]
            for i, (label, value, y) in enumerate(fields):
                label_surf = small_font.render(label, True, BLACK)
                screen.blit(label_surf, (WIDTH//2 - 150, y - 25))
                color = BLUE if self.active_field == i else BROWN
                pygame.draw.rect(screen, color, (WIDTH//2 - 150, y, 300, 35), 2)
                text_surf = font.render(value, True, BLACK)
                screen.blit(text_surf, (WIDTH//2 - 140, y + 10))
            
            pos = pygame.mouse.get_pos()
            state = None
            state = self.register_button.update(screen, pos, state, click=False)
            state = self.back_button.update(screen, pos, state, click=False)
            
            if self.message:
                message_surf = small_font.render(self.message, True, self.message_color)
                screen.blit(message_surf, (WIDTH//2 - message_surf.get_width()//2, 370))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.register_button.rect1.collidepoint(event.pos):
                        if not self.username or not self.password or not self.confirm:
                            self.message = "All fields are required!"
                            self.message_color = RED
                        elif len(self.username) < 3:
                            self.message = "Username too short (min 3 chars)"
                            self.message_color = RED
                        elif len(self.password) < 4:
                            self.message = "Password too short (min 4 chars)"
                            self.message_color = RED
                        elif self.password != self.confirm:
                            self.message = "Passwords don't match!"
                            self.message_color = RED
                        else:
                            success, msg = register_user(self.username, self.password)
                            self.message = msg
                            self.message_color = GREEN if success else RED
                            if success:
                                pygame.time.delay(1500)
                                return True
                    if self.back_button.rect1.collidepoint(event.pos):
                        return False
                    if WIDTH//2 - 150 <= event.pos[0] <= WIDTH//2 + 150:
                        if 70 <= event.pos[1] <= 105:
                            self.active_field = 0
                        elif 150 <= event.pos[1] <= 185:
                            self.active_field = 1
                        elif 230 <= event.pos[1] <= 265:
                            self.active_field = 2
                        else:
                            self.active_field = None
                if event.type == pygame.KEYDOWN and self.active_field is not None:
                    if event.key == pygame.K_RETURN:
                        if self.active_field < 2:
                            self.active_field += 1
                    elif event.key == pygame.K_BACKSPACE:
                        if self.active_field == 0:
                            self.username = self.username[:-1]
                        elif self.active_field == 1:
                            self.password = self.password[:-1]
                        elif self.active_field == 2:
                            self.confirm = self.confirm[:-1]
                    else:
                        if self.active_field == 0:
                            self.username += event.unicode
                        elif self.active_field == 1:
                            self.password += event.unicode
                        elif self.active_field == 2:
                            self.confirm += event.unicode

class LoginScreen:
    def __init__(self, prompt="LOGIN"):
        self.prompt = prompt
        self.username = ""
        self.password = ""
        self.active_field = None 
        self.message = ""
        self.message_color = BLACK
        self.login_button = Button("Login", (WIDTH//2 - 100, 280), (200, 40), BLACK, BLACK, GREEN, "login")
        self.back_button = Button("Back", (WIDTH//2 - 100, 440), (200, 40), BLACK, BLACK, GREEN, "back")
        self.running = True

    def run(self):
        while self.running:
            screen.fill(WHITE)
            title = small_font.render(self.prompt, True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            fields = [
                ("Username:", self.username, 150),
                ("Password:", "*" * len(self.password), 200)
            ]
            for i, (label, value, y) in enumerate(fields):
                label_surf = small_font.render(label, True, BLACK)
                screen.blit(label_surf, (WIDTH//2 - 150, y - 15))
                color = BLUE if self.active_field == i else BROWN
                pygame.draw.rect(screen, color, (WIDTH//2 - 150, y, 300, 35), 2)
                text_surf = font.render(value, True, BLACK)
                screen.blit(text_surf, (WIDTH//2 - 140, y + 5))
            
            pos = pygame.mouse.get_pos()
            state = None
            state = self.login_button.update(screen, pos, state, click=False)
            state = self.back_button.update(screen, pos, state, click=False)
            
            if self.message:
                message_surf = small_font.render(self.message, True, self.message_color)
                screen.blit(message_surf, (WIDTH//2 - message_surf.get_width()//2, 385))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.login_button.rect1.collidepoint(event.pos):
                        if not self.username or not self.password:
                            self.message = "Username and password required!"
                            self.message_color = RED
                        else:
                            success, msg, user = login_user(self.username, self.password)
                            self.message = msg
                            self.message_color = GREEN if success else RED
                            if success:
                                pygame.time.delay(1500)
                                return True, user, "login"
                    if self.back_button.rect1.collidepoint(event.pos):
                        return False, "back", "back"
                    if WIDTH//2 - 150 <= event.pos[0] <= WIDTH//2 + 150:
                        if 150 <= event.pos[1] <= 185:
                            self.active_field = 0
                        elif 200 <= event.pos[1] <= 235:
                            self.active_field = 1
                        else:
                            self.active_field = None
                if event.type == pygame.KEYDOWN and self.active_field is not None:
                    if event.key == pygame.K_RETURN:
                        if self.active_field == 0:
                            self.active_field = 1
                        else:
                            if not self.username or not self.password:
                                self.message = "Username and password required!"
                                self.message_color = RED
                            else:
                                success, msg, user = login_user(self.username, self.password)
                                self.message = msg
                                self.message_color = GREEN if success else RED
                                if success:
                                    pygame.time.delay(1500)
                                    return True, user, "login"
                    elif event.key == pygame.K_BACKSPACE:
                        if self.active_field == 0:
                            self.username = self.username[:-1]
                        elif self.active_field == 1:
                            self.password = self.password[:-1]
                    else:
                        if self.active_field == 0:
                            self.username += event.unicode
                        elif self.active_field == 1:
                            self.password += event.unicode

def two_player_login():
    login1 = LoginScreen("Login Player 1")
    success1, user1, state = login1.run()
    if state == "back":
        return False, "back", "back"
    elif not success1:
        return False, None, None
    login2 = LoginScreen("Login Player 2")
    success2, user2, state = login2.run()
    if state == "back":
        return False, "back", "back"
    if not success2:
        return False, None, None
    return True, user1, user2

def leaderboard_screen():
    running = True
    while running:
        screen.fill(WHITE)
        title = font.render("Leaderboard", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        users = session.query(User).order_by(User.score.desc()).all()
        y_offset = 70
        for i, user in enumerate(users):
            entry = small_font.render(f"{i+1}. {user.username} - {user.score}", True, BLACK)
            screen.blit(entry, (WIDTH//2 - entry.get_width()//2, y_offset))
            y_offset += 40

        back_button = Button("Back", (WIDTH//2 - 100, HEIGHT-80), (200, 50), WHITE, RED, BLUE, "back")
        pos = pygame.mouse.get_pos()
        state = back_button.update(screen, pos, 0, click=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.rect1.collidepoint(event.pos):
                    running = False

        pygame.display.update()

class Player:
    def __init__(self, kind, position, bullet=10, death=False, score=0, time=120):
        self.kind = kind
        self.death = death
        self.time = time
        self.position = position
        self.score = score
        self.bullet = bullet
        self.start_time = 0
        self.user = None  

    def death_check(self):
        timer = (pygame.time.get_ticks() - self.start_time) // 1000
        self.time = max(120 - timer, 0)
        if self.time == 0:
            self.death = True

class Shot(Player):
    def __init__(self, score, kind, x, y, bullet, show=False):
        super().__init__(score, kind, (x, y), bullet)
        self.x = x
        self.y = y
        self.score = score
        self.show = show
        self.kind = kind

    def visability(self):
        screen.blit(self.kind, (self.x, self.y))

class Target:
    def __init__(self):
        self.target_x = random.randint(30, WIDTH - 30)
        self.target_y = random.randint(30, HEIGHT - 30)
        self.active = True
        self.radius = 25

    def calculate_score(self, shot):
        target_center = (self.target_x + self.radius, self.target_y + self.radius)
        shot_center = (shot.x + 25, shot.y + 25)
        distance = ((target_center[0] - shot_center[0])**2 + (target_center[1] - shot_center[1])**2)**0.5
        score = max(10, 100 - int(distance/10))
        return score

    def draw(self):
        if self.active:
            screen.blit(target_image, (self.target_x, self.target_y))

    def hit(self, shot):
        if self.active:
            target_center = (self.target_x + self.radius, self.target_y + self.radius)
            shot_center = (shot.x + 25, shot.y + 25)
            distance = ((target_center[0] - shot_center[0])**2 + (target_center[1] - shot_center[1])**2)**0.5
            if distance < self.radius + 25:
                self.active = False
                return True
        return False

class Enemy(Target):
    def __init__(self, speed=0.02):
        super().__init__()
        self.choise_target = random.choice(targets)
        self.enemy_x = 0
        self.enemy_y = self.choise_target.target_y
        self.speed = speed
        self.active = True

    def draw(self):
        if self.active:
            screen.blit(enemy_image, (self.enemy_x, self.enemy_y))

    def attack(self):
        if self.active:
            self.enemy_x += self.speed
            if self.enemy_x >= self.choise_target.target_x:
                self.choise_target.active = False
                targets.remove(self.choise_target)
                targets.append(Target())
                self.reset()

    def reset(self):
        self.choise_target = random.choice(targets)
        self.enemy_x = 0
        self.enemy_y = self.choise_target.target_y
        self.active = False

    def activate(self):
        self.active = True

class Bonus(Target):
    def __init__(self, speed=0.02):
        super().__init__()
        self.bonus_y = random.randint(30, HEIGHT - 30)
        self.bonus_x = 0
        self.speed = speed
        self.active = True
        self.radius = 25
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 0), (25, 25), 25)

    def draw(self):
        if self.active:
            screen.blit(self.image, (self.bonus_x, self.bonus_y))

    def move(self):
        if self.active:
            self.bonus_x += self.speed
            if self.bonus_x >= WIDTH:
                self.reset()

    def reset(self):
        self.bonus_y = random.randint(30, HEIGHT - 30)
        self.bonus_x = 0
        self.active = False

    def activate(self):
        self.active = True

    def hit(self, shot):
        if self.active:
            bonus_center = (self.bonus_x + self.radius, self.bonus_y + self.radius)
            shot_center = (shot.x + 25, shot.y + 25)
            distance = ((bonus_center[0] - shot_center[0])**2 + (bonus_center[1] - shot_center[1])**2)**0.5
            if distance < self.radius + 25:
                self.active = False
                return True
        return False

class WinPage:
    def __init__(self, winner):
        self.winner = winner
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.buttons = [
            Button("Main Menu", (300, 350), (200, 60), WHITE, GREEN, BLUE, "menu"),
            Button("Quit", (300, 430), (200, 60), WHITE, RED, BLUE, "quit")
        ]
        self.run()

    def run(self):
        running = True
        while running:
            screen.blit(background_picture, (0, 0))
            if self.winner == "player1":
                winner_text = self.font_large.render("Player 1 Wins!", True, GREEN)
                score_text = self.font_medium.render(f"Score: {player[0].score}", True, WHITE)
            elif self.winner == "player2":
                winner_text = self.font_large.render("Player 2 Wins!", True, GREEN)
                score_text = self.font_medium.render(f"Score: {player[1].score}", True, WHITE)
            else:
                winner_text = self.font_large.render("It's a Tie!", True, GREEN)
                score_text = self.font_medium.render("Tie Game", True, WHITE)
            screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, 150))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 230))

            pos = pygame.mouse.get_pos()
            state = None
            for btn in self.buttons:
                state = btn.update(screen, pos, state, click=False)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.rect1.collidepoint(event.pos):
                            if btn.ch_state == "menu":
                                running = False
                                Game().run()
                            elif btn.ch_state == "quit":
                                pygame.quit()
                                sys.exit()
            pygame.display.update()

class Game:
    def __init__(self):
        pygame.display.set_caption("Shoting")
        self.state = 1  
        self.buttons = [
            Button("Login", (300, 80), (200, 80), BLACK, BLACK, GREEN, 6),
            Button("Register", (300, 170), (200, 80), BLACK, BLACK, GREEN, 5),
            Button("LeaderBoard", (300, 260), (200, 80), BLACK, BLACK, GREEN, 3),
            Button("Quit", (300, 350), (200, 80), BLACK, BLACK, GREEN, 4)
        ]
        self.click = False
        self.running = True
        self.font = pygame.font.Font(None, 28)
        self.run()

    def run(self):
        global player, enemy
        while True:
            screen.blit(background_picture, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = True
                else:
                    self.click = False
            if self.state == 1:
                for btn in self.buttons:
                    batman_music.play()
                    pos = pygame.mouse.get_pos()
                    self.state = btn.update(screen, pos, self.state, self.click)
            elif self.state == 5:
                reg = RegisterScreen()
                result = reg.run()
                self.state = 1
            elif self.state == 6:
                success, user1, user2 = two_player_login()
                if user1 == "back" or user2 == "back":
                    self.state = 1
                if success:
                    player[0].user = user1
                    player[1].user = user2
                    self.state = 2
            elif self.state == 3:
                leaderboard_screen()
                self.state = 1
            elif self.state == 4:
                pygame.quit()
                sys.exit()
            elif self.state == 2:
                batman_music.play()
                player[0].start_time = pygame.time.get_ticks()
                player[1].start_time = pygame.time.get_ticks()
                last_attack_time = pygame.time.get_ticks()
                attack_loop = 30000
                bonus = Bonus()
                bonus_spawn_time = pygame.time.get_ticks()
                bonus_interval = 20000
                while True:
                    screen.fill(BROWN)
                    current_time = pygame.time.get_ticks()
                    while current_time - bonus_spawn_time >= bonus_interval:
                        bonus.activate()
                        bonus_spawn_time = current_time
                    if (player[0].death_check() or player[0].bullet <= 0) and (player[1].death_check() or player[1].bullet <= 0):
                        batman_music.stop()
                        if player[0].user is not None:
                            update_user_score(player[0].user, player[0].score)
                        if player[1].user is not None:
                            update_user_score(player[1].user, player[1].score)
                        if player[0].score > player[1].score:
                            WinPage("player1")
                        elif player[1].score > player[0].score:
                            WinPage("player2")
                        else:
                            WinPage("tie")
                        return
                    if bonus.active:
                        bonus.move()
                        bonus.draw()
                        for shot in players_shots:
                            if bonus.hit(shot):
                                if shot.kind == gun1_image:
                                    player[0].bullet += 10
                                else:
                                    player[1].bullet += 10
                                bonus.reset()
                                break
                    for shot in players_shots:
                        shot.visability()
                    for target in targets:
                        target.draw()
                    enemy.draw()
                    enemy.attack()
                    for shot in players_shots:
                        for target in targets:
                            if target.hit(shot):
                                score = target.calculate_score(shot)
                                if shot.kind == gun1_image:
                                    player[0].score += score
                                elif shot.kind == gun2_image:
                                    player[1].score += score
                                if enemy.choise_target == target:
                                    enemy.reset()
                                targets.remove(target)
                                targets.append(Target())
                    timer_text1 = self.font.render(f"Player 1    time:{player[0].time}  Bullets:{player[0].bullet}  score:{player[0].score}", True, WHITE)
                    screen.blit(timer_text1, (20, 20))
                    timer_text2 = self.font.render(f"Player 2    time:{player[1].time}  Bullets:{player[1].bullet}   score:{player[1].score}", True, WHITE)
                    screen.blit(timer_text2, (20, 50))
                    player[0].death_check()
                    player[1].death_check()
                    pygame.display.update()
                    current_time = pygame.time.get_ticks()
                    while current_time - last_attack_time >= attack_loop:
                        enemy.activate()
                        last_attack_time = current_time
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            gun1_player = player[0]
                            gun2_player = player[1]
                            if event.key == pygame.K_ESCAPE:
                                self.running = False
                            if event.key == pygame.K_RETURN:
                                if gun1_player.bullet > 0:
                                    batman_music.stop()
                                    gun1_music.play()
                                    gun1_player.bullet -= 1
                                    shot_obj = Shot(gun1_player.score, gun1_player.kind, gun1_player.position[0], gun1_player.position[1], gun1_player.bullet, show=True)
                                    players_shots.append(shot_obj)
                                    player1_shot.append((gun1_player.position[0], gun1_player.position[1]))
                            if event.key == pygame.K_SPACE:
                                if gun2_player.bullet > 0:
                                    batman_music.stop()
                                    gun2_music.play()
                                    gun2_player.bullet -= 1
                                    shot_obj = Shot(gun2_player.score, gun2_player.kind, gun2_player.position[0], gun2_player.position[1], gun2_player.bullet, show=True)
                                    players_shots.append(shot_obj)
                                    player2_shot.append((gun2_player.position[0], gun2_player.position[1]))
                            elif event.key == pygame.K_w:
                                gun1_player.position = (gun1_player.position[0], gun1_player.position[1] - 10)
                            elif event.key == pygame.K_d:
                                gun1_player.position = (gun1_player.position[0] + 10, gun1_player.position[1])
                            elif event.key == pygame.K_a:
                                gun1_player.position = (gun1_player.position[0] - 10, gun1_player.position[1])
                            elif event.key == pygame.K_s:
                                gun1_player.position = (gun1_player.position[0], gun1_player.position[1] + 10)
                            elif event.key == pygame.K_i:
                                gun2_player.position = (gun2_player.position[0], gun2_player.position[1] - 10)
                            elif event.key == pygame.K_l:
                                gun2_player.position = (gun2_player.position[0] + 10, gun2_player.position[1])
                            elif event.key == pygame.K_j:
                                gun2_player.position = (gun2_player.position[0] - 10, gun2_player.position[1])
                            elif event.key == pygame.K_k:
                                gun2_player.position = (gun2_player.position[0], gun2_player.position[1] + 10)
                        if event.type == pygame.QUIT:
                            self.running = False
                            pygame.quit()
                            sys.exit()
            pygame.display.update()

player = [
    Player(gun1_image, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))),
    Player(gun2_image, (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
]
for _ in range(3):
    targets.append(Target())
enemy = Enemy()
Game()

while len(targets) > 3:
    targets.pop()
    enemy.reset()

