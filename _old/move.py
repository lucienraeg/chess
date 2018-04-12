
class Move():

	def __init__(self, piece1, x1, y1, piece2, x2, y2):
		self.piece1 = piece1
		self.x1 = x1
		self.y1 = y1

		self.piece2 = piece2
		self.x2 = x2
		self.y2 = y2

	def __repr__(self):
		return "'{}' {} to '{}' {}".format(self.piece1, coords_to_notation(self.x1, self.y1), self.piece2, coords_to_notation(self.x2, self.y2))

def coords_to_notation(x, y):
	char1 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')[x]
	char2 = str(y+1)
	return char1+char2


def calculate_possible_moves(board, x, y):
	piece = board[x, y]
	if not piece == None: piece_side = list(piece)[0]
	else: piece_side = '-'
	if not piece == None: piece_type = list(piece)[2]
	else: piece_type = '-'

	pos_moves = []

	if not piece_side == '-':
		pos_moves.append(Move(piece, x, y, None, x-1, y-1))
		pos_moves.append(Move(piece, x, y, None, x, y-1))
		pos_moves.append(Move(piece, x, y, None, x+1, y-1))

	return pos_moves

def apply_move_to_board(b, m):
	new_board = b

	new_board[m.x2, m.y2] = m.piece1 # put piece in new position
	new_board[m.x1, m.y1] = None # remove original piece from prev location

	return new_board