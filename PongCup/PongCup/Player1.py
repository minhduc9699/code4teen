import pygame
import time
import sys
from pygame.locals import*
import cv2
import webcam
import time


pygame.init()
fieldimg = pygame.image.load('field.jpg')
clock = pygame.time.Clock()
# Create a displace surface object
display_surf = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
window_width, window_height = display_surf.get_size()
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.display.set_caption("PongCup2018")
fps = 200
fps_clock = pygame.time.Clock()
#font chữ
font = pygame.font.SysFont(None, 25)
soccerimg = pygame.image.load('soccer1.png')
score = 0
spainimg = pygame.image.load('Spain.png')
gerimg = pygame.image.load('Germany.png')
arghenimg=pygame.image.load('Argentina.png')

class Paddle:
    def __init__(self, x, w, h):
        self.w = w
        self.h = h
        self.x = x
        self.y = window_height/2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        display_surf.blit(gerimg, self.rect)

    def move(self, pos):
        self.rect.y = pos[1]
        self.draw()



class AutoPaddle(Paddle):
    def __init__(self, x, w, h, speed, ball):

        super().__init__(x, w, h)
        self.speed = speed

        self.ball = ball

    def move(self):
        if self.ball.dir_x == 1:
            if self.rect.y + self.rect.h/2 < self.ball.rect.bottom:
                self.rect.y += self.speed
            if self.rect.y + self.rect.h/2 > self.ball.rect.bottom:
                self.rect.y -= self.speed
    def draw(self):
        display_surf.blit(arghenimg, self.rect)

class ScoreBoard:

    def __init__(self, font_size=20, score=0):
        self.x = window_width - 150
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

    def display(self, score):
        result_srf = self.font.render('Score : %s' % score, True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topleft = (window_width - 150, 20)
        display_surf.blit(result_srf, result_rect)
def pause():
    paused = True
    Game().text.message_to_screen('Paused',WHITE,-100,size='large')
    Game().text.message_to_screen('Press C to continue or Q to quit',
                                  WHITE,
                                  25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        # display_surf.fill(WHITE)

        clock.tick(5)
class Text:
    def text_objects(self, text, color, size):
        if size == "small":
            textSurface = smallfont.render(text, True, color)
        elif size == "medium":
            textSurface = medfont.render(text, True, color)
        elif size == "large":
            textSurface = largefont.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def text_to_button(self, msg, color, button_x, button_y, button_width, button_height, size='small'):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = ((button_x + (button_width / 2)), button_y + (button_height / 2))
        display_surf.blit(textSurf, textRect)

    def message_to_screen(self, msg, color, y_displace=0, size="small"):
        textSurf, textRect = self.text_objects(msg, color, size)
        textRect.center = (window_width / 2), (window_height / 2) + y_displace
        display_surf.blit(textSurf, textRect)

class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.dir_x = -1  # left = -1 and right = 1
        self.dir_y = -1   # up = -1 and down = 1
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        display_surf.blit(soccerimg, self.rect)

    def bounce(self, axis):
        if axis == 'x':
            self.dir_y *= -1
        if axis == 'y':
            self.dir_x *= -1

    def hit_ceiling(self):
        if self.dir_y == -1 and self.rect.top <= self.h:
            return True
        else:
            return False

    def hit_floor(self):
        if self.dir_y == 1 and self.rect.bottom >= window_height - self.h:
            return True
        else:
            return False

    def hit_wall(self):
        if self.dir_x == -1 and self.rect.left <= self.w:
            pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\goal.wav")
            pygame.mixer.music.play(0)
            return True
        else:
            return False

    def hit_paddle_user(self, paddle):
        if self.rect.left <= paddle.rect.right and self.rect.bottom >= paddle.rect.top and self.rect.top <= paddle.rect.bottom:
            return True
        else:
            return False

    def hit_paddle_computer(self, paddle):
        if self.rect.right == paddle.rect.left and self.rect.bottom >= paddle.rect.top and self.rect.top <= paddle.rect.bottom:
            return True
        else:
            return False

    def move(self):
        self.rect.x += (self.dir_x * self.speed)
        self.rect.y += (self.dir_y * self.speed)
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('x')

class Game:
    def __init__(self, line_thickness=10, speed=10):
        self.line_thickness = line_thickness
        self.speed = speed
        ball_x = window_width / 2
        ball_y = window_height / 2
        ball_w = 40
        ball_h = 40
        self.ball = Ball(ball_x, ball_y, ball_w, ball_h, self.speed)
        self.paddles = {}
        paddle_x = 20
        paddle_w = 50
        paddle_h = 200
        self.paddles['user'] = Paddle(paddle_x, paddle_w, window_height/2)
        self.paddles['computer'] = AutoPaddle(window_width - 60, paddle_w, paddle_h, self.speed, self.ball)
        self.score = ScoreBoard()
        self.text = Text()
    def draw_arena(self):

        display_surf.blit(fieldimg, (0, 0))
        pygame.draw.line(display_surf, WHITE, (window_width/2, 0), (window_width/2, window_height))

    def update(self):
        self.draw_arena()
        self.ball.draw()
        self.paddles['user'].draw()
        self.paddles['computer'].draw()
        self.ball.move()
        self.paddles['computer'].move()

        if self.ball.hit_paddle_user(self.paddles['user']):
            self.ball.bounce('y')
            self.score.score += 1
            pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\hitball.wav")
            pygame.mixer.music.play(1)
        self.score.display(self.score.score)
        if self.ball.hit_paddle_computer(self.paddles['computer']):
            self.ball.bounce('y')
            pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\hitball.wav")
            pygame.mixer.music.play(1)


def main():
    # goal =pygame.mixer.Sound("D:\\Codeshit1\\PongCup\\music\\goal.wav")
    # hitball=pygame.mixer.Sound("D:\\Codeshit1\\PongCup\\music\\hitball.wav")
    # menu=pygame.mixer.Sound("D:\\Codeshit1\\PongCup\\music\\menu.wav")
    ingame_sound = pygame.mixer.Sound("D:\\Codeshit1\\PongCup\\music\\ingame.wav")
    pygame.mixer.music.load(("D:\\Codeshit1\\PongCup\\music\\ingame.wav"))
    ingame_sound.play()
    pygame.init()
    game = Game()
    GameExit = False
    GameOver = False
    c= 0
    vision = webcam.webcam()
    vision.thread_webcam()
    while not GameExit:

        while GameOver == True:
            display_surf.fill(WHITE)
            game.text.message_to_screen('Game Over, Press C to play again or  Q to Quit', BLACK)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_q:
                        GameExit = True
                        GameOver = False
                    if event.key == pygame.K_c:
                        main()
        for event in pygame.event.get():
            if event.type == QUIT:
                GameExit = True
            if event.type == KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.KEYDOWN:
                c= event.key
            elif event.type == pygame.KEYUP:
                c= 0

        cx, cy, hmax = vision.get_currentPos()
        game.paddles['user'].move((cx, cy- hmax / 2))
        frame = vision.get_currentFrame()
        # cv2.rectangle(frame, (0, 0), (int(3 * frame.shape[1] / 4), int(frame.shape[0] / 2)), (0, 0, 255), 5)
        cv2.circle(frame, (int(cx)//3, int(cy)//3), 10, (0, 255, 0), 1)
        cv2.imshow("video thread main", frame)
        cv2.waitKey(10)

        # if c == pygame.K_d and game.paddles['user'].rect.x <= window_width / 2 - game.line_thickness:
        #     game.paddles['user'].rect.x += game.speed
        #
        # # Down1:
        # elif c == pygame.K_a and game.paddles['user'].rect.x >= game.line_thickness:
        #     game.paddles['user'].rect.x -= game.speed
        #
        # # Left1
        # elif c == pygame.K_w and game.paddles['user'].rect.y > 11:
        #     game.paddles['user'].rect.y -= game.speed
        #
        # # right1
        # elif c == pygame.K_s and game.paddles['user'].rect.y < window_height:
        #     game.paddles['user'].rect.y += game.speed

        game.update()
        # cơ chế chơi
        if game.ball.hit_wall():
            # time.sleep(5)
            break
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()