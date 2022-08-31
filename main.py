import pygame


# Nodes represent the squares on the board and may contain pieces
class Node(object):
    def __init__(self, x, y):
        self.piece = None
        self.col = x
        self.row = y
        self.selected = False
        self.open = False

    def __init__(self, piece, x, y):
        self.piece = piece
        self.col = x
        self.row = y
        self.selected = False
        self.open = False

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def get_piece_img(self):
        return self.piece.get_img()

    def get_col(self):
        return self.col

    def set_col(self, col):
        self.col = col

    def get_row(self):
        return self.row

    def set_row(self, row):
        self.row = row

    # Selected returns true if the node has been clicked
    def get_selected(self):
        return self.selected

    def set_selected(self, selected):
        self.selected = selected

    # Open returns true if the piece can be moved here
    def get_open(self):
        return self.open

    def set_open(self):
        self.open = True

    def set_closed(self):
        self.open = False


# Piece represents an actual chess piece: King, Queen, Pawn...
class Piece(object):
    def __init__(self, name, white, img):
        self.name = name
        self.white = white
        self.first_move = True
        self.check = False
        if white:
            self.wImg = pygame.image.load(img)
        else:
            self.bImg = pygame.image.load(img)

    def set_check(self, check):
        self.check = check

    def get_check(self):
        return self.check

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_white(self, white):
        self.white = white

    def get_white(self):
        return self.white

    def get_first(self):
        return self.first_move

    def moved(self):
        self.first_move = False

    def get_img(self):
        if self.white:
            return self.wImg
        else:
            return self.bImg


class Board(object):
    width = 800
    height = 800

    def __init__(self):
        self.w_check = False
        self.b_check = False
        self.check_list = []
        self.board = [['' for i in range(8)] for i in range(8)]
        self.board[0] = [Node(Piece('r', False, 'bRook.png'), 0, 0), Node(Piece('kn', False, 'bKnight.png'), 1, 0),
                         Node(Piece('b', False, 'bBishop.png'), 2, 0), Node(Piece('q', False, 'bQueen.png'), 3, 0),
                         Node(Piece('k', False, 'bKing.png'), 4, 0), Node(Piece('b', False, 'bBishop.png'), 5, 0),
                         Node(Piece('kn', False, 'bKnight.png'), 6, 0), Node(Piece('r', False, 'bRook.png'), 7, 0)]
        self.board[1] = [Node(Piece('p', False, 'bPawn.png'), i, 1) for i in range(8)]
        for k in range(2, 6):
            self.board[k] = [Node(None, 0, k), Node(None, 1, k),
                             Node(None, 2, k), Node(None, 3, k),
                             Node(None, 4, k), Node(None, 5, k),
                             Node(None, 6, k), Node(None, 7, k)]
        self.board[6] = [Node(Piece('p', True, 'wPawn.png'), i, 6) for i in range(8)]
        self.board[7] = [Node(Piece('r', True, 'wRook.png'), 0, 7), Node(Piece('kn', True, 'wKnight.png'), 1, 7),
                         Node(Piece('b', True, 'wBishop.png'), 2, 7), Node(Piece('q', True, 'wQueen.png'), 3, 7),
                         Node(Piece('k', True, 'wKing.png'), 4, 7), Node(Piece('b', True, 'wBishop.png'), 5, 7),
                         Node(Piece('kn', True, 'wKnight.png'), 6, 7), Node(Piece('r', True, 'wRook.png'), 7, 7)]

    def get_w_check(self):
        return self.w_check

    def set_w_check(self):
        self.w_check = True

    def get_b_check(self):
        return self.b_check

    def set_b_check(self):
        self.b_check = True

    def get_board(self):
        return self.board

    def get_node(self, i, j):
        return self.board[i][j]

    def get_list(self):
        return self.check_list

    def clear_list(self):
        self.check_list = []

    def check_movement(self, node):
        piece_name = node.get_piece().get_name()
        row = node.get_row()
        col = node.get_col()
        if piece_name is 'p':
            self.pawn_move(row, col)
        elif piece_name is 'kn':
            self.knight_move(row, col)
        elif piece_name is 'r':
            self.rook_move(row, col)
        elif piece_name is 'b':
            self.bishop_move(row, col)
        elif piece_name is 'q':
            self.rook_move(row, col)
            self.bishop_move(row, col)
        elif piece_name is 'k':
            self.king_check_move(node, row, col)

    def movement(self, node):
        piece_name = node.get_piece().get_name()
        row = node.get_row()
        col = node.get_col()
        if piece_name is 'p':
            self.pawn_move(row, col)
        elif piece_name is 'kn':
            self.knight_move(row, col)
        elif piece_name is 'r':
            self.rook_move(row, col)
        elif piece_name is 'b':
            self.bishop_move(row, col)
        elif piece_name is 'q':
            self.rook_move(row, col)
            self.bishop_move(row, col)
        elif piece_name is 'k':
            self.king_move(node, row, col)

    def pawn_move(self, row, col):
        if node.get_piece().get_white():
            if Board.valid_pos(row - 1, col) and self.board[row - 1][col].get_piece() is None:
                self.board[row - 1][col].set_open()
            if Board.valid_pos(row - 2, col) and node.get_piece().get_first() and self.board[row - 2][
                col].get_piece() is None:
                self.board[row - 2][col].set_open()
            if Board.valid_pos(row - 1, col - 1) and self.board[row - 1][col - 1].get_piece() is not None:
                if not self.board[row - 1][col - 1].get_piece().get_white():
                    if self.board[row - 1][col - 1].get_piece().get_name() is not 'k':
                        self.board[row - 1][col - 1].set_open()
                    else:
                        self.check_list.append([row - 1, col - 1])
            if Board.valid_pos(row - 1, col + 1) and self.board[row - 1][col + 1].get_piece() is not None:
                if not self.board[row - 1][col + 1].get_piece().get_white():
                    if self.board[row - 1][col + 1].get_piece().get_name() is not 'k':
                        self.board[row - 1][col + 1].set_open()
                    else:
                        self.check_list.append([row - 1, col + 1])
        else:
            if Board.valid_pos(row + 1, col) and self.board[row + 1][col].get_piece() is None:
                self.board[row + 1][col].set_open()
            if Board.valid_pos(row + 2, col) and node.get_piece().get_first() and self.board[row + 2][
                col].get_piece() is None:
                self.board[row + 2][col].set_open()
            if Board.valid_pos(row + 1, col + 1) and self.board[row + 1][col + 1].get_piece() is not None:
                if self.board[row + 1][col + 1].get_piece().get_white():
                    if self.board[row + 1][col + 1].get_piece().get_name() is not 'k':
                        self.board[row + 1][col + 1].set_open()
                    else:
                        self.check_list.append([row + 1, col + 1])
            if Board.valid_pos(row + 1, col - 1) and self.board[row + 1][col - 1].get_piece() is not None:
                if self.board[row + 1][col - 1].get_piece().get_white():
                    if self.board[row + 1][col - 1].get_piece().get_name() is not 'k':
                        self.board[row + 1][col - 1].set_open()
                    else:
                        self.check_list.append([row + 1, col - 1])

    def knight_move(self, row, col):
        if Board.valid_pos(row - 2, col - 1):
            if self.board[row - 2][col - 1].get_piece() is None:
                self.board[row - 2][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 2][col - 1].get_piece().get_white():
                    if self.board[row - 2][col - 1].get_piece().get_name() is not 'k':
                        self.board[row - 2][col - 1].set_open()
                    else:
                        self.check_list.append([row - 2, col - 1])
        if Board.valid_pos(row - 2, col + 1):
            if self.board[row - 2][col + 1].get_piece() is None:
                self.board[row - 2][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 2][col + 1].get_piece().get_white():
                    if self.board[row - 2][col + 1].get_piece().get_name() is not 'k':
                        self.board[row - 2][col + 1].set_open()
                    else:
                        self.check_list.append([row - 2, col + 1])
        if Board.valid_pos(row + 2, col - 1):
            if self.board[row + 2][col - 1].get_piece() is None:
                self.board[row + 2][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 2][col - 1].get_piece().get_white():
                    if self.board[row + 2][col - 1].get_piece().get_name() is not 'k':
                        self.board[row + 2][col - 1].set_open()
                    else:
                        self.check_list.append([row + 2, col - 1])
        if Board.valid_pos(row + 2, col + 1):
            if self.board[row + 2][col + 1].get_piece() is None:
                self.board[row + 2][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 2][col + 1].get_piece().get_white():
                    if self.board[row + 2][col + 1].get_piece().get_name() is not 'k':
                        self.board[row + 2][col + 1].set_open()
                    else:
                        self.check_list.append([row + 2, col + 1])
        if Board.valid_pos(row - 1, col - 2):
            if self.board[row - 1][col - 2].get_piece() is None:
                self.board[row - 1][col - 2].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col - 2].get_piece().get_white():
                    if self.board[row - 1][col - 2].get_piece().get_name() is not 'k':
                        self.board[row - 1][col - 2].set_open()
                    else:
                        self.check_list.append([row - 1, col - 2])
        if Board.valid_pos(row - 1, col + 2):
            if self.board[row - 1][col + 2].get_piece() is None:
                self.board[row - 1][col + 2].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col + 2].get_piece().get_white():
                    if self.board[row - 1][col + 2].get_piece().get_name() is not 'k':
                        self.board[row - 1][col + 2].set_open()
                    else:
                        self.check_list.append([row - 1, col + 2])
        if Board.valid_pos(row + 1, col - 2):
            if self.board[row + 1][col - 2].get_piece() is None:
                self.board[row + 1][col - 2].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col - 2].get_piece().get_white():
                    if self.board[row + 1][col - 2].get_piece().get_name() is not 'k':
                        self.board[row + 1][col - 2].set_open()
                    else:
                        self.check_list.append([row + 1, col - 2])
        if Board.valid_pos(row + 1, col + 2):
            if self.board[row + 1][col + 2].get_piece() is None:
                self.board[row + 1][col + 2].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col + 2].get_piece().get_white():
                    if self.board[row + 1][col + 2].get_piece().get_name() is not 'k':
                        self.board[row + 1][col + 2].set_open()
                    else:
                        self.check_list.append([row + 1, col + 2])

    def rook_move(self, row, col):
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row - inc, col):
                if self.board[row - inc][col].get_piece() is None:
                    self.board[row - inc][col].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row - inc][col].get_piece().get_white():
                        if self.board[row - inc][col].get_piece().get_name() is not 'k':
                            self.board[row - inc][col].set_open()
                        else:
                            self.check_list.append([row - inc, col])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row + inc, col):
                if self.board[row + inc][col].get_piece() is None:
                    self.board[row + inc][col].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row + inc][col].get_piece().get_white():
                        if self.board[row + inc][col].get_piece().get_name() is not 'k':
                            self.board[row + inc][col].set_open()
                        else:
                            self.check_list.append([row + inc, col])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row, col - inc):
                if self.board[row][col - inc].get_piece() is None:
                    self.board[row][col - inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row][col - inc].get_piece().get_white():
                        if self.board[row][col - inc].get_piece().get_name() is not 'k':
                            self.board[row][col - inc].set_open()
                        else:
                            self.check_list.append([row, col - inc])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row, col + inc):
                if self.board[row][col + inc].get_piece() is None:
                    self.board[row][col + inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row][col + inc].get_piece().get_white():
                        if self.board[row][col + inc].get_piece().get_name() is not 'k':
                            self.board[row][col + inc].set_open()
                        else:
                            self.check_list.append([row, col + inc])
                    break

    def bishop_move(self, row, col):
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row - inc, col - inc):
                if self.board[row - inc][col - inc].get_piece() is None:
                    self.board[row - inc][col - inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row - inc][col - inc].get_piece().get_white():
                        if self.board[row - inc][col - inc].get_piece().get_name() is not 'k':
                            self.board[row - inc][col - inc].set_open()
                        else:
                            self.check_list.append([row - inc, col - inc])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row - inc, col + inc):
                if self.board[row - inc][col + inc].get_piece() is None:
                    self.board[row - inc][col + inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row - inc][col + inc].get_piece().get_white():
                        if self.board[row - inc][col + inc].get_piece().get_name() is not 'k':
                            self.board[row - inc][col + inc].set_open()
                        else:
                            self.check_list.append([row - inc, col + inc])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row + inc, col - inc):
                if self.board[row + inc][col - inc].get_piece() is None:
                    self.board[row + inc][col - inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row + inc][col - inc].get_piece().get_white():
                        if self.board[row + inc][col - inc].get_piece().get_name() is not 'k':
                            self.board[row + inc][col - inc].set_open()
                        else:
                            self.check_list.append([row + inc, col - inc])
                    break
        for i in range(7):
            inc = i + 1
            if Board.valid_pos(row + inc, col + inc):
                if self.board[row + inc][col + inc].get_piece() is None:
                    self.board[row + inc][col + inc].set_open()
                else:
                    if node.get_piece().get_white() is not self.board[row + inc][col + inc].get_piece().get_white():
                        if self.board[row + inc][col + inc].get_piece().get_name() is not 'k':
                            self.board[row + inc][col + inc].set_open()
                        else:
                            self.check_list.append([row + inc, col + inc])
                    break

    def king_move(self, node, row, col):
        if node.get_piece().get_first():
            if node.get_piece().get_white():
                # Castling Procedure
                if self.board[7][1].get_piece() is None and self.board[7][2].get_piece() is None \
                        and self.board[7][3].get_piece() is None \
                        and self.board[7][0].get_piece().get_name() is 'r' \
                        and self.board[7][0].get_piece().get_first():
                    self.board[7][2].set_open()
                if self.board[7][5].get_piece() is None and self.board[7][6].get_piece() is None \
                        and self.board[7][7].get_piece().get_name() is 'r' \
                        and self.board[7][7].get_piece().get_first():
                    self.board[7][6].set_open()
            else:
                if self.board[0][1].get_piece() is None and self.board[0][2].get_piece() is None \
                        and self.board[0][3].get_piece() is None \
                        and self.board[0][0].get_piece().get_name() is 'r' \
                        and self.board[0][0].get_piece().get_first():
                    self.board[0][2].set_open()
                if self.board[0][5].get_piece() is None and self.board[0][6].get_piece() is None \
                        and self.board[0][7].get_piece().get_name() is 'r' \
                        and self.board[0][7].get_piece().get_first():
                    self.board[0][6].set_open()
        # Regular King Movement
        if Board.valid_pos(row + 1, col):
            if self.board[row + 1][col].get_piece() is None:
                self.board[row + 1][col].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col].get_piece().get_white() \
                        and self.board[row + 1][col].get_piece().get_name() is not 'k':
                    self.board[row + 1][col].set_open()
        if Board.valid_pos(row - 1, col):
            if self.board[row - 1][col].get_piece() is None:
                self.board[row - 1][col].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col].get_piece().get_white() \
                        and self.board[row - 1][col].get_piece().get_name() is not 'k':
                    self.board[row - 1][col].set_open()
        if Board.valid_pos(row, col + 1):
            if self.board[row][col + 1].get_piece() is None:
                self.board[row][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row][col + 1].get_piece().get_white() \
                        and self.board[row][col + 1].get_piece().get_name() is not 'k':
                    self.board[row][col + 1].set_open()
        if Board.valid_pos(row, col - 1):
            if self.board[row][col - 1].get_piece() is None:
                self.board[row][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row][col - 1].get_piece().get_white() \
                        and self.board[row][col - 1].get_piece().get_name() is not 'k':
                    self.board[row][col - 1].set_open()
        if Board.valid_pos(row + 1, col - 1):
            if self.board[row + 1][col - 1].get_piece() is None:
                self.board[row + 1][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col - 1].get_piece().get_white() \
                        and self.board[row + 1][col - 1].get_piece().get_name() is not 'k':
                    self.board[row + 1][col - 1].set_open()
        if Board.valid_pos(row + 1, col + 1):
            if self.board[row + 1][col + 1].get_piece() is None:
                self.board[row + 1][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col + 1].get_piece().get_white() \
                        and self.board[row + 1][col + 1].get_piece().get_name() is not 'k':
                    self.board[row + 1][col + 1].set_open()
        if Board.valid_pos(row - 1, col - 1):
            if self.board[row - 1][col - 1].get_piece() is None:
                self.board[row - 1][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col - 1].get_piece().get_white() \
                        and self.board[row - 1][col - 1].get_piece().get_name() is not 'k':
                    self.board[row - 1][col - 1].set_open()
        if Board.valid_pos(row - 1, col + 1):
            if self.board[row - 1][col + 1].get_piece() is None:
                self.board[row - 1][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col + 1].get_piece().get_white() \
                        and self.board[row - 1][col + 1].get_piece().get_name() is not 'k':
                    self.board[row - 1][col + 1].set_open()

    def king_check_move(self, node, row, col):
        if node.get_piece().get_first():
            if node.get_piece().get_white():
                # Castling Procedure
                if self.board[7][1].get_piece() is None and self.board[7][2].get_piece() is None \
                        and self.board[7][3].get_piece() is None \
                        and self.board[7][0].get_piece().get_name() is 'r' \
                        and self.board[7][0].get_piece().get_first():
                    self.board[7][2].set_open()
                if self.board[7][5].get_piece() is None and self.board[7][6].get_piece() is None \
                        and self.board[7][7].get_piece().get_name() is 'r' \
                        and self.board[7][7].get_piece().get_first():
                    self.board[7][6].set_open()
            else:
                if self.board[0][1].get_piece() is None and self.board[0][2].get_piece() is None \
                        and self.board[0][3].get_piece() is None \
                        and self.board[0][0].get_piece().get_name() is 'r' \
                        and self.board[0][0].get_piece().get_first():
                    self.board[0][2].set_open()
                if self.board[0][5].get_piece() is None and self.board[0][6].get_piece() is None \
                        and self.board[0][7].get_piece().get_name() is 'r' \
                        and self.board[0][7].get_piece().get_first():
                    self.board[0][6].set_open()
        # Regular King Movement
        if Board.valid_pos(row + 1, col):
            if self.board[row + 1][col].get_piece() is None:
                self.board[row + 1][col].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col].get_piece().get_white() \
                        and self.board[row + 1][col].get_piece().get_name() is not 'k':
                    self.board[row + 1][col].set_open()
        if Board.valid_pos(row - 1, col):
            if self.board[row - 1][col].get_piece() is None:
                self.board[row - 1][col].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col].get_piece().get_white() \
                        and self.board[row - 1][col].get_piece().get_name() is not 'k':
                    self.board[row - 1][col].set_open()
        if Board.valid_pos(row, col + 1):
            if self.board[row][col + 1].get_piece() is None:
                self.board[row][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row][col + 1].get_piece().get_white() \
                        and self.board[row][col + 1].get_piece().get_name() is not 'k':
                    self.board[row][col + 1].set_open()
        if Board.valid_pos(row, col - 1):
            if self.board[row][col - 1].get_piece() is None:
                self.board[row][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row][col - 1].get_piece().get_white() \
                        and self.board[row][col - 1].get_piece().get_name() is not 'k':
                    self.board[row][col - 1].set_open()
        if Board.valid_pos(row + 1, col - 1):
            if self.board[row + 1][col - 1].get_piece() is None:
                self.board[row + 1][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col - 1].get_piece().get_white() \
                        and self.board[row + 1][col - 1].get_piece().get_name() is not 'k':
                    self.board[row + 1][col - 1].set_open()
        if Board.valid_pos(row + 1, col + 1):
            if self.board[row + 1][col + 1].get_piece() is None:
                self.board[row + 1][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row + 1][col + 1].get_piece().get_white() \
                        and self.board[row + 1][col + 1].get_piece().get_name() is not 'k':
                    self.board[row + 1][col + 1].set_open()
        if Board.valid_pos(row - 1, col - 1):
            if self.board[row - 1][col - 1].get_piece() is None:
                self.board[row - 1][col - 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col - 1].get_piece().get_white() \
                        and self.board[row - 1][col - 1].get_piece().get_name() is not 'k':
                    self.board[row - 1][col - 1].set_open()
        if Board.valid_pos(row - 1, col + 1):
            if self.board[row - 1][col + 1].get_piece() is None:
                self.board[row - 1][col + 1].set_open()
            else:
                if node.get_piece().get_white() is not self.board[row - 1][col + 1].get_piece().get_white() \
                        and self.board[row - 1][col + 1].get_piece().get_name() is not 'k':
                    self.board[row - 1][col + 1].set_open()

    def close_all(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.board[i][j].set_closed()

    @staticmethod
    def valid_pos(row, col):
        if 8 > row > -1 and 8 > col > -1:
            return True

    @staticmethod
    def get_loc():
        mx, my = pygame.mouse.get_pos()
        column = mx // 100
        row = my // 100
        return int(row), int(column)

    @staticmethod
    def white_square(x, y):
        pygame.draw.rect(screen, black_color, pygame.Rect(x, y, width / 8, height / 8), 1)

    @staticmethod
    def black_square(x, y):
        pygame.draw.rect(screen, gray_color, pygame.Rect(x, y, width / 8, height / 8))
        pygame.draw.rect(screen, black_color, pygame.Rect(x, y, width / 8, height / 8), 1)

    @staticmethod
    def create_board():
        x = 0
        y = 0
        counter = 0
        for i in range(16):
            if counter == 4:
                counter = 0
                x = 0
                y += 200
            Board.white_square(x, y)
            x += 100
            Board.black_square(x, y)
            x += 100
            counter += 1
        x = 0
        y = 100
        counter = 0
        for i in range(16):
            if counter == 4:
                counter = 0
                x = 0
                y += 200
            Board.black_square(x, y)
            x += 100
            Board.white_square(x, y)
            x += 100
            counter += 1

    @staticmethod
    def castling(temp_piece, row, column):
        if temp_piece.get_name() is 'k' and temp_piece.get_first():
            if temp_piece.get_white():
                if row == 7 and column == 2:
                    board.get_node(7, 3).set_piece(board.get_node(7, 0).get_piece())
                    board.get_node(7, 3).get_piece().moved()
                    board.get_node(7, 0).set_piece(None)
                if row == 7 and column == 6:
                    board.get_node(7, 5).set_piece(board.get_node(7, 7).get_piece())
                    board.get_node(7, 5).get_piece().moved()
                    board.get_node(7, 7).set_piece(None)
            else:
                if row == 0 and column == 2:
                    board.get_node(0, 3).set_piece(board.get_node(0, 0).get_piece())
                    board.get_node(0, 3).get_piece().moved()
                    board.get_node(0, 0).set_piece(None)
                if row == 0 and column == 6:
                    board.get_node(0, 5).set_piece(board.get_node(0, 7).get_piece())
                    board.get_node(0, 5).get_piece().moved()
                    board.get_node(0, 7).set_piece(None)

    def check(self, white):
        if white:
            for i in range(8):
                for j in range(8):
                    if self.board[i][j].get_piece() is not None:
                        if self.board[i][j].get_piece().get_white():
                            print(self.board[i][j].get_piece().get_white())
                            self.board.movement(board[i][j])
                            print(board.get_list())


board = Board()

pygame.init()
# Colors
black_color = (0,0,0)
white_color = (255,255,255)
brown_color = (222,184,135)
blue_color = (50,255,255)
gray_color =(211,211,211)

# Create Screen
width = 800
height = 800
screen = pygame.display.set_mode((width, height))

# Title
pygame.display.set_caption("Chess")


node = None
clicked = False
move = False
turn = True
# Game Loop
running = True
while running:
    pygame.time.delay(100)
    screen.fill((255, 255, 255))
    Board.create_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse movement
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, column = Board.get_loc()
            first_row, first_col = row, column
            print(row, column)
            node = board.get_node(row, column)
            if node.get_piece() is not None:
                if turn == node.get_piece().get_white():
                    board.movement(node)
                    node.set_selected(True)
                    if node.get_selected():
                        print('selected')
            if event.button == 1:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            if clicked:
                row, column = Board.get_loc()
                print(row, column)
                if board.get_node(row, column).get_open():
                    temp_piece = node.get_piece()
                    node.set_piece(None)
                    if temp_piece.get_name() is 'p' and row == 0 and temp_piece.get_white():
                        board.get_node(row, column).set_piece(Piece('q', True, 'wQueen.png'))
                    elif temp_piece.get_name() is 'p' and row == 7 and not temp_piece.get_white():
                        board.get_node(row, column).set_piece(Piece('q', False, 'bQueen.png'))
                    else:
                        board.get_node(row, column).set_piece(temp_piece)
                    board.castling(temp_piece, row, column)
                    board.get_node(row, column).get_piece().moved()
                    if turn:
                        turn = False
                    else:
                        turn = True
                    if board.get_list():
                        if turn:
                            board.set_b_check()
                        else:
                            board.set_w_check()
                    board.clear_list()
                node.set_selected(False)
                board.close_all()
                print(turn)
                print(board.get_list())
                print('W check', board.get_w_check())
                print('B check', board.get_b_check())

            if event.button == 1:
                clicked = False

    for i in range(len(board.get_board())):
        for j in range(len(board.get_board()[i])):
            if board.get_node(i, j).get_open():
                pygame.draw.rect(screen, blue_color,
                                 pygame.Rect(board.get_node(i, j).get_col() * 100,
                                             board.get_node(i, j).get_row() * 100, width / 8, height / 8), 1)
            if board.get_node(i, j).get_piece() is not None and not(board.get_node(i, j).get_selected()):
                screen.blit(board.get_node(i, j).get_piece().get_img(),
                            (board.get_node(i, j).get_col()*100 + 15, board.get_node(i, j).get_row()*100 + 15))
            elif board.get_node(i, j).get_selected():
                mx, my = pygame.mouse.get_pos()
                print(mx, my)
                screen.blit(board.get_node(i, j).get_piece().get_img(), (mx, my))
    pygame.display.update()





