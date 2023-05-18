import pygame, random, sys
from pygame.locals import QUIT, K_UP, K_DOWN, K_w, K_s

pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 400
FPS = 60
PADDLE_COL = (252, 252, 252)
BG_COL = (49, 95, 48)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")
clock = pygame.time.Clock()

# Set up game variables
paddle_width = 12
paddle_height = 65
ball_radius = 13
ball_speed_x = 5
ball_speed_y = 5
paddle_speed = 5
countdown = 3
bounce_count = 0

player_score = 0
ai_score = 0

# Create the player paddles
player1 = pygame.Rect(25, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
player2 = pygame.Rect(WIDTH - 25 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Create the ball
ball = pygame.Rect(WIDTH // 2 - ball_radius // 2, HEIGHT // 2 - ball_radius // 2, ball_radius, ball_radius)
ball_speed = [random.choice([-1, 1]) * ball_speed_x, random.choice([-1, 1]) * ball_speed_y]

# AI variables
ai_speed = paddle_speed
depth = 1

# Game Loop
running = True
while running:    
    # Functions
    # Resetting the game
    def reset_game():
        # Reset player paddle positions
        player1.y = HEIGHT // 2 - paddle_height // 2
        player2.y = HEIGHT // 2 - paddle_height // 2

        # Reset ball position and speed
        ball.x = WIDTH // 2 - ball_radius // 2
        ball.y = HEIGHT // 2 - ball_radius // 2
        ball_speed[0] = random.choice([-1, 1]) * ball_speed_x
        ball_speed[1] = random.choice([-1, 1]) * ball_speed_y
        
        pygame.time.delay(1000)
        
        
    # Minimax algorithm
    def minimax_search(state, depth, is_maximizing):
        if depth == 0 or is_terminal(state):
            return evaluate_state(state)

        if is_maximizing:
            best_score = float('-inf')
            for action in possible_actions(state):
                new_state = perform_action(state, action)
                score = minimax_search(new_state, depth - 1, False)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for action in possible_actions(state):
                new_state = perform_action(state, action)
                score = minimax_search(new_state, depth - 1, True)
                best_score = min(best_score, score)
            return best_score
        
    # IDS
    def iterative_deepening_search(state, depth_limit):
        best_action = None
        for depth in range(1, depth_limit + 1):
            best_score = float('-inf')
            for action in possible_actions(state):
                new_state = perform_action(state, action)
                score = minimax_search(new_state, depth, True)
                if score > best_score:
                    best_score = score
                    best_action = action
            if best_action:
                return best_action
        return best_action
        
    # Function for evaluating game state
    def evaluate_state(state):
        player2_y = state
        ball_distance = abs(player2_y - ball.y)
        return -ball_distance
        
    # AI's possible actions
    def possible_actions(state):
        actions = ['up', 'down']
        return actions
    
    # Check if ball has reached either players' side
    def is_terminal(state):
        # Check if the ball has reached the player's side or the AI's side
        return ball.x <= 0 or ball.x >= WIDTH - ball_radius
    
    # Move the player2's y-axis based on the best action
    def perform_action(state, action):
        player2_y = state
        # Update the AI's paddle position based on the chosen action
        if action == 'up' and player2_y > 0:
            player2_y -= ai_speed
        elif action == 'down' and player2_y < HEIGHT - paddle_height:
            player2_y += ai_speed
        return player2_y
    
    ai_action = iterative_deepening_search(player2.y, depth)
    
    if ai_action == 'up' and player2.y > 0:
        player2.y -= ai_speed
    elif ai_action == 'down' and player2.y < HEIGHT - paddle_height:
        player2.y += ai_speed
    
    # Handling exit
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # Move player paddle
    keys = pygame.key.get_pressed()
    if (keys[K_UP] or keys[K_w]) and player1.y > 0:
        player1.y -= paddle_speed
    if (keys[K_DOWN] or keys[K_s]) and player1.y < HEIGHT - paddle_height:
        player1.y += paddle_speed
        
    # Move the ball
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Collision detection with paddles
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed[0] = -ball_speed[0]
        ball_speed[1] = random.choice([ball_speed[1], -ball_speed[1]])
        if bounce_count < 20:
            ball_speed[0] *= 1.07
            ball_speed[1] *= 1.005
            paddle_speed += 0.1
            bounce_count += 1

    # Collision detection with top/bottom walls
    if ball.y <= 0 or ball.y >= HEIGHT - ball_radius:
        ball_speed[1] = -ball_speed[1]
        
    # Collision detection with left/right walls
    if ball.x <= 0:
        ai_score += 1
        bounce_count = 0
        paddle_speed = 5
        reset_game()
    elif ball.x >= WIDTH - ball_radius:
        player_score += 1
        bounce_count = 0
        paddle_speed = 5
        reset_game()
        
    # Fill the screen with BG_COL
    screen.fill(BG_COL)

    # Draw paddles and ball
    pygame.draw.rect(screen, PADDLE_COL, player1)
    pygame.draw.rect(screen, PADDLE_COL, player2)
    pygame.draw.ellipse(screen, PADDLE_COL, ball)
    
    # Draw texts
    score_font = pygame.font.Font('freesansbold.ttf', 48)
    player_text = score_font.render(str(player_score), True, PADDLE_COL)
    ai_text = score_font.render(str(ai_score), True, PADDLE_COL)
    player_txtrec = player_text.get_rect()
    player_txtrec.left = 300
    player_txtrec.top = 10
    ai_txtrec = ai_text.get_rect()
    ai_txtrec.right = WIDTH - 300 
    ai_txtrec.top = 10
    screen.blit(player_text, player_txtrec)
    screen.blit(ai_text, ai_txtrec)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)
    
# Exit the game
pygame.quit()
sys.exit()