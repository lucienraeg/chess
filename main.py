import tdl
import numpy as np
import colors as col
import move as move

CON_WIDTH, CON_HEIGHT = 92, 56
STATUS_WIDTH, STATUS_HEIGHT = 12, 2
GRAVE_WIDTH, GRAVE_HEIGHT = 12, 4

SCREEN_WIDTH = CON_WIDTH
SCREEN_HEIGHT = STATUS_HEIGHT+CON_HEIGHT

class Piece():
	
	def __init__(self, pside, ptype, x, y):
		self.side = pside
		self.type = ptype
		self.x = x
		self.y = y

	def __repr__(self):
		return "{}{}".format(self.side, self.type)

class Board():

	def __init__(self, title='        '):
		self.title = title
		self.cells = np.array([[None]*8]*8)
		self.highlighted_cells_green = []
		self.highlighted_cells_blue = []
		self.grave_pieces = []

	def wipe(self):
		self.cells = np.array([[None]*8]*8)
		self.highlighted_cells_green = []
		self.highlighted_cells_blue = []
		self.title = '        '

	def get_cell(self, x, y):
		if not 0 <= x <= 7 or not 0 <= y <= 7:
			return None
		return self.cells[x, y]

	def place_piece(self, piece):
		self.cells[piece.x, piece.y] = piece

	def remove_piece(self, piece):
		self.cells[piece.x, piece.y] = None

	def move_piece(self, m):
		piece = m.piece
		x = piece.x
		y = piece.y
		to_x = m.to_x
		to_y = m.to_y

		# take piece
		if not self.get_cell(to_x, to_y) == None:
			self.grave_pieces.append(self.get_cell(to_x, to_y))

		# apply changes
		self.place_piece(Piece(piece.side, piece.type, to_x, to_y))
		self.remove_piece(piece)

	def standard_setup(self):
		# black
		self.place_piece(Piece('b', 'R', 0, 0))
		self.place_piece(Piece('b', 'N', 1, 0))
		self.place_piece(Piece('b', 'B', 2, 0))
		self.place_piece(Piece('b', 'Q', 3, 0))
		self.place_piece(Piece('b', 'K', 4, 0))
		self.place_piece(Piece('b', 'B', 5, 0))
		self.place_piece(Piece('b', 'N', 6, 0))
		self.place_piece(Piece('b', 'R', 7, 0))
		self.place_piece(Piece('b', 'P', 0, 1))
		self.place_piece(Piece('b', 'P', 1, 1))
		self.place_piece(Piece('b', 'P', 2, 1))
		self.place_piece(Piece('b', 'P', 3, 1))
		self.place_piece(Piece('b', 'P', 4, 1))
		self.place_piece(Piece('b', 'P', 5, 1))
		self.place_piece(Piece('b', 'P', 6, 1))
		self.place_piece(Piece('b', 'P', 7, 1))

		# white
		self.place_piece(Piece('w', 'R', 0, 7))
		self.place_piece(Piece('w', 'N', 1, 7))
		self.place_piece(Piece('w', 'B', 2, 7))
		self.place_piece(Piece('w', 'Q', 3, 7))
		self.place_piece(Piece('w', 'K', 4, 7))
		self.place_piece(Piece('w', 'B', 5, 7))
		self.place_piece(Piece('w', 'N', 6, 7))
		self.place_piece(Piece('w', 'R', 7, 7))
		self.place_piece(Piece('w', 'P', 0, 6))
		self.place_piece(Piece('w', 'P', 1, 6))
		self.place_piece(Piece('w', 'P', 2, 6))
		self.place_piece(Piece('w', 'P', 3, 6))
		self.place_piece(Piece('w', 'P', 4, 6))
		self.place_piece(Piece('w', 'P', 5, 6))
		self.place_piece(Piece('w', 'P', 6, 6))
		self.place_piece(Piece('w', 'P', 7, 6))

def handle_keys():

	global selx, sely, alt_board, legal_move_coords, holding_piece, holding_piece_from

	user_input = tdl.event.key_wait()

	# movement
	if user_input.key == 'UP' or user_input.key == 'DOWN' or user_input.key == 'LEFT' or user_input.key == 'RIGHT':

		# sel movement
		if user_input.key == 'UP':
			sely -= 1
		elif user_input.key == 'DOWN':
			sely += 1
		elif user_input.key == 'LEFT':
			selx -= 1
		elif user_input.key == 'RIGHT':
			selx += 1

	# calc possible moves
	elif user_input.char == 'z':
		for alt_board in alt_boards: alt_board.wipe()

		if main_board.get_cell(selx, sely) == None:
			legal_move_coords = []
		else:
			# pos_moves = move.calc_possible_piece_moves(main_board, main_board.get_cell(selx, sely))
			pos_moves = move.calc_possible_moves(main_board, main_board.get_cell(selx, sely).side)

			for i, pos_move in enumerate(pos_moves):
				alt_boards[i].cells = np.copy(main_board.cells) # fill alt board with main board pieces
				alt_boards[i].move_piece(pos_move) # make pos move on board
				alt_boards[i].title = str(pos_move) # set title to move repr

	# move piece
	elif user_input.char == 'x':
		# pick up piece
		if holding_piece == None:
			if not main_board.get_cell(selx, sely) == None:

				# take piece and set up legal moves
				piece = main_board.get_cell(selx, sely)
				pos_moves = move.calc_possible_piece_moves(main_board, main_board.get_cell(selx, sely))
				legal_move_coords = [(pos_move.to_x, pos_move.to_y) for pos_move in pos_moves]
				main_board.highlighted_cells_green = legal_move_coords
				main_board.remove_piece(piece)

				# set holding piece data
				holding_piece_from = (selx, sely)
				holding_piece = piece
		# move
		else:
			if ((selx, sely) in legal_move_coords) or ((selx, sely) == holding_piece_from):

				# move piece
				if ((selx, sely)) in legal_move_coords:
					main_board.move_piece(move.Move(holding_piece, selx, sely))
				# put piece back
				else:
					main_board.place_piece(Piece(holding_piece.side, holding_piece.type, selx, sely))

				# clear
				main_board.highlighted_cells_green = []
				holding_piece = None



	selx = clamp(selx, 0, 7)
	sely = clamp(sely, 0, 7)

