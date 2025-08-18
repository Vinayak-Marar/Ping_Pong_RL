import pygame
import random
import sys

# --- Game settings ---
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 50
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 12
FPS = 60
PADDLE_SPEED = 7
BALL_SPEED_MIN = 4
BALL_SPEED_MAX = 6
INCREASED_SPEED = 1.01
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)


def reset_ball():
    """Return initial ball state: (x, y, vel_x, vel_y)"""
    x = WIDTH // 2
    y = HEIGHT // 2
    # random horizontal velocity
    vx = random.choice([-1, 1]) * random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX)
    # always start moving upward
    vy = -random.uniform(BALL_SPEED_MIN, BALL_SPEED_MAX)
    return x, y, vx, vy


def clamp(val, a, b):
    return max(a, min(b, val))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong - Single Player")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # Paddle start (centered at bottom)
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    paddle_y = HEIGHT - PADDLE_HEIGHT - 0

    # Ball
    ball_x, ball_y, ball_vx, ball_vy = reset_ball()

    # Score / stats
    hits = 0
    misses = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Input ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle_x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle_x += PADDLE_SPEED

        paddle_x = clamp(paddle_x, 0, WIDTH - PADDLE_WIDTH)

        # --- Update ball ---
        ball_x += ball_vx
        ball_y += ball_vy

        # Bounce left/right walls
        if ball_x - BALL_RADIUS <= 0:
            ball_x = BALL_RADIUS
            ball_vx *= -1
        elif ball_x + BALL_RADIUS >= WIDTH:
            ball_x = WIDTH - BALL_RADIUS
            ball_vx *= -1

        # Bounce top
        if ball_y - BALL_RADIUS <= 0:
            ball_y = BALL_RADIUS
            ball_vy *= -1

        # Check paddle collision (only when ball is moving downwards)
        if ball_vy > 0:
            if (paddle_y <= ball_y + BALL_RADIUS <= paddle_y + PADDLE_HEIGHT) and (
                paddle_x <= ball_x <= paddle_x + PADDLE_WIDTH
            ):
                # reflect vertically
                ball_y = paddle_y - BALL_RADIUS
                ball_vy *= INCREASED_SPEED*-1
                ball_vx *= INCREASED_SPEED

                # clamp speed to avoid too-slow or too-fast
                speed = (ball_vx ** 2 + ball_vy ** 2) ** 0.5
                if speed < BALL_SPEED_MIN:
                    factor = BALL_SPEED_MIN / speed
                    ball_vx *= factor
                    ball_vy *= factor

                hits += 1

        # Missed the paddle (ball fell below bottom)
        if ball_y + BALL_RADIUS > HEIGHT:
            misses += 1
            # reset ball to center with new random velocity
            ball_x, ball_y, ball_vx, ball_vy = reset_ball()

        # --- Draw ---
        screen.fill(BLACK)

        # Draw walls (visual guide) - left, top, right
        # (Bottom is open for paddle/miss)
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, 3))  # top
        pygame.draw.rect(screen, WHITE, (0, 0, 3, HEIGHT))  # left
        pygame.draw.rect(screen, WHITE, (WIDTH - 3, 0, 3, HEIGHT))  # right

        # Paddle
        pygame.draw.rect(screen, GREEN, (paddle_x, paddle_y, PADDLE_WIDTH-10, PADDLE_HEIGHT))

        # Ball
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

        # HUD
        score_surf = font.render(f"Hits: {hits}   Misses: {misses}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
