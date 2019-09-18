import sys, pygame, random, math
from pygame.locals import *

pygame.init()

# Global
HEIGHT = 1280 #Height and Width are reversed but
WIDTH = 720   #my code is too far deep now for changes...
left_boundary = -(HEIGHT/2)
right_boundary = (HEIGHT/2)
top_boundary = -(WIDTH/2)
bottom_boundary = (WIDTH/2)
window_surface = pygame.display.set_mode((HEIGHT, WIDTH))
fps = 120
font_size = 60
basicFont = pygame.font.SysFont(None, font_size)
text = basicFont.render(('Hello World'), True, (255, 255, 255), (0, 0, 0))
xlist = [-5, 5]
ylist = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]

class pong:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PURPLE = (80, 0, 255)
    YELLOW = (255, 255, 0)
    player_score, computer_score = 0, 0
    p_games_won, c_games_won = 0, 0
    start, won, pwon, cwon = False, False, False, False
    winner = "EMPTY"
    start_button, exit_button, replay_button = False, False, False

    #Ball
    x, y = 0, 0
    radius = 10
    diameter = 30
    angle = 360 * random.choice([-10, -9, -8, -7, -6, -5, -4, -3, -2, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    speedx = 2 * math.sin(angle)
    speedy = 2 * math.cos(angle)

    #Paddle
    p_HEIGHT = 200
    p_WIDTH = 10
    p_x, p_y, c_x, c_y = 0, 0, 0, 0 #Player/Computer Paddle (X, Y)
    p_speed, c_speed, c_speedvert = 8, 4, 2

    #Sounds
    bounce = pygame.mixer.Sound("bounce.wav")
    score = pygame.mixer.Sound("score.wav")
    lose = pygame.mixer.Sound("lose.wav")

    def __init__(self):
        pygame.init()
        pygame.display.update()
        pygame.display.set_caption("Pong No Walls")
        self.screen = window_surface
        self.screen.fill(self.BLACK)
        self.clock = pygame.time.Clock()
        self.y -= self.speedy
        self.x -= self.speedx

    def begin_game(self):
        self.message(self.player_score, self.WHITE, HEIGHT/2 - font_size, WIDTH/2 - font_size/2)
        self.message(self.computer_score, self.WHITE, HEIGHT/2 + font_size, WIDTH/2 - font_size/2)
        self.draw_game()
        self.computer_control()
        self.reset_ball_pos()
        self.update_ball_pos()
        self.paddle_collision()
        self.win_condition()

    def computer_control(self):
        if (self.x < self.c_x) and (self.c_x >= 4):
            self.c_x -= self.c_speed
        if (self.x > self.c_x) and (self.c_x <= (HEIGHT/2) - self.p_HEIGHT):
            self.c_x += self.c_speed
        if (self.y < self.c_y) and (self.c_y >= -(WIDTH/2) + self.p_HEIGHT/2):
            self.c_y -= self.c_speedvert
        if (self.y > self.c_y) and (self.c_y <= (WIDTH/2) - self.p_HEIGHT/2):
            self.c_y += self.c_speedvert

    def draw_game(self):
        pygame.draw.line(window_surface, self.YELLOW, (HEIGHT/2, 0), (HEIGHT/2, WIDTH), 2)
        pygame.draw.circle(window_surface, self.RED, (int(self.x) + int((HEIGHT/2)),int(self.y) + int((WIDTH/2))), self.radius)
        pygame.draw.rect(window_surface, self.WHITE, ((0, int(self.p_y + WIDTH/2 - self.p_HEIGHT/2)), (int(self.p_WIDTH), int(self.p_HEIGHT)))) #Vertical Player Paddle
        pygame.draw.rect(window_surface, self.WHITE, ((int(self.p_x + HEIGHT/2 - self.p_HEIGHT), 0), (int(self.p_HEIGHT), int(self.p_WIDTH)))) #Top Player Paddle
        pygame.draw.rect(window_surface, self.WHITE, ((int(self.p_x + HEIGHT/2 - self.p_HEIGHT), int(WIDTH - self.p_WIDTH)), (int(self.p_HEIGHT), int(self.p_WIDTH)))) #Bottom Player Paddle
        pygame.draw.rect(window_surface, self.GREEN, ((HEIGHT - self.p_WIDTH, int(self.c_y + WIDTH/2 - self.p_HEIGHT/2)), (int(self.p_WIDTH), int(self.p_HEIGHT)))) #Vertical Computer Paddle
        pygame.draw.rect(window_surface, self.GREEN, ((int(self.c_x + HEIGHT/2), 0), (int(self.p_HEIGHT), int(self.p_WIDTH)))) #Top Computer Paddle
        pygame.draw.rect(window_surface, self.GREEN, ((int(self.c_x + HEIGHT/2), int(WIDTH - self.p_WIDTH)), (int(self.p_HEIGHT), int(self.p_WIDTH)))) #Bottom Computer Paddle

    def message(self, msg, color, locationx, locationy):
        text = basicFont.render(str(msg), True, color)
        window_surface.blit(text, (locationx, locationy))

    def paddle_collision(self):
        keys = pygame.key.get_pressed()
        #Player Paddles Only
        if keys[pygame.K_UP] and self.p_y >= top_boundary + self.p_HEIGHT/2:
            self.p_y -= self.p_speed
        if keys[pygame.K_DOWN] and self.p_y <= (bottom_boundary - self.p_HEIGHT + self.p_HEIGHT/2):
            self.p_y += self.p_speed
        if keys[pygame.K_LEFT] and self.p_x >= -(HEIGHT/2 - self.p_HEIGHT):
            self.p_x -= self.p_speed
        if keys[pygame.K_RIGHT] and self.p_x <= (-4):
            self.p_x += self.p_speed
        #COMPUTER PADDLES
        if keys[pygame.K_w] and self.c_y >= top_boundary + self.p_HEIGHT/2:
            self.c_y -= self.c_speed
        if keys[pygame.K_a] and self.c_y <= bottom_boundary - self.p_HEIGHT/2:
            self.c_y += self.c_speed
        if keys[pygame.K_s] and self.c_x >= (4):
            self.c_x -= self.c_speed
        if keys[pygame.K_d] and self.c_x <= ((HEIGHT/2) - self.p_HEIGHT):
            self.c_x += self.c_speed
        #COMPUTER SPEED
        if keys[pygame.K_PAGEUP]:
            self.c_speed = 4
            self.c_speedvert = 5
        if keys[pygame.K_PAGEDOWN]:
            self.c_speed = 1
            self.c_speedvert = 1

    def reset_ball_pos(self): #Also keeps score-count
        if (self.x <= -(HEIGHT/2)): #If meets sidewall
            self.computer_score += 1
            self.speedx = random.choice(xlist)
            self.speedy = random.choice(ylist)
            self.x = 0
            self.y = 0
        if ((self.y <= -(WIDTH/2) and self.x <= 0) or (self.y >= (WIDTH/2)) and self.x <= 0): #If meets upper/bottom wall
            self.computer_score += 1
            self.x = 0
            self.y = 0
            self.speedx = random.choice(xlist)
            self.speedy = random.choice(ylist)
        if (self.x >= (HEIGHT/2)):
            self.player_score += 1
            self.speedx = random.choice(xlist)
            self.speedy = random.choice(ylist)
            self.x = 0
            self.y = 0
        if ((self.y <= (-WIDTH/2) and self.x >= 0) or (self.y >= (WIDTH/2) and self.x >= 0)):
            self.player_score += 1
            self.speedx = random.choice(xlist)
            self.speedy = random.choice(ylist)
            self.x = 0
            self.y = 0

    def welcome_screen(self):
        pygame.draw.rect(window_surface, self.RED, (HEIGHT/2 + 50, WIDTH/2 - 50, 200, 100))
        pygame.draw.rect(window_surface, self.GREEN, (HEIGHT/2 - 250, WIDTH/2 - 50, 200, 100))
        self.message("PLAY", self.BLACK, HEIGHT/2 - 225, WIDTH/2 - 25)
        self.message("EXIT", self.BLACK, HEIGHT/2 + 100, WIDTH/2 - 25)
        start_button, exit_button = True, True

    def winner_screen(self):
        pygame.draw.rect(window_surface, self.RED, (HEIGHT/2 + 50, WIDTH/2 - 50, 200, 100))
        pygame.draw.rect(window_surface, self.GREEN, (HEIGHT/2 - 250, WIDTH/2 - 50, 200, 100))
        pygame.draw.rect(window_surface, self.WHITE, (HEIGHT/2 - 400, WIDTH/2 - 230, 800, 100))
        self.message("REPLAY", self.BLACK, HEIGHT/2 - 225, WIDTH/2 - 25)
        self.message("EXIT", self.BLACK, HEIGHT/2 + 100, WIDTH/2 - 25)
        self.message("WINNER: " + self.winner, self.BLACK, HEIGHT/2 - 270, WIDTH/2 - 200)
        replay_button, exit_button = True, True

    def screen_state(self):
        if (self.start == False):
            self.welcome_screen()
        if (self.start == True):
            self.begin_game()
        if (self.cwon == True or self.pwon):
            self.winner_screen()
            if (self.pwon == True):
                pygame.mixer.find_channel(True).play(self.score)
            if (self.cwon == True):
                pygame.mixer.find_channel(True).play(self.lose)
    def update_ball_pos(self):
        self.y -= self.speedy
        self.x -= self.speedx

        #if ((self.y <= -(WIDTH/2) or self.y >= (WIDTH/2)) and self.x >= 0): #This Block of code is a practice mode
        #    self.speedy *= -1
        #if ((self.x <= -(HEIGHT/2) or self.x >= (HEIGHT/2)) and self.x >= 0):
        #    self.speedx *= -1
        #PLAYER
        if (self.x <= -(HEIGHT/2 - self.diameter) and (self.y + self.p_HEIGHT/2 >= self.p_y and self.y + self.p_HEIGHT/2 <= self.p_y + self.p_HEIGHT)): # Vertical Ball/Paddle Collision
            self.speedx *= -1
            pygame.mixer.Sound.play(self.bounce)
        if ((self.x <= self.p_x and self.x >= self.p_x - self.p_HEIGHT) and (self.y <= -(WIDTH/2) + self.p_WIDTH + self.radius)): # Top Ball/Paddle Collison
            self.speedy *= -1
            pygame.mixer.Sound.play(self.bounce)
        if ((self.x <= self.p_x and self.x >= self.p_x - self.p_HEIGHT) and (self.y >= (WIDTH/2 - self.p_WIDTH - self.radius))): # Bottom Ball/Paddle Collision
            self.speedy *= -1
            pygame.mixer.Sound.play(self.bounce)
        #COMPUTER
        if (self.x >= (HEIGHT/2 - self.p_WIDTH) and (self.y + self.p_HEIGHT/2 >= self.c_y and self.y + self.p_HEIGHT/2 <= self.c_y + self.p_HEIGHT)): # Vertical Ball/Paddle Collision
            self.speedx *= -1
            pygame.mixer.Sound.play(self.bounce)
        if (self.x >= self.c_x and self.x <= self.c_x + self.p_HEIGHT) and (self.y <= -(WIDTH/2) + self.p_WIDTH + self.radius): # Top Ball/Paddle Collison
            self.speedy *= -1
            pygame.mixer.Sound.play(self.bounce)
        if (self.x >= self.c_x and self.x <= self.c_x + self.p_HEIGHT) and (self.y >= (WIDTH/2) - self.p_WIDTH - self.radius): # Bottom Ball/Paddle Collision
            self.speedy *= -1
            pygame.mixer.Sound.play(self.bounce)

    def win_condition(self):
        if (self.player_score >= 2 and (self.player_score - self.computer_score) >= 2):
            self.p_games_won += 1
            self.player_score, self.computer_score = 0, 0
        if (self.computer_score >= 2 and (self.computer_score - self.player_score) >= 2):
            self.c_games_won += 1
            self.player_score, self.computer_score = 0, 0
        if (self.p_games_won == 3):
            self.pwon = True
            self.winner = "PLAYER"
        if (self.c_games_won == 3):
            self.cwon = True
            self.winner = "CPU"

    def main_loop(self):
        while True:
            window_surface.fill((pong.PURPLE))
            self.screen_state()
            self.clock.tick(fps)
            pygame.display.flip()
            for event in pygame.event.get():
                if ((event.type == MOUSEBUTTONDOWN) and (pygame.mouse.get_pos() > (390, 310) and pygame.mouse.get_pos() < (590, 410))): #and (self.start_button == True or self.replay_button == True):
                    self.start = True
                if ((event.type == MOUSEBUTTONDOWN) and (pygame.mouse.get_pos() > (390, 310) and pygame.mouse.get_pos() < (590, 410))) and (self.start == True): #and (self.start_button == True or self.replay_button == True):
                    self.start = True
                    self.begin_game()
                if ((event.type == MOUSEBUTTONDOWN) and (pygame.mouse.get_pos() > (690, 310) and pygame.mouse.get_pos() < (890, 410))): #and self.exit_button == True:
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    quit()

game = pong()
game.main_loop()
