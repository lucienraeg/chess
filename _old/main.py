import tdl
import numpy as np
import colors as col
import move as move

CON_WIDTH, CON_HEIGHT = 54, 54

STATUS_WIDTH, STATUS_HEIGHT = 14, 2

SCREEN_WIDTH = CON_WIDTH
SCREEN_HEIGHT = STATUS_HEIGHT+CON_HEIGHT

def handle_keys():

	global selx, sely, alt_board

	user_input = tdl.event.key_wait()

	# movement
	if user_input.key == 'UP':
		sely -= 1
	elif user_input.key == 'DOWN':
		sely += 1
	elif user_input.key == 'LEFT':
		selx -= 1
	elif user_input.key == 'RIGHT':
		selx += 1
	elif user_input.char == 'z':
		pos_moves = move.calculate_possible_moves(board, selx, sely)

		for i, pos_move in enumerate(pos_moves):
			alt_boards[i] = move.apply_move_to_board(board, pos_move)
			print(alt_boards[i])
		

	selx = clamp(selx, 0, 7)
	sely = clamp(sely, 0, 7)

def get_piece_side(piece):
	if not piece == None:
		return list(piece)[0]
	else:
		return '-'

def get_piece_type(piece):
	if not piece == None:
		return list(piece)[2]
	else:
		return '-'

def coords_to_notation(x, y):
	char1 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')[x]
	char2 = str(y+1)
	return char1+char2

def create_board():

	board = np.array([[None]*8]*8)

	# black
	board[:, 1] = 'B P'
	board[0, 0] = 'B R'
	board[1, 0] = 'B N'
	board[2, 0] = 'B B'
	board[3, 0] = 'B Q'
	board[4, 0] = 'B K'
	board[5, 0] = 'B B'
	board[6, 0] = 'B N'
	board[7, 0] = 'B R'

	# white side
	board[:, 6] = 'W P'
	board[0, 7] = 'W R'
	board[1, 7] = 'W N'
	board[2, 7] = 'W B'
	board[3, 7] = 'W Q'
	board[4, 7] = 'W K'
	board[5, 7] = 'W B'
	board[6, 7] = 'W N'
	board[7, 7] = 'W R'

	return board

def draw_board(b, xoffset, yoffset, draw_coords=False, draw_border=False, draw_selection=False, top_text=None):

	xoffset = xoffset
	yoffset = yoffset

	# draw text
	if not top_text == None:
		con.draw_str(xoffset, yoffset-1, "{}".format(top_text), col.RED)

	# draw coords
	if draw_coords:
		for i in range(8):
			con.draw_char(xoffset-2, yoffset+i, str(i+1), col.DK_GRAY)

		for i, c in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
			con.draw_char(xoffset+i, yoffset-2, c, col.DK_GRAY)

	# draw border
	if draw_border:
		border_color = col.WHITE
		for i in range(8):
			con.draw_char(xoffset-1, yoffset+i, 186, border_color)
			con.draw_char(xoffset+8, yoffset+i, 186, border_color)
			con.draw_char(xoffset+i, yoffset-1, 205, border_color)
			con.draw_char(xoffset+i, yoffset+8, 205, border_color)
		
		con.draw_char(xoffset-1, yoffset-1, 201, border_color)
		con.draw_char(xoffset-1, yoffset+8, 200, border_color)
		con.draw_char(xoffset+8, yoffset-1, 187, border_color)
		con.draw_char(xoffset+8, yoffset+8, 188, border_color)		

	# draw all cells
	for y in range(8):
		for x in range(8):

			# tile
			bg_color = (col.LT_GRAY, col.DK_GRAY)[(y+(x%2==0))%2==0]

			# draw selection
			if draw_selection and (x, y) == (selx, sely):
				bg_color = col.GREEN

			# piece
			char = ' '
			fg_color = col.WHITE
			if not b[x, y] == None:
				side = get_piece_side(b[x, y])
				piece = get_piece_type(b[x, y])
				char = piece_char_indicies[piece]

				fg_color = {'W': col.WHITE, 'B': col.BLACK}[side]

			# tile
			con.draw_char(xoffset+x, yoffset+y, char, fg=fg_color, bg=bg_color)

def draw_status():
	for x in range(STATUS_WIDTH):
		status.draw_char(x, 1, 205, col.WHITE)

	status.draw_char(0, 0, get_piece_side(board[selx, sely]), col.WHITE)
	status.draw_char(1, 0, piece_char_indicies[get_piece_type(board[selx, sely])], col.GREEN)
	status.draw_str(2, 0, "{}".format(coords_to_notation(selx, sely)), col.WHITE)

def clamp(x, a, b):
	return max(a, min(b, x))

# init

tdl.set_font('fonts/terminal16x16chess.png', greyscale=True, altLayout=False)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='roguelike', fullscreen=False)
con = tdl.Console(CON_WIDTH, CON_HEIGHT)
status = tdl.Console(STATUS_WIDTH, STATUS_HEIGHT)
selx, sely = 0, 0

# board

pieces = ['K', 'Q', 'B', 'N', 'R', 'P']
piece_char_indicies = {'K': 6, 'Q': 5, 'B': 4, 'N': 3, 'R': 2, 'P': 1, '-': 0}
board = create_board()
alt_boards = np.array([create_board() for i in range(4)])

# main loop

while not tdl.event.is_window_closed():
	
	# draw board
	draw_board(board, 3, 3, draw_coords=True, draw_border=True, draw_selection=True)

	# draw alt boards
	for i, alt_board in enumerate(alt_boards):
		draw_board(alt_board, 16+(9*i), 3, top_text=str(i))	

	# draw panel
	draw_status()

	root.blit(status, 0, 0, SCREEN_WIDTH, STATUS_HEIGHT, 0, 0)
	root.blit(con, 0, 2, CON_WIDTH, CON_HEIGHT, 0, 0)
	tdl.flush()

	exit_game = handle_keys()
	if exit_game:
		break