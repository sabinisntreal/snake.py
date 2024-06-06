import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Snake properties
snake_block = 20
snake_speed = 10  # Reduced speed

# Snake
snake = [[WIDTH // 2, HEIGHT // 2]]
snake_direction = 'STOP'

# Food
food = [random.randrange(1, (WIDTH // 20)) * 20, random.randrange(1, (HEIGHT // 20)) * 20]

# Score
score = 0

# High score
high_score = 0

# Functions
def draw_snake(snake):
    pygame.draw.circle(win, GREEN, (snake[0][0] + snake_block // 2, snake[0][1] + snake_block // 2), snake_block // 2)
    for block in snake[1:]:
        pygame.draw.circle(win, BLUE, (block[0] + snake_block // 2, block[1] + snake_block // 2), snake_block // 2)

def draw_food(food, color=RED):
    pygame.draw.circle(win, color, (food[0] + snake_block // 2, food[1] + snake_block // 2), snake_block // 2)

def move_snake(snake, direction):
    if direction == 'UP':
        snake[0][1] -= snake_block
    elif direction == 'DOWN':
        snake[0][1] += snake_block
    elif direction == 'LEFT':
        snake[0][0] -= snake_block
    elif direction == 'RIGHT':
        snake[0][0] += snake_block

def grow_snake(snake):
    snake.append(list(snake[-1]))

def game_over():
    global high_score
    font_style = pygame.font.SysFont(None, 50)
    message = font_style.render("Game Over! Score: " + str(score), True, YELLOW)
    win.blit(message, [WIDTH/5, HEIGHT/3])

    if score > high_score:
        high_score = score
        message = font_style.render("New High Score: " + str(high_score), True, ORANGE)
        win.blit(message, [WIDTH/5, HEIGHT/2])

    pygame.display.update()
    pygame.time.wait(2000)

def reset_game():
    global snake, snake_direction, score
    snake = [[WIDTH // 2, HEIGHT // 2]]
    snake_direction = 'STOP'
    score = 0

# Main loop
clock = pygame.time.Clock()
running = True
paused = True  # Initial state is paused
special_food_counter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_direction = 'UP'
                paused = False
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_direction = 'DOWN'
                paused = False
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_direction = 'LEFT'
                paused = False
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_direction = 'RIGHT'
                paused = False
            elif event.key == pygame.K_SPACE:
                snake_direction = 'STOP'
                paused = True

    if paused:
        continue

    if snake[0] == food:
        score += 10
        special_food_counter += 1
        if special_food_counter == 5:
            score += 40
            draw_food(food, YELLOW)
        else:
            draw_food(food)
        special_food_counter %= 5
        food = [random.randrange(1, (WIDTH // 20)) * 20, random.randrange(1, (HEIGHT // 20)) * 20]
        grow_snake(snake)

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = list(snake[i - 1])
    move_snake(snake, snake_direction)

    if (snake[0][0] >= WIDTH or snake[0][0] < 0 or
        snake[0][1] >= HEIGHT or snake[0][1] < 0 or
        snake[0] in snake[1:]):
        game_over()
        reset_game()
        paused = True

    win.fill(BLACK)
    draw_snake(snake)
    draw_food(food)

    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, WHITE)
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    win.blit(score_text, (10, 10))
    win.blit(high_score_text, (10, 30))

    pygame.display.update()

    clock.tick(snake_speed)

pygame.quit()
