from game.drawing import PAD_X, PAD_Y, TILE_SIZE


def click(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos
    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

    if not (0 <= x < 8 and 0 <= y < 8):
        return board.reset_selected()

    if board.current:
        if (x, y) in board.valid_moves:
            return board.move(board.current, (x, y))

        piece = board.board[y][x]
        board.current.dragged = False

        if board.current.first_select:
            board.current.first_select = False
            return
        elif piece != board.current:
            return

    board.reset_selected()


def drag(mouse_pos, board):
    mouse_x, mouse_y = mouse_pos
    x, y = (mouse_x - PAD_X) // TILE_SIZE, (mouse_y - PAD_Y) // TILE_SIZE

    if not (0 <= x < 8 and 0 <= y < 8):
        return

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
