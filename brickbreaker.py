import os
import sys
import cv2
import pygame
import random
import numpy as np
from eyeGestures.utils import VideoCapture
from eyeGestures import EyeGestures_v3

pre_calibrate = True

# Initialize Pygame
pygame.init()
pygame.font.init()

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/..')

gestures = EyeGestures_v3()
try:
    cap = VideoCapture(1)
except:
    cap = VideoCapture(0)

x = np.arange(0, 1.1, 0.2)
y = np.arange(0, 1.1, 0.2)

xx, yy = np.meshgrid(x, y)

calibration_map = np.column_stack([xx.ravel(), yy.ravel()])
n_points = min(len(calibration_map),25)
np.random.shuffle(calibration_map)
gestures.uploadCalibrationMap(calibration_map,context="my_context")
gestures.setFixation(1.0)

clock = pygame.time.Clock()

# Import assets

FONT = pygame.font.Font(os.path.join('assets', 'spacetime-regular.ttf'), 50)

paddle_img = pygame.image.load(os.path.join('assets', 'paddle.png'))
brick_imgs = [
    pygame.image.load(os.path.join('assets', 'brick1.png')),
    pygame.image.load(os.path.join('assets', 'brick2.png')),
    pygame.image.load(os.path.join('assets', 'brick3.png'))
]
ball_img = pygame.image.load(os.path.join('assets', 'asteroid.png'))
bg_img = pygame.image.load(os.path.join('assets', 'background.png'))

# Screen dimensions
SCREEN_INFO = pygame.display.Info()
SCREEN_WIDTH = SCREEN_INFO.current_w
SCREEN_HEIGHT = SCREEN_INFO.current_h
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Crater Crash")
font_size = 48
bold_font = pygame.font.Font(None, font_size)
bold_font.set_bold(True)  # Set the font to bold

# Colors
RED = (255, 0, 100)
BLUE = (30, 90, 122)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

BRICK_COLORS = (
    (196,118,204),
    (216,143,151),
    (157,219,144)
)

# Paddle
PADDLE_WIDTH = 700
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - (PADDLE_HEIGHT + 10), PADDLE_WIDTH, PADDLE_HEIGHT)
# paddle_img = pygame.transform.scale(paddle_img, (PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball
BALL_SIZE = 50
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed = [5, -5]
ball_img = pygame.transform.scale(ball_img, (BALL_SIZE, BALL_SIZE))

# Bricks
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
bricks = [pygame.Rect(10 + i * (BRICK_WIDTH + 10), 10 + j * (BRICK_HEIGHT + 10), BRICK_WIDTH, BRICK_HEIGHT) for i in range(SCREEN_WIDTH%(BRICK_WIDTH+10)) for j in range(5)]
brick_imgs = [pygame.transform.scale(brick_img, (BRICK_WIDTH, BRICK_HEIGHT)) for brick_img in brick_imgs]

score = 0

NUM_LIVES = 3
lives = NUM_LIVES

screen = 0
NUM_SCREENS = 5
TEXT_COLOR = WHITE
TEXT_BG_COLOR = BLUE

def center(text, y_offset=0):
    return text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+y_offset))

