import pygame
import random
import time
#1 Initialize
pygame.init()
pygame.display.set_caption("Pong Game")
#2 Set up game window

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_x = 2
        self.v_y = 1
        self.iamge = pygame.image.load("assets/ball.png")

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def physic(self, paddle1, paddle2):
        if self.x >= 580 or self.x <= 0:
            self.x = 300
            self.y = 300
        if self.y >= 580 or self.y <= 0:
            self.v_y = - self.v_y

        if paddle1.x + 30 >= self.x and (paddle1.y <= self.y <= paddle1.y + 120):
            self.v_x = - self.v_x
        if paddle2.x <= self.x + 20 and (paddle2.y <= self.y <= paddle2.y + 120):
            self.v_x = - self.v_x
        

    def dispplay(self, canvas):
        canvas.blit(self.iamge, (self.x, self.y))


class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/paddle.png")

    def move_up(self):
        self.y -= 2

    def move_down(self):
        self.y += 2
    

    def display(self, canvas):
        canvas.blit(self.image, (self.x, self.y))

    




ball = Ball(300,300)
paddle1 = Paddle(0, 150)
paddle2 = Paddle(570, 300)

def game(a, b):
  
    SIZE = (600, 600)

    BG_COLOR = (1, 1, 1) # google color picker

    canvas = pygame.display.set_mode(SIZE) # to giay ve

    clock = pygame.time.Clock()


    loop = True



    w_pressed = False
    s_pressed = False
    up_pressed = False
    down_pressed = False


    while loop:
        ball.move()
        ball.physic(paddle1, paddle2)
        # pooling, check xem nguoi dung lam gi
        events = pygame.event.get() # lay ra hanh dong nguoi dung, de vao list
        for e in events: # duyet tung phan tu trong event

            if e.type == pygame.QUIT:
                loop = False # action = thoat game


            elif e.type == pygame.KEYDOWN: # nhan xuong ( keyup nha ra)
                if e.key == pygame.K_w: # chu y toa do x, y
                    w_pressed = True
                elif e.key == pygame.K_s:
                    s_pressed = True

                if e.key == pygame.K_UP:  # chu y toa do x, y
                    up_pressed = True
                elif e.key == pygame.K_DOWN:
                    down_pressed = True


            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_w:
                    w_pressed = False
                elif e.key == pygame.K_s:
                    s_pressed = False

                if e.key == pygame.K_UP:
                    up_pressed = False
                elif e.key == pygame.K_DOWN:
                    down_pressed = False

        if w_pressed:
            paddle1.move_up()
        if s_pressed:
            paddle1.move_down()
        if up_pressed:
            paddle2.move_up()
        if down_pressed:
            paddle2.move_down()



        canvas.fill(BG_COLOR)
        ball.dispplay(canvas)
        paddle1.display(canvas)
        paddle2.display(canvas)

        clock.tick(120)

        pygame.display.flip()

game(0, 0)
