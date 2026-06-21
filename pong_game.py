"""
Pong
----
Classic 2-player Pong built with Pygame.

Controls:
  Player 1 (left paddle)  - W / S
  Player 2 (right paddle) - Up / Down arrows
  P                       - pause / unpause
  R                       - restart after game over (someone reaches winning score)
  ESC                     - quit

Run with:  python pong_game.py
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

PADDLE_WIDTH = 14
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6
PADDLE_MARGIN = 30  # distance from the side wall

BALL_SIZE = 14
BALL_SPEED_START = 5
BALL_SPEED_MAX = 14
BALL_SPEEDUP = 0.4  # speed increase on each paddle hit

WINNING_SCORE = 5

# Colors
BG_COLOR = (18, 21, 27)
MID_LINE_COLOR = (60, 66, 78)
PADDLE_COLOR = (235, 235, 235)
BALL_COLOR = (235, 192, 92)
TEXT_COLOR = (235, 235, 235)
SHADOW_COLOR = (10, 12, 16)
ACCENT_COLOR = (98, 209, 124)


class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy):
        self.rect.y += dy
        self.rect.y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self, screen):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect, border_radius=4)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)
        self.reset(direction=random.choice([-1, 1]))

    def reset(self, direction=1):
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        angle = random.uniform(-0.35, 0.35)  # slight vertical randomness
        self.speed = BALL_SPEED_START
        self.vx = direction * self.speed * (1 - abs(angle))
        self.vy = self.speed * angle * 2.5

    def move(self):
        self.rect.x += round(self.vx)
        self.rect.y += round(self.vy)

        # Bounce off top/bottom walls
        if self.rect.top <= 0:
            self.rect.top = 0
            self.vy *= -1
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.vy *= -1

    def bounce_off_paddle(self, paddle: Paddle, going_right: bool):
        # Adjust vertical speed based on where the ball hit the paddle
        offset = (self.rect.centery - paddle.rect.centery) / (PADDLE_HEIGHT / 2)
        self.speed = min(self.speed + BALL_SPEEDUP, BALL_SPEED_MAX)
        direction = 1 if going_right else -1
        self.vx = direction * self.speed * 0.9
        self.vy = self.speed * offset * 0.9

    def draw(self, screen):
        pygame.draw.ellipse(screen, BALL_COLOR, self.rect)


class PongGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 64, bold=True)
        self.font_med = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.reset()

    def reset(self):
        self.p1 = Paddle(PADDLE_MARGIN, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.p2 = Paddle(WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.score1 = 0
        self.score2 = 0
        self.paused = False
        self.game_over = False
        self.winner = None

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.game_over:
                    self.reset()

        if self.game_over or self.paused:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.p1.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            self.p1.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            self.p2.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            self.p2.move(PADDLE_SPEED)

    def update(self):
        if self.game_over or self.paused:
            return

        self.ball.move()

        # Paddle collisions
        if self.ball.rect.colliderect(self.p1.rect) and self.ball.vx < 0:
            self.ball.rect.left = self.p1.rect.right
            self.ball.bounce_off_paddle(self.p1, going_right=True)
        elif self.ball.rect.colliderect(self.p2.rect) and self.ball.vx > 0:
            self.ball.rect.right = self.p2.rect.left
            self.ball.bounce_off_paddle(self.p2, going_right=False)

        # Scoring
        if self.ball.rect.right < 0:
            self.score2 += 1
            self.check_winner()
            if not self.game_over:
                self.ball.reset(direction=1)
        elif self.ball.rect.left > WINDOW_WIDTH:
            self.score1 += 1
            self.check_winner()
            if not self.game_over:
                self.ball.reset(direction=-1)

    def check_winner(self):
        if self.score1 >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 1"
        elif self.score2 >= WINNING_SCORE:
            self.game_over = True
            self.winner = "Player 2"

    def draw_mid_line(self):
        dash_height = 16
        gap = 12
        x = WINDOW_WIDTH // 2 - 2
        y = 0
        while y < WINDOW_HEIGHT:
            pygame.draw.rect(self.screen, MID_LINE_COLOR, (x, y, 4, dash_height))
            y += dash_height + gap

    def draw_centered_text(self, text, font, color, y_offset=0):
        surf = font.render(text, True, color)
        shadow = font.render(text, True, SHADOW_COLOR)
        x = WINDOW_WIDTH // 2 - surf.get_width() // 2
        y = WINDOW_HEIGHT // 2 - surf.get_height() // 2 + y_offset
        self.screen.blit(shadow, (x + 2, y + 2))
        self.screen.blit(surf, (x, y))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_mid_line()

        self.p1.draw(self.screen)
        self.p2.draw(self.screen)
        self.ball.draw(self.screen)

        score1_surf = self.font_big.render(str(self.score1), True, TEXT_COLOR)
        score2_surf = self.font_big.render(str(self.score2), True, TEXT_COLOR)
        self.screen.blit(score1_surf, (WINDOW_WIDTH // 4 - score1_surf.get_width() // 2, 24))
        self.screen.blit(score2_surf, (WINDOW_WIDTH * 3 // 4 - score2_surf.get_width() // 2, 24))

        hint = self.font_small.render("P1: W/S    P2: Up/Down    P: Pause    Esc: Quit", True, MID_LINE_COLOR)
        self.screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 28))

        if self.paused:
            self.draw_centered_text("PAUSED", self.font_big, TEXT_COLOR)
        elif self.game_over:
            self.draw_centered_text(f"{self.winner} Wins!", self.font_big, ACCENT_COLOR, -20)
            self.draw_centered_text("Press R to restart", self.font_med, TEXT_COLOR, 40)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    PongGame().run()
