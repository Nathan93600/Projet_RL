import pygame
import numpy as np
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_SIZE = (700, 600)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Couleurs
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Création de la grille
grid = np.zeros((ROW_COUNT, COLUMN_COUNT))

# Création de la fenêtre
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Puissance 4")

# Fonction pour dessiner la grille
def draw_board(grid):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if grid[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), WINDOW_SIZE[1] - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif grid[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), WINDOW_SIZE[1] - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    pygame.display.update()

# Fonction pour placer un jeton dans une colonne
def drop_piece(grid, row, col, piece):
    grid[row][col] = piece

# Fonction pour vérifier si une colonne est valide (non pleine)
def is_valid_location(grid, col):
    return grid[ROW_COUNT - 1][col] == 0

# Fonction pour trouver la première case vide dans une colonne
def get_next_open_row(grid, col):
    for r in range(ROW_COUNT):
        if grid[r][col] == 0:
            return r

# Fonction pour vérifier s'il y a un gagnant
def winning_move(grid, piece):
    # Vérification des lignes
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if grid[r][c] == piece and grid[r][c + 1] == piece and grid[r][c + 2] == piece and grid[r][c + 3] == piece:
                return True
    # Vérification des colonnes
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if grid[r][c] == piece and grid[r + 1][c] == piece and grid[r + 2][c] == piece and grid[r + 3][c] == piece:
                return True
    # Vérification des diagonales \
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if grid[r][c] == piece and grid[r + 1][c + 1] == piece and grid[r + 2][c + 2] == piece and grid[r + 3][c + 3] == piece:
                return True
    # Vérification des diagonales /
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            if grid[r][c] == piece and grid[r + 1][c - 1] == piece and grid[r + 2][c - 2] == piece and grid[r + 3][c - 3] == piece:
                return True

# Initialisation de la grille de jeu
draw_board(grid)
pygame.display.update()

# Définition des types de joueurs
HUMAN = 0
AI = 1

# Définition des joueurs pour chaque mode de jeu
player1_type = AI  # Change this to select the type of player 1 (HUMAN or AI)
player2_type = HUMAN  # Change this to select the type of player 2 (HUMAN or AI)

# Définition des joueurs
players = {1: player1_type, 2: player2_type}

# Q-learning parameters
alpha = 0.15  # learning rate
gamma = 0.99  # discount factor
epsilon = 0.1  # exploration rate

# Q-table initialization
Q = np.zeros((ROW_COUNT * COLUMN_COUNT, COLUMN_COUNT))

# Boucle du jeu
turn = 0
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if players[turn % 2 + 1] == HUMAN:
            # For human players
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                if is_valid_location(grid, col):
                    row = get_next_open_row(grid, col)
                    drop_piece(grid, row, col, turn % 2 + 1)
                    if winning_move(grid, turn % 2 + 1):
                        print(f"Player {turn % 2 + 1} wins!")
                        game_over = True
                    turn += 1  # Increment turn only if the move is valid

        elif players[turn % 2 + 1] == AI:
            # For AI players
            if not game_over:
                if np.random.uniform(0, 1) < epsilon:
                    col = np.random.choice(np.flatnonzero(grid[ROW_COUNT - 1] == 0))
                else:
                    state = np.ravel(grid)
                    valid_moves = np.flatnonzero(state == 0)
                    max_q_value = float("-inf")
                    best_action = None
                    for move in valid_moves:
                        next_state = grid.copy()
                        row = get_next_open_row(next_state, move % COLUMN_COUNT)
                        drop_piece(next_state, row, move % COLUMN_COUNT, turn % 2 + 1)
                        q_index = np.ravel_multi_index((row, move % COLUMN_COUNT), (ROW_COUNT, COLUMN_COUNT))
                        q_value = np.max(Q[q_index])
                        if q_value > max_q_value:
                            max_q_value = q_value
                            best_action = move % COLUMN_COUNT
                    col = best_action

                if is_valid_location(grid, col):
                    row = get_next_open_row(grid, col)
                    drop_piece(grid, row, col, turn % 2 + 1)
                    if winning_move(grid, turn % 2 + 1):
                        print(f"Player {turn % 2 + 1} wins!")
                        game_over = True
                    turn += 1  # Increment turn only if the move is valid

        draw_board(grid)
        pygame.display.update()

        if game_over:
            pygame.time.wait(3000)
