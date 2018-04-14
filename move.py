import piece_rules

class Move:

	def __init__(self, board, piece, to_x, to_y):
		self.piece = piece
		self.to_x = to_x
		self.to_y = to_y

		# determine value gain
		if board.get_cell(self.to_x, self.to_y) == None:
			self.value_gain = 0
		else:
			self.value_gain = piece_rules.values[board.get_cell(self.to_x, self.to_y).type]

	def __repr__(self):
		return "{}{} {} {}".format(self.piece.side, self.piece.type, coords_to_notation(self.piece.x, self.piece.y), coords_to_notation(self.to_x, self.to_y))

def list_side_pieces(board, side):
	pieces = []
	for j in range(8):
		for i in range(8):
			piece = board.get_cell(i, j)
			if not piece == None:
				if piece.side == side:
					pieces.append(piece)

	return pieces

def calc_possible_moves(board, side):
	# side is either 'w' or 'b'
	moves = []
	pieces = list_side_pieces(board, side)
	for piece in pieces:
		ps = calc_possible_piece_moves(board, piece)
		for p in ps:
			moves.append(p)

	return moves

def calc_possible_piece_moves(board, piece):
	pside = piece.side
	ptype = piece.type
	x = piece.x
	y = piece.y

	translations = piece_rules.get_translations(board, piece)
	pos_moves = []

	# check for legality
	for t in translations:
		tx = x+t[0]
		ty = y+t[1]

		pos_moves.append(Move(board, piece, tx, ty))

	return pos_moves

def coords_to_notation(x, y):
	char1 = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')[x]
	char2 = ('8', '7', '6', '5', '4', '3', '2', '1')[y]
	return char1+char2