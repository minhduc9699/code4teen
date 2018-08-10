import pygame
import time
import sys
from pygame.locals import *
from Player1 import main as main_1
import cv2
import webcam
import webcam2
import random

pygame.init()
fieldimg = pygame.image.load('field.jpg')
clock = pygame.time.Clock()
# Create a displace surface object2200
display_surf = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

GREEN = (72, 150, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
LIGHTRED = (255, 0, 0)
ORANGE=(255,128,0)

YELLOW = (200, 200, 0)
LIGHTYELLOW = (255, 255, 0)
LIGHTGREEN = (91, 189, 43)
pygame.display.set_caption("PongCup2018")
fps = 200
fps_clock = pygame.time.Clock()
# font chữ
smallfont = pygame.font.SysFont('comicsansms', 25)
medfont = pygame.font.SysFont('comicsansms', 50)
largefont = pygame.font.SysFont('comicsansms', 100)
# phần việc cần làm:
# thêm đồ họa
window_width, window_height = display_surf.get_size()
soccerimg = pygame.image.load('soccer1.png')
spainimg = pygame.image.load('Spain.png')
gerimg = pygame.image.load('Germany.png')
introimg = pygame.image.load('intro1.jpg')
arghenimg=pygame.image.load('Argentina.png')
#nút bấm intro
def Button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(display_surf, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            if action == '2players':
                main()
            if action == '1player':
                main_1()

    else:
        pygame.draw.rect(display_surf, inactive_color, (x, y, width, height))
    Text().text_to_button(text, BLACK, x, y, width, height)

#pause
def pause():
    paused = True
    Game().text.message_to_screen('Paused',
                                     WHITE,
                                  -100,
                                  size='large')
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

#vòng game
def main():
    ingame_sound = pygame.mixer.Sound("D:\\Codeshit1\\PongCup\\music\\ingame.wav")
    pygame.mixer.music.load(("D:\\Codeshit1\\PongCup\\music\\ingame.wav"))
    ingame_sound.play()
    pygame.init()
    game = Game()
    GameExit = False
    GameOver = False
    c = 0
    vision = webcam.webcam()
    vision.thread_webcam()
    vision2 = webcam2.webcam()
    vision2.thread_webcam2()
    while not GameExit:
        window_width, window_height = display_surf.get_size()

        if GameOver == True:
            game.text.message_to_screen('Game Over',
                                        RED,
                                        -50,
                                        size='large')
            game.text.message_to_screen('Press C to play again or  Q to Quit',
                                        WHITE,
                                        50,
                                        size='medium')
            pygame.display.update()

        while GameOver == True:
            # display_surf.fill(WHITE)

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
        game.paddles['user1'].move((cx, cy - hmax / 2))
        frame = vision.get_currentFrame()
        # cv2.rectangle(frame, (0, 0), (int(3 * frame.shape[1] / 4), int(frame.shape[0] / 2)), (0, 0, 255), 5)
        cv2.circle(frame, (int(cx), int(cy)), 10, (0, 255, 0), 1)
        cv2.imshow("German",frame)
        cv2.waitKey(10)
        # if c == pygame.K_d and game.paddles['user1'].rect.x <= window_width / 2 - game.line_thickness:
        #     game.paddles['user1'].rect.x += game.speed
        #
        # # Down1:
        # elif c == pygame.K_a and game.paddles['user1'].rect.x >= game.line_thickness:
        #     game.paddles['user1'].rect.x -= game.speed
        #
        # # Left1
        # elif c == pygame.K_w and game.paddles['user1'].rect.y > 11:
        #     game.paddles['user1'].rect.y -= game.speed
        #
        # # right1
        # elif c == pygame.K_s and game.paddles['user1'].rect.y < window_height:
        #     game.paddles['user1'].rect.y += game.speed

        # # up2
        # if c == pygame.K_LEFT and game.paddles['user2'].rect.x >= window_width / 2 + 1:
        #     game.paddles['user2'].rect.x -= game.speed
        # # down2
        # elif c == pygame.K_RIGHT and game.paddles['user2'].rect.x <= window_width - 20:
        #     game.paddles['user2'].rect.x += game.speed
        # # left2
        # elif c == pygame.K_DOWN and game.paddles['user2'].rect.y < window_height - 61:
        #     game.paddles['user2'].rect.y += game.speed
        # # right2
        # elif c == pygame.K_UP and game.paddles['user2'].rect.y > 11:
        #     game.paddles['user2'].rect.y -= game.speed

#player 2

        cx2, cy2, hmax2 = vision2.get_currentPos2()
        game.paddles['user2'].move((cx2, cy2 - hmax2 / 2))
        frame2 = vision2.get_currentFrame2()
        # cv2.rectangle(frame, (0, 0), (int(3 * frame.shape[1] / 4), int(frame.shape[0] / 2)), (0, 0, 255), 5)
        cv2.circle(frame2, (int(cx2), int(cy2)), 10, (0, 255, 0), 1)
        cv2.imshow("Argentina",frame2)
        cv2.waitKey(10)


        game.update()
        # cơ chế chơi


        if game.score.score1 == 5:
            game.text.message_to_screen('You Lose',BLACK)
            GameOver = True
        #
        if game.score.score2 == 5:
            game.text.message_to_screen('You Lose',BLACK)
            GameOver = True
        # if game.skill.hit_paddle1(game.paddles['user1']):
        #     break
        pygame.display.flip()
        fps_clock.tick(fps)


#    print('Your score:', game.score.score)


#game intro
def game_intro():
    pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\menu.wav")
    pygame.mixer.music.play(1)
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_c:
                    intro = False

        display_surf.blit(introimg, (0, 0))
        Game().text.message_to_screen('PongCup2018',
                                      ORANGE,
                                      -100,
                                      'large')

        # Game().text.message_to_screen('Press C to play or Q to Quit',
        #                             BLACK,
        #                             50,
        #                             size='medium')

        pygame.draw.rect(display_surf, GREEN, (window_width / 2 - 100, window_height / 2 + 100, 200, 50))
        pygame.draw.rect(display_surf, YELLOW, (window_width / 2 - 100, window_height / 2 + 200, 200, 50))
        pygame.draw.rect(display_surf, RED, (window_width / 2 - 100, window_height / 2 + 300, 200, 50))

        Text().text_to_button('Play', BLACK, window_width / 2 - 100, window_height / 2, 200, 50, 'medium')
        Button('1 Player Game', window_width / 2 - 100, window_height / 2 + 100, 200, 50, GREEN, LIGHTGREEN,
               action='1player')
        Button('2 Players Game', window_width / 2 - 100, window_height / 2 + 200, 200, 50, YELLOW, LIGHTYELLOW,
               action='2players')
        Button('Quit', window_width / 2 - 100, window_height / 2 + 300, 200, 50, RED, LIGHTRED, action='quit')

        pygame.display.update()
        clock.tick(15)


class Paddle1:
    def __init__(self, x, w, h,speed):
        self.w = w
        self.h = h
        self.x = x
        self.y = window_height / 2
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        display_surf.blit(gerimg, self.rect)

    def move(self, pos):
        self.rect.y = pos[1]
        self.draw()

class Paddle2:
    def __init__(self, x, w, h,speed):
        self.w = w
        self.h = h
        self.x = x
        self.y = window_height / 2
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        display_surf.blit(arghenimg, self.rect)

    def move(self, pos):
        self.rect.y = pos[1]
        self.draw()


# class Skill:#color = none
#     def __init__(self,x,y,w,h):
#         self.x = x
#         self.y = y
#         self.w = w
#         self.h = h
#         self.color = color
#         self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
#         làm cách nào để chuyển màu từng skill ?
    # def draw(self):
    #     pygame.draw.rect(display_surf,RED,pygame.Rect(self.x,self.y,self.w,self.h))
    #     ăn các kĩ năng:resize paddle(team kia, team mình)(to,nhỏ), tăng giảm speed ball,tăng giảm speed paddle,ngược hướng paddle
    # def resize_paddle(self,paddle):
    # def hit_paddle1(self,paddle1):
    #     điều kiện chưa xong                                                                                  tọa độ x ?
        # if self.rect.top == paddle1.rect.bottom and paddle1.rect.y > self.rect.top and paddle1.rect.y <self.rect.bottom:
        #
        #     return True
        # else:
        #     return False

    # def hit_paddle2

    # def skills(self,color):






#chữ
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


class ScoreBoard:
    def __init__(self, font_size=50, score1=0, score2=0):
        self.score1 = score1
        self.score2 = score2
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

    def display1(self, score1):
        result_srf = self.font.render('%s' % score1, True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topleft = (window_width / 2 - 100, 50)
        display_surf.blit(result_srf, result_rect)

    def display2(self, score2):
        result_srf = self.font.render('%s' % score2, True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topright = (window_width / 2 + 100, 50)
        display_surf.blit(result_srf, result_rect)


class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.dir_x = -1  # left = -1 and right = 1
        self.dir_y = -1  # up = -1 and down = 1
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        # pygame.draw.rect(display_surf, WHITE, self.rect)
        display_surf.blit(soccerimg,self.rect)
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
        if (self.dir_x == -1 and self.rect.left <= self.w) or (
                self.dir_x == 1 and self.rect.right >= window_width - self.w):
            return True
        else:
            return False

    def hit_paddle_user1(self, paddle1):
        if self.rect.left == paddle1.rect.right and self.rect.bottom >= paddle1.rect.top and self.rect.top <= paddle1.rect.bottom:
            return True
        else:
            return False

    def hit_paddle_user2(self, paddle2):
        if self.rect.right == paddle2.rect.left and self.rect.bottom >= paddle2.rect.top and self.rect.top <= paddle2.rect.bottom:
            return True
        else:
            return False

    def move(self):
        self.rect.x += (self.dir_x * self.speed)
        self.rect.y += (self.dir_y * self.speed)
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('x')


class Game:
    # tìm các thứ liên quan đến linethickness để chỉnh paddle với bóng
    def __init__(self, line_thickness=10, speed=10):
        self.line_thickness = line_thickness
        self.speed = speed
        #ball things
        ball_x = window_width / 2
        ball_y = window_height / 2
        ball_w = 40
        ball_h = 40
        ball_speed = 10
        self.ball = Ball(ball_x, ball_y, ball_w, ball_h, ball_speed)
        #paddle things
        self.paddles = {}
        paddle_x = 20
        paddle_w = 50
        paddle_h = 200
        paddle_speed = 10
        self.paddles['user1'] = Paddle1(paddle_x, paddle_w, paddle_h,paddle_speed)
        self.paddles['user2'] = Paddle2(window_width - 60, paddle_w, paddle_h,paddle_speed)
        #skill:
        # skill_x = random.randint(0,window_width)
        # skill_y = random.randint(0,window_height)
        # skill_w = 30
        # skill_h = 30
        # self.skill = Skill(skill_x,skill_y,skill_w,skill_h)
        self.score = ScoreBoard()
        self.text = Text()

    def draw_arena(self):

        display_surf.blit(fieldimg, (0, 0))
        pygame.draw.line(display_surf, WHITE, (window_width / 2, 0), (window_width / 2, window_height))

    def update(self):
        self.draw_arena()
        self.ball.draw()
        self.paddles['user1'].draw()
        self.paddles['user2'].draw()
        self.ball.move()
        # self.skill.draw()
        # self.skill.hit_paddle1(Paddle1)



        # self.skill.hit_paddle2(Paddle2)
        # if

        if self.ball.hit_paddle_user1(self.paddles['user1']):
            self.ball.bounce('y')
            pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\hitball.wav")
            pygame.mixer.music.play(0)
        if self.ball.hit_paddle_user2(self.paddles['user2']):
            self.ball.bounce('y')
            pygame.mixer.music.load("D:\\Codeshit1\\PongCup\\music\\hitball.wav")
            pygame.mixer.music.play(0)
            # cơ chế cộng điểm
        if self.ball.rect.x > window_width:
            self.score.score1 += 1
            self.ball.rect.x = window_width / 2
            self.ball.rect.y = window_height / 2
        self.score.display1(self.score.score1)
        if self.ball.rect.x < 5:
            self.score.score2 += 1
            self.ball.rect.x = window_width / 2
            self.ball.rect.y = window_height / 2
        self.score.display2(self.score.score2)


if __name__ == '__main__':
    game_intro()
    main()