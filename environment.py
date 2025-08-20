import pygame
import random
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)


class PingPong:

    def __init__(self,
                 fps=30,
                 height=600,
                 width=800,
                 ball_radius=10,
                 ball_speed=6,
                 paddle_height=12,
                 paddle_width=100,
                 paddle_speed=7,
                 increased_speed=1.05):
        
        self.fps = fps
        self.height = height
        self.width = width
        self.ball_radius=ball_radius
        self.ball_speed = ball_speed
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width
        self.paddle_speed = paddle_speed
        self.increased_speed = increased_speed

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong Env")
        self.clock = pygame.time.Clock()


        self.ball_x = self.width//2
        self.ball_y = self.height // 2
        self.ball_vx = random.choice([-1,1])*self.ball_speed
        self.ball_vy = random.choice([-1,1])*self.ball_speed
        self.paddle_x = (self.width - self.paddle_width)//2
        self.paddle_y = self.height - self.paddle_height - 0

        self.hits = 0
        self.misses = 0


    def step(self,action):

        done = False
        reward = 0

        if action=="L":
            self.paddle_x -= self.paddle_speed
        elif action=="R":
            self.paddle_x += self.paddle_speed
        else:
            pass

        self.paddle_x = max(0, min(self.paddle_x, self.width - self.paddle_width))
        
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        if self.ball_x - self.ball_radius <= 0:
            self.ball_x = self.ball_radius
            self.ball_vx *= -1
        elif self.ball_x + self.ball_radius >= self.width:
            self.ball_x = self.width - self.ball_radius
            self.ball_vx *= -1

        if self.ball_y - self.ball_radius <= 0:
            self.ball_y = self.ball_radius
            self.ball_vy *= -1

        if self.ball_vy > 0:
            if (self.paddle_y <= self.ball_y + self.ball_radius <= self.paddle_y + self.paddle_height) and (
                self.paddle_x <= self.ball_x <= self.paddle_x + self.paddle_width
            ):
                # reflect vertically
                self.ball_y = self.paddle_y - self.ball_radius
                self.ball_vy *= self.increased_speed*-1
                self.ball_vx *= self.increased_speed
                
                reward = 2
                self.hits += 1

        if self.ball_y < self.height//2:
            reward +=0.1

        # Missed the paddle (ball fell below bottom)
        if self.ball_y + self.ball_radius > self.height:
            reward = -1
            self.misses += 1
            if self.misses == 3:
                reward = -5
                done = True
            # reset ball to center with new random velocity
            self.reset_ball()

            if self.hits == 5:
                done = True
                print("Bazzuka")
        return self._get_state(),reward, done

    def _get_state(self):
        return [float(self.ball_x/self.width),
                float(self.ball_y/self.height),
                float(self.ball_vx/self.ball_speed),
                float(self.ball_vy/self.ball_speed),
                float(self.paddle_x/self.width)]

    def reset(self):
        self.ball_x = self.width//2
        self.ball_y = self.height // 2
        self.ball_vx = random.choice([-1,1])*self.ball_speed
        self.ball_vy = random.choice([-1,1])*self.ball_speed
        self.paddle_x = (self.width - self.paddle_width)//2
        self.hits = 0
        self.misses = 0
        return self._get_state()

    def reset_ball(self):
        self.ball_x = self.width//2
        self.ball_y = self.height // 2
        self.ball_vx = random.choice([-1,1])*self.ball_speed
        self.ball_vy = random.choice([-1,1])*self.ball_speed
        self.paddle_x = self.width // 2
    
    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        pygame.draw.rect(self.screen, GREEN, 
                         (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
        
        pygame.draw.rect(self.screen, WHITE, (0, 0, self.width, 3))  # top
        pygame.draw.rect(self.screen, WHITE, (0, 0, 3, self.height))  # left
        pygame.draw.rect(self.screen, WHITE, (self.width - 3, 0, 3, self.height))  # right
        

        pygame.draw.circle(self.screen, (255, 0, 0),(int(self.ball_x), int(self.ball_y)) , self.ball_radius)
        pygame.display.flip()
        self.clock.tick(self.fps)