def draw_board(b, xoffset, yoffset, draw_coords=False, draw_sel=False, style=0):

	# styles
	# 0: gray checkered board, black and white piecse
	# 1: dot board, brown and beige pieces

	piece_colors = ((col.BLACK, col.WHITE), (col.BROWN, col.BEIGE))[style]

	xoffset = xoffset
	yoffset = yoffset

	# draw coords
	if draw_coords:
		for i, c in enumerate(['8', '7', '6', '5', '4', '3', '2', '1']):
			con.draw_char(xoffset-1, yoffset+i, c, (col.DK_GRAY, col.BLUE)[i == sely])

		for i, c in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']):
			con.draw_char(xoffset+i, yoffset-1, c, (col.DK_GRAY, col.BLUE)[i == selx])

	# draw title
	if not b.title == '':
		con.draw_str(xoffset, yoffset+8, b.title, col.BLUE)

	# draw all cells
	for y in range(8):
		for x in range(8):

			if style == 0:
				char = ' '
				fg_color = None
				bg_color = (col.LT_GRAY, col.DK_GRAY)[(y+(x%2==0))%2==0]
			if style == 1:
				char = 250
				fg_color = col.DK_GRAY
				bg_color = col.BLACK

			# get piece info
			piece = b.get_cell(x, y)
			if not piece == None:
				char = piece_char_indicies[piece.type]
				fg_color = piece_colors[piece.side == 'w']

			# draw tile details
			if (draw_sel and (x, y) == (selx, sely)) or (x, y) in b.highlighted_cells_blue:

				bg_color = col.BLUE
			elif (x, y) in b.highlighted_cells_green:
				if piece == None:
					fg_color = col.GREEN
					char = 249
				else:
					bg_color = col.GREEN

			# tile
			con.draw_char(xoffset+x, yoffset+y, char, fg=fg_color, bg=bg_color)

def draw_status():
	for x in range(STATUS_WIDTH):
		status.draw_char(x, 1, 205, col.WHITE)	

	# draw sel cursor info
	status.draw_str(0, 0, "{}".format(move.coords_to_notation(selx, sely)), col.WHITE)
	if not main_board.get_cell(selx, sely) == None:
		piece = main_board.get_cell(selx, sely)
		status.draw_char(2, 0, piece.side, col.WHITE)
		status.draw_char(3, 0, piece_char_indicies[piece.type], col.GREEN)
	else:
		status.draw_char(2, 0, '-', col.GRAY)
		status.draw_char(3, 0, '-', col.GRAY)

	# draw holidng piece info
	if not holding_piece == None:
		status.draw_char(STATUS_WIDTH-2, 0, holding_piece.side, col.WHITE)
		status.draw_char(STATUS_WIDTH-1, 0, piece_char_indicies[holding_piece.type], col.GREEN)
	else:
		status.draw_char(STATUS_WIDTH-2, 0, '-', col.GRAY)
		status.draw_char(STATUS_WIDTH-1, 0, '-', col.GRAY)

def draw_grave(board):
	for x in range(GRAVE_WIDTH):
		grave.draw_char(x, 0, 205, col.WHITE)

	for x in range(GRAVE_WIDTH):
		for y in range(GRAVE_HEIGHT-1):
			grave.draw_char(x, y+1, 250, col.LT_GRAY)

	for i, piece in enumerate(board.grave_pieces):
		xx = i % 12
		yy = i // 12 + 1
		grave.draw_char(xx, yy, piece_char_indicies[piece.type], (col.BROWN, col.BEIGE)[piece.side == 'w'], None)

def clamp(x, a, b):
	return max(a, min(b, x))

# init
tdl.set_font('fonts/terminal16x16chess.png', greyscale=True, altLayout=False)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='roguelike', fullscreen=False)
status = tdl.Console(STATUS_WIDTH, STATUS_HEIGHT)
con = tdl.Console(CON_WIDTH, CON_HEIGHT)
grave = tdl.Console(GRAVE_WIDTH, GRAVE_HEIGHT)
selx, sely = 0, 0

# board info
piece_char_indicies = {'K': 6, 'Q': 5, 'B': 4, 'N': 3, 'R': 2, 'P': 1, '-': 0}

# create main board and misc
main_board = Board()
main_board.standard_setup()
holding_piece = None
holding_piece_from = (0, 0)
legal_move_coords = []

# create alt boards
alt_boards = [Board() for i in range(40)]

# main loop
while not tdl.event.is_window_closed():

	# draw status and grave
	draw_status()
	draw_grave(main_board)

	# draw boards
	draw_board(main_board, 2, 2, draw_coords=True, draw_sel=True, style=1)
	for i, alt_board in enumerate(alt_boards):
		xx = i % 8
		yy = i // 8

		x = 17+(xx*9)
		y = 2+(yy*10)

		draw_board(alt_board, x, y, style=1)

	root.blit(status, 0, 0, SCREEN_WIDTH, STATUS_HEIGHT, 0, 0)
	root.blit(con, 0, 2, CON_WIDTH, CON_HEIGHT, 0, 0)
	root.blit(grave, 0, 14, GRAVE_WIDTH, GRAVE_HEIGHT, 0, 0)
	tdl.flush()

	exit_game = handle_keys()
	if exit_game:
		break