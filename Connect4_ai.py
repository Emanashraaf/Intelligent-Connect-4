#imports
import tkinter as tk
from tkinter import * 
from tkinter import messagebox
import numpy as np
import sys
import math

#definations
THEM = 1
US = 2
THEM_TURN = 0
US_TURN = 1
game_over = False

#functions
def create_board(Connect4_board):
	canvas.create_rectangle(0, 0, 700, 100, fill="#000000")
	canvas.create_rectangle(0, 100, 700, 700, fill="#0000FF")
	for c in range(7):
		for r in range(6):
			canvas.create_oval(c*100+5, r*100+105, c*100+95, r*100+195,fill="#000000",width=0)
	
	for c in range(7):
		for r in range(6):		
			if Connect4_board[r][c] == THEM:
				canvas.create_oval(c*100+5, r*100+105, c*100+95, r*100+195,fill="#ff0000",width=0)
			elif Connect4_board[r][c] == US:
				canvas.create_oval(c*100+5, r*100+105, c*100+95, r*100+195,fill="#ffd700",width=0)


def avaliable_moves(Connect4_board):
	moves = []
	for col in range(7):
		if Connect4_board[0][col] == 0:
			moves.append(col)
	return moves

def winning_move(Connect4_board, piece):
	# horizontal 
	for col in range(4):
		for row in range(6):
			if (Connect4_board[row][col] == piece and Connect4_board[row][col+1] == piece 
			and Connect4_board[row][col+2] == piece and Connect4_board[row][col+3] == piece):
				return True

	# vertical 
	for col in range(7):
		for row in range(3):
			if (Connect4_board[row][col] == piece and Connect4_board[row+1][col] == piece 
			and Connect4_board[row+2][col] == piece and Connect4_board[row+3][col] == piece):
				return True

	# diaganols
	for col in range(4):
		for row in range(3):
			if (Connect4_board[row][col] == piece and Connect4_board[row+1][col+1] == piece 
			and Connect4_board[row+2][col+2] == piece and Connect4_board[row+3][col+3] == piece):
				return True

	for col in range(4):
		for row in range(3, 6):
			if (Connect4_board[row][col] == piece and Connect4_board[row-1][col+1] == piece 
			and Connect4_board[row-2][col+2] == piece and Connect4_board[row-3][col+3] == piece):
				return True


def calc_score(window, piece):
	score = 0
	opp_piece = 1
	if piece == 1:
		opp_piece = 2

	if window.count(piece) == 4:
		score += 50
	elif window.count(piece) == 3 and window.count(0) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(0) == 2:
		score += 5

	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score -= 6

	return score


def utility(Connect4_board, piece):
	score = 0

	## Center
	center_array = [int(i) for i in list(Connect4_board[:, 3])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Horizontal
	for r in range(6):
		row_window = [i for i in list(Connect4_board[r,:])]
		for c in range(4):
			window = row_window[c:c+4]
			score += calc_score(window, piece)

	## Vertical
	for c in range(7):
		col_window = [i for i in list(Connect4_board[:,c])]
		for r in range(3):
			window = col_window[r:r+4]
			score += calc_score(window, piece)

	## diagonal
	for r in range(3):
		for c in range(4):
			window = [Connect4_board[r+i][c+i] for i in range(4)]
			score += calc_score(window, piece)

	for r in range(3):
		for c in range(4):
			window = [Connect4_board[r+3-i][c+i] for i in range(4)]
			score += calc_score(window, piece)

	return score



def minimax(Connect4_board, depth, alpha, beta, maximizer):
	aval_moves = avaliable_moves(Connect4_board)
	if winning_move(Connect4_board, US) :
		return (None, 100000000000000)
	elif winning_move(Connect4_board, THEM):
		return (None, -10000000000000)
	elif len(aval_moves) == 0 : 
		return (None, 0)
	elif depth == 0 :
		return (None, utility(Connect4_board, US))


	if maximizer:
		temp_alpha = -math.inf
		column = aval_moves[0]  #initialization

		for c in aval_moves:
			for r in range(6):
				if Connect4_board[r][c] == 0:
					row = r

			b_copy = Connect4_board.copy()
			b_copy[row][c] = US
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > temp_alpha:
				temp_alpha = new_score
				column = c
			alpha = max(alpha, temp_alpha)
			if alpha >= beta:
				break
		return column, temp_alpha

	else: # Minimizer
		temp_beta = math.inf
		column = aval_moves[0]

		for c in aval_moves:
			for r in range(6):
				if Connect4_board[r][c] == 0:
					row = r

			b_copy = Connect4_board.copy()
			b_copy[row][c] = THEM
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < temp_beta:
				temp_beta = new_score
				column = c
			beta = min(beta, temp_beta)
			if alpha >= beta:
				break
		return column, temp_beta

def mouse_motion(event):
    x, y = event.x, event.y
    canvas.create_rectangle(0, 0, 700, 100, fill="#000000")
    canvas.create_oval(x-45, 5, x+45, 95,fill="#FF0000",width=0)

def mouse_click(event):
    global turn
    x = event.x
    canvas.create_rectangle(0, 0, 700, 100, fill="#000000")
    col = int(math.floor(x/100))
    
    if (Connect4_board[0][col] == 0):
    	for r in range(6):
    		if Connect4_board[5-r][col] == 0:
    			row = 5-r
    			break
    	Connect4_board[row][col] = THEM

    	global turn
    	turn += 1
    	turn = turn % 2
    	create_board(Connect4_board)

    	if winning_move(Connect4_board, THEM):
    		global game_over
    		game_over = True
    		result = tk.messagebox.showinfo('Congratulations','you wins!')
    		sys.exit()
    	num_zeros = (Connect4_board == 0).sum()
    	if num_zeros == 0 :
    		result = tk.messagebox.showinfo('EXIT','GAME OVER!')
    		sys.exit()

def mouse_release(event):
    col, score = minimax(Connect4_board, 3, -math.inf, math.inf, True)
    if (Connect4_board[0][col] == 0):
    	for r in range(6):
    		if Connect4_board[5-r][col] == 0:
    			row = 5-r
    			break

    	Connect4_board[row][col] = US
    	create_board(Connect4_board)
    	if winning_move(Connect4_board, US):
    		result = tk.messagebox.showinfo('Hard Luck','Computer wins!')
    		game_over = True
    		sys.exit()
    	num_zeros = (Connect4_board == 0).sum()
    	if num_zeros == 0 :
    		result = tk.messagebox.showinfo('EXIT','GAME OVER!')
    		sys.exit()

#########################################################################################    		
#board creation 
Connect4_board = np.zeros((6,7))

#asking for player want to play first or not!
root = tk.Tk()
result = tk.messagebox.askquestion('Start Game','Do you want to start the game?')
if result == 'yes':
	turn = THEM_TURN
else:
	turn = US_TURN

#drawing
canvas = Canvas (root,width = 700,height = 700)
create_board(Connect4_board)

while not game_over:
	if turn == THEM_TURN:
		# Mouse Motion Event
		root.bind('<Motion>', mouse_motion)
		# Mouse Click Event		
		root.bind('<Button>', mouse_click)
        # Mouse Release Event
		root.bind('<ButtonRelease>' , mouse_release)

	if turn == US_TURN:
        #this for the first time AI plays
		col, score = minimax(Connect4_board, 5, -math.inf, math.inf, True)

		if Connect4_board[5][col] == 0:
			for r in range(6):
			   if Connect4_board[r][col] == 0:
			   	 row = r
			Connect4_board[row][col] = US

			turn += 1
			turn = turn % 2
			create_board(Connect4_board)

		# Mouse Motion Event
		root.bind('<Motion>', mouse_motion)
		# Mouse Click Event		
		root.bind('<Button>', mouse_click)
        # Mouse Release Event
		root.bind('<ButtonRelease>' , mouse_release)
	canvas.pack()
	root.mainloop()