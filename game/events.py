def click(mouse_pos, board, padding, tile_size):
    mouse_x, mouse_y = mouse_pos
    pad_x, pad_y = padding
    x, y = (mouse_x - pad_x) // tile_size, (mouse_y - pad_y) // tile_size

    if not (0 <= x < 8 and 0 <= y < 8):
        return board.reset_selected()

    if board.current:
        if (x, y) in board.valid_moves:
            return board.move(board.current, (x, y))

        piece = board.board[y][x]
        board.current.dragged = False

        if board.current.first_select or (piece and piece != board.current):
            board.current.first_select = False
            return

    board.reset_selected()


def drag(mouse_pos, board, padding, tile_size):
    mouse_x, mouse_y = mouse_pos
    pad_x, pad_y = padding
    x, y = (mouse_x - pad_x) // tile_size, (mouse_y - pad_y) // tile_size

    if not (0 <= x < 8 and 0 <= y < 8):
        return board.reset_selected()

    piece = board.board[y][x]

    if not piece or piece.dragged:
        return

    if board.current and (x, y) in board.valid_moves:
        return board.move(board.current, (x, y))

    if piece != board.current:
        board.reset_selected()

    if not board.current:
        board.select(piece)
        piece.first_select = True

    piece.dragged = True
