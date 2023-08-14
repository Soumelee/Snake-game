import numpy as np
import cv2
import random
import time
from enum import Enum

# Constraints
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BLOCK_SIZE = 10
MOVEMENT_DELAY = 0.2

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

# Functions

def is_boundary_collision(snake_head):
    x, y = snake_head
    return x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0

def is_self_collision(snake_position):
    snake_head = snake_position[0]
    return snake_head in snake_position[1:]

def is_eat_apple(score):
    new_apple_position = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                          random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
    score += 1
    return new_apple_position, score

def handle_input(current_direction):
    key = cv2.waitKey(1) & 0xFF
    new_direction = None
    
    if key == 27: # ASCII code for the ESC key
        return False, current_direction
    if key == ord('w') and current_direction != Direction.DOWN:
        return True, Direction.UP
    elif key == ord('a') and current_direction != Direction.RIGHT:
        return True, Direction.LEFT
    elif key == ord('s') and current_direction != Direction.UP:
        return True, Direction.DOWN
    elif key == ord('d') and current_direction != Direction.LEFT:
        return True, Direction.RIGHT
    
    return True, current_direction

# Initialize variables
img = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3), np.uint8)
snake_position = [[250, 250], [240, 250], [230, 250]]
apple_position = [random.randrange(1, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                  random.randrange(1, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]
score = 0
current_direction = Direction.RIGHT

while True:
    cv2.imshow('Snake Game', img)
    key = cv2.waitKey(1) & 0xFF
    img.fill(0)  # Clear the image

    # Display Apple
    cv2.rectangle(img, (apple_position[0], apple_position[1]),
                  (apple_position[0] + BLOCK_SIZE, apple_position[1] + BLOCK_SIZE),
                  (0, 0, 255), 3)
    
    # Display Snake
    for position in snake_position:
        cv2.rectangle(img, (position[0], position[1]),
                      (position[0] + BLOCK_SIZE, position[1] + BLOCK_SIZE),
                      (0, 255, 0), 3)

    time.sleep(MOVEMENT_DELAY)

    # Handle user input and update direction
    should_continue, current_direction = handle_input(current_direction)
    if not should_continue:
        break

    # Update snake's position based on direction
    head_x, head_y = snake_position[0]
    if current_direction == Direction.LEFT:
        head_x -= BLOCK_SIZE
    elif current_direction == Direction.RIGHT:
        head_x += BLOCK_SIZE
    elif current_direction == Direction.UP:
        head_y -= BLOCK_SIZE
    elif current_direction == Direction.DOWN:
        head_y += BLOCK_SIZE

    # Handle collision with apple
    if [head_x, head_y] == apple_position:
        apple_position, score = is_eat_apple(score)
        snake_position.insert(0, [head_x, head_y])
    else:
        snake_position.insert(0, [head_x, head_y])
        snake_position.pop()

    # Check for game over conditions
    if is_boundary_collision([head_x, head_y]) or is_self_collision(snake_position):
        font = cv2.FONT_HERSHEY_SIMPLEX
        img.fill(0)
        cv2.putText(img, f'Your Score is {score}', (140, 250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow('Snake Game', img)
        cv2.waitKey(0)
        cv2.imwrite('snake_game_over.jpg', img)
        break

cv2.destroyAllWindows()
