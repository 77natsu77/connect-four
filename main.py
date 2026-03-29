import numpy as np
import pygame
import sys
import math
import random

colour_blue = (0, 0, 255)
colour_black = (0, 0, 0)
colour_red = (255, 0, 0)
colour_yellow = (255, 255, 0)

row_count = 6
column_count = 7

window_length = 4
empty = 0
ai = 1
player = 0

player_piece = 1
ai_piece = 2

def create_board():
  board = np.zeros((row_count, column_count))
  return board


def drop_piece(board, row, col, piece):
  board[row][col] = piece


def is_valid_location(board, col):#cheks if col if full
  return board[row_count - 1][col] == 0

def get_next_open_row(board, col):
  for r in range(row_count):
    if board[r][col] == 0:
      return r

def print_board(board):
  print(np.flip(board, 0))

def draw_board(board):
  for c in range(column_count):
    for r in range(row_count):
      pygame.draw.rect(screen, colour_blue,
                       (c * square_size, r * square_size + square_size,
                        square_size, square_size))
      pygame.draw.circle(
          screen, colour_black,
          (int(c * square_size + square_size / 2),
           int(r * square_size + square_size + square_size / 2)), radius)

  for c in range(column_count):
    for r in range(row_count):
      if board[r][c] == player_piece:
        pygame.draw.circle(
            screen, colour_red,
            (int(c * square_size + square_size / 2),
             height - int(r * square_size + square_size/ 2)), radius)
      elif board[r][c] == ai_piece:
        pygame.draw.circle(
            screen, colour_yellow,
            (int(c * square_size + square_size / 2),
             height - int(r * square_size + square_size/ 2)), radius)


def winning_move(board, piece):
  # Check horizontal locations for win
  for c in range(column_count - 3):
    for r in range(row_count):
      if board[r][c] == piece and board[r][c + 1] == piece and board[r][
          c + 2] == piece and board[r][c + 3] == piece:
        return True

  # Check vertical locations for win
  for c in range(column_count):
    for r in range(row_count - 3):
      if board[r][c] == piece and board[r + 1][c] == piece and board[
          r + 2][c] == piece and board[r + 3][c] == piece:
        return True
        
  # Check positively sloped diaganols`
  for c in range(column_count-3):
    for r in range(row_count-3):
      if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
        return True

    # Check negatively sloped diaganols`
  for c in range(column_count-3):
    for r in range(3, row_count):
      if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
        return True

def evaluate_window(window, piece):
  score = 0
  opp_piece = player_piece
  if piece == player_piece:
    opp_piece = ai_piece

  if window.count(piece) == 4:
    score += 100
  elif window.count(piece) == 3 and window.count(empty) == 1:
    score += 5
  elif window.count(piece) == 2 and window.count(empty) == 2:
    score += 2
    
  if window.count(opp_piece) == 3 and window.count(empty) == 1:
    score -= 4
  return score

def score_position(board, piece):
  score = 0

  #Score Centre Column
  center_array = [int(i) for i in list(board[:, column_count // 2])]
  centre_count = center_array.count(piece)
  score += centre_count * 3

  #Score Horizontal
  for r in range(row_count):
    row_array = [int(i) for i in list(board[r, :])]
    for c in range(column_count - 3):
      window = row_array[c:c + window_length]
      score += evaluate_window(window, piece)


  #Score Vertical
  for c in range(column_count):
    col_array = [int(i) for i in list(board[: , c])]
    for r in range(row_count - 3):
      window = col_array[r:r + window_length]
      score += evaluate_window(window, piece)

  #Score Positive Sloped Diagonal
  for r in range(row_count - 3):
    for c in range(column_count - 3):
      window = [board[r + i][c + i] for i in range(window_length)]
      score += evaluate_window(window, piece)

  #Score Negative Sloped Diagonal
  for r in range(row_count - 3):
    for c in range(column_count - 3):
      window = [board[r + 3 - i][c + i] for i in range(window_length)]
      score += evaluate_window(window, piece)

  return score

def is_terminal_node(board):
  return winning_move(board, player_piece) or winning_move(board, ai_piece) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):#depth controls how smath the ai is basically
  valid_locations = get_valid_locations(board)
  is_terminal = is_terminal_node(board)
  if depth == 0 or is_terminal:
    if is_terminal:
      if winning_move(board, ai_piece):
        return (None, 100000000000000)
      elif winning_move(board, player_piece):
        return (None, -10000000000000)
      else:  # Game is over, no more valid moves
        return (None, 0)
    else:  # Depth is zero
      return (None, score_position(board, ai_piece))
  if maximizingPlayer:
    value = -math.inf
    column = random.choice(valid_locations)
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, ai_piece)
      new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
      if new_score > value:
        value = new_score
        column = col
      alpha = max(alpha, value)
      if alpha >= beta:
        break
    return column, value
    
  else: # Minimizing player
    value = math.inf
    column = random.choice(valid_locations)
    for col in valid_locations:
      row = get_next_open_row(board, col)
      b_copy = board.copy()
      drop_piece(b_copy, row, col, player_piece)
      new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
      if new_score < value:
        value = new_score
        column = col
      beta = min(beta, value)
      if alpha >= beta:
        break
    return column, value

def get_valid_locations(board):
  valid_locations = []
  for col in range(column_count):
    if is_valid_location(board, col):
      valid_locations.append(col)
  return valid_locations
  
board = create_board()
game_over = False
print_board(board)

pygame.init()

square_size = 100
width = column_count * square_size
height = (row_count + 1) * square_size
size = (width, height)

radius = int(square_size / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 75)

turn = random.randint(player, ai)

while not game_over:
 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
      pygame.quit()

    if event.type == pygame.MOUSEMOTION:
      pygame.draw.rect(screen, colour_black, (0, 0, width, square_size))
      posx = event.pos[0]
      if turn == 0:
        pygame.draw.circle(screen, colour_red, (posx, int(square_size / 2)),
                           radius)
      else:
        pygame.draw.circle(screen, colour_yellow, (posx, int(square_size / 2)),
                           radius)
    if event.type == pygame.MOUSEBUTTONDOWN:
      pygame.draw.rect(screen, colour_black, (0, 0, width, square_size))
      # Ask for Player 1 Input
      posx = event.pos[0]
      col = int(math.floor(posx / square_size))#rounds down so it doesnt go down
      #math.ceil rounds up
      if turn == player:
        if is_valid_location(board, col):
          row = get_next_open_row(board , col)
          drop_piece(board ,row , col , player_piece)
          if winning_move(board, player_piece):
            label = font.render("Player 1 wins!!", 1, colour_red)
            screen.blit(label, (40, 10))
            game_over = True

          turn +=1
          turn = turn % 2
          
          print_board(board)
          draw_board(board)
          
    if turn == ai and not game_over:
      col = random.randint( 0 , column_count - 1)
      col , minimax_score = minimax(board, 5, -math.inf, math.inf, True)
      
      if is_valid_location(board, col):
        row = get_next_open_row(board , col)
        drop_piece(board ,row , col , ai_piece)
        if winning_move(board, ai_piece):
          label = font.render("Player 2 wins!!", 1, colour_yellow)
          screen.blit(label, (40, 10))
          game_over = True

      print_board(board)
      draw_board(board)
      turn += 1
      turn = turn % 2
        
    pygame.display.update()
  if game_over:
    pygame.time.wait(3000)  # 3000 milliseconds = 3 seconds