# Start screen
while screen < NUM_SCREENS:
    SCREEN.blit(bg_img, (0,0))

    match screen:
        case 0:
            texts = ['PRESS SPACE TO START']
        case 1:
            texts = [
                'WELCOME! YOU WILL UNDERGO A SHORT', 
                'CALIBRATION BEFORE YOUR MISSION BEGINS'
            ]
        case 2:
            texts = [
                'LOOK AT THE CENTER OF EACH', 
                'PURPLE CIRCLE AS IT APPEARS'
            ]
        case 3:
            texts = [
                'ONCE YOUR CALIBRATION IS COMPLETE,',
                'LOOK TO THE LEFT OR RIGHT SIDE',
                'OF THE SCREEN TO STEER'
            ]
        case 4:
            texts = [
                'BE CAREFUL!',
                f'YOU ONLY HAVE {NUM_LIVES} LIVES'
            ]

    for i, text in enumerate(texts):
        text_rect = FONT.render(text, False, TEXT_COLOR, TEXT_BG_COLOR)
        SCREEN.blit(text_rect, center(text_rect, y_offset=-70*(len(texts)-1)+i*70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                screen += 1
    
    pygame.display.flip()
    clock.tick(60)
    
running = True
iterator = 0
prev_x = 0
prev_y = 0
SCORE_FONT = pygame.font.Font(os.path.join('assets', 'spacetime-regular.ttf'), 100)

# Main game loop
while running:
    # Event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                running = False

    # Generate new random position for the cursor  
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        # frame = np.rot90(frame)
        frame = np.flip(frame, axis=1)
        calibrate = pre_calibrate and (iterator <= n_points) # calibrate 25 points
        event, calibration = gestures.step(frame, calibrate, SCREEN_WIDTH, SCREEN_HEIGHT, context="my_context")
    except:
        print("WARN: No eyes detected!")

    SCREEN.fill((0, 0, 0))
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.scale(frame, (400, 400))

    if event is not None or calibration is not None:
        # Display frame on Pygame screen
        SCREEN.blit(
            pygame.surfarray.make_surface(
                np.rot90(event.sub_frame)
            ),
            (0, 0)
        )

        if calibrate:
            text_surface = FONT.render(f'{event.fixation}', False, (0, 0, 0))
            SCREEN.blit(text_surface, (0,0))
            if calibrate:
                if calibration.point[0] != prev_x or calibration.point[1] != prev_y:
                    iterator += 1
                    prev_x = calibration.point[0]
                    prev_y = calibration.point[1]
                # pygame.draw.circle(SCREEN, GREEN, fit_point, calibration_radius)
                pygame.draw.circle(SCREEN, BLUE, calibration.point, calibration.acceptance_radius)
                text_surface = bold_font.render(f"{iterator}/{n_points}", True, WHITE)
                text_square = text_surface.get_rect(center=calibration.point)
                SCREEN.blit(text_surface, text_square)
            if gestures.whichAlgorithm(context="my_context") == "Ridge":
                pygame.draw.circle(SCREEN, RED, event.point, 50)
            if gestures.whichAlgorithm(context="my_context") == "LassoCV":
                pygame.draw.circle(SCREEN, BLUE, event.point, 50)
            if event.saccades:
                pygame.draw.circle(SCREEN, GREEN, event.point, 50)

        if not calibrate:
            # Move paddle
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.left -= PADDLE_SPEED
            if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
                paddle.right += PADDLE_SPEED

            displacement = event.point[0] - prev_x

            if event.point[0] < SCREEN_WIDTH/2 and paddle.left > 0:
                paddle.left -= PADDLE_SPEED
            if event.point[0] > SCREEN_WIDTH/2 and paddle.right < SCREEN_WIDTH:
                paddle.right += PADDLE_SPEED

            prev_x = event.point[0]

            # Move ball
            ball.left += ball_speed[0]
            ball.top += ball_speed[1]

            # Ball collision with walls
            if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
                ball_speed[0] = -ball_speed[0]
            if ball.top <= 0:
                ball_speed[1] = -ball_speed[1]
            if ball.bottom >= SCREEN_HEIGHT:
                ball.left = SCREEN_WIDTH//2
                ball.top = 60
                lives -= 1
                if lives == 0:
                    pygame.quit()
                    sys.exit()

            # Ball collision with paddle
            if ball.colliderect(paddle):
                ball_speed[1] = -ball_speed[1]

            # Ball collision with bricks
            for brick in bricks[:]:
                if ball.colliderect(brick):
                    ball_speed[1] = -ball_speed[1]
                    bricks.remove(brick)
                    score += 1
                    if score == len(bricks):
                        bricks = [pygame.Rect(10 + i * (BRICK_WIDTH + 10), 10 + j * (BRICK_HEIGHT + 10), BRICK_WIDTH, BRICK_HEIGHT) for i in range(SCREEN_WIDTH%(BRICK_WIDTH+10)) for j in range(5)]

            score_text = SCORE_FONT.render(f'{score}', False, BRICK_COLORS[NUM_LIVES-lives])
            centered_text_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+30))

            # Drawing
            SCREEN.fill(BLACK)
            pygame.draw.rect(SCREEN, BRICK_COLORS[NUM_LIVES-lives], paddle)
            # SCREEN.blit(paddle_img, paddle)
            SCREEN.blit(ball_img, ball)
            SCREEN.blit(score_text, centered_text_rect)
            for brick in bricks:
                SCREEN.blit(brick_imgs[3-lives], brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()