def get_translations(board, piece):
	pside = piece.side
	ptype = piece.type
	x = piece.x
	y = piece.y

	t = []
	legal_t = []

	# pawn
	if ptype == 'P':
		s = (1, -1)[pside == 'w']
		starting_y = (1, 6)[pside == 'w']

		if board.get_cell(x, y+1*s) == None: t.append((0, 1*s)) # one square move forward
		if board.get_cell(x, y+2*s) == None and y == starting_y: t.append((0, 2*s)) # two square move forward
		if not board.get_cell(x-1, y+1*s) == None: t.append((-1, 1*s)) # take left diagonal
		if not board.get_cell(x+1, y+1*s) == None: t.append((1, 1*s)) # take right diagonal

	# knight
	elif ptype == 'N':
		t = [(-1, -2), (1, -2), (-2, -1), (2, -1), (-2, 1), (2, 1), (-1, 2), (1, 2)]

	# king
	elif ptype == 'K':
		t = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

		# TO DO: castling

	# rook
	elif ptype == 'R':
		for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

			lim = 8
			for i in range(1, 8):
				obs_piece = board.get_cell(x+i*dx, y+i*dy)

				# establish limit
				if lim == 8:
					if not obs_piece == None:
						if obs_piece.side == pside: # obstructed by piece on own side
							lim = i-1
						else: # obstructed by piece on opp side (can take)
							lim = i

				if i <= lim:
					t.append((i*dx, i*dy))

	# bishop
	elif ptype == 'B':
		for (dx, dy) in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:

			lim = 8
			for i in range(1, 8):
				obs_piece = board.get_cell(x+i*dx, y+i*dy)

				# establish limit
				if lim == 8:
					if not obs_piece == None:
						if obs_piece.side == pside: # obstructed by piece on own side
							lim = i-1
						else: # obstructed by piece on opp side (can take)
							lim = i

				if i <= lim:
					t.append((i*dx, i*dy))

  
	# validate legality of each move
	for translation in t:
		tx = x+translation[0]
		ty = y+translation[1]

		# check if inside board
		if not 0 <= tx <= 7 or not 0 <= ty <= 7:
			continue

		# check if on own piece
		if not board.get_cell(tx, ty) == None:
			if board.get_cell(tx, ty).side == pside:
				continue

		legal_t.append(translation)
	
	return legal_t