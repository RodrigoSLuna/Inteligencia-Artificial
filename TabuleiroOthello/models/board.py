"""Tabuleiro"""

import copy
from models.move import Move

class Board(object):
    """Objeto de tabuleiro de jogo de Othelo."""
    EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'

    DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT = [-1, 0], [1, 0], [0, -1], [0, 1]
    DIR_UP_RIGHT, DIR_DOWN_RIGHT, DIR_DOWN_LEFT, DIR_UP_LEFT = [-1, 1], [1, 1], [1, -1], [-1, -1]

    DIRECTIONS = (DIR_UP, DIR_UP_RIGHT, DIR_RIGHT, DIR_DOWN_RIGHT,
                  DIR_DOWN, DIR_DOWN_LEFT, DIR_LEFT, DIR_UP_LEFT)

    def __init__(self, board):
        if board is None:
            self.board = []
            for i in range(0, 10):
                self.board.insert(i, [Board.OUTER]*10)

            for i in range(1, 9):
                for j in range(1, 9):
                    self.board[i][j] = Board.EMPTY

            self.board[4][4], self.board[4][5] = Board.WHITE, Board.BLACK
            self.board[5][4], self.board[5][5] = Board.BLACK, Board.WHITE
        else:
            self.board = copy.deepcopy(board)

    def play(self, move, color):
        """Realiza jogada de jogador de cor 'color' na posicao 'move'."""
        if (color == Board.BLACK) or (color == Board.WHITE):
            self.board[move.x][move.y] = color
            self._reverse(move, color)
        return

    def get_square_color(self, line, column):
        """Retorna qual a cor presente na casa de posicao (l,c)."""
        return self.board[line][column]

    def get_clone(self):
        """Retorna uma copia do tabuleiro atual."""
        return Board(self.board)

    def valid_moves(self, color):
        """Retorna os movimentos validos para o jogador de cor 'color'."""
        ret = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self.board[i][j] == Board.EMPTY:
                    for direction in Board.DIRECTIONS:
                        move = Move(i, j)
                        bracket = self._find_bracket(move, color, direction)
                        if bracket:
                            ret += [move]
        return ret

    def __str__(self):
        return 'White (' + str(self.score()[0]) + ') X (' + str(self.score()[1]) + ') Black'

    def score(self):
        """Retorna o score de ambos os jogadores."""
        white = 0
        black = 0
        for i in range(1, 9):
            for j in range(1, 9):
                if self.board[i][j] == Board.WHITE:
                    white += 1
                elif self.board[i][j] == Board.BLACK:
                    black += 1

        return [white, black]


    def _squares(self):
        return [i for i in xrange(11, 89) if 1 <= (i % 10) <= 8]

    def _reverse(self, move, color):
        for direction in Board.DIRECTIONS:
            self._make_flips(move, color, direction)

    def _make_flips(self, move, color, direction):
        bracket = self._find_bracket(move, color, direction)
        if not bracket:
            return
        square = [move.x + direction[0], move.y + direction[1]]
        while square != bracket:
            self.board[square[0]][square[1]] = color
            square = [square[0] + direction[0], square[1] + direction[1]]

    def _find_bracket(self, move, color, direction):
        bracket = [move.x + direction[0], move.y + direction[1]]
        bracket_color = self.board[bracket[0]][bracket[1]]

        if bracket_color == color:
            return None
        opponent = self._opponent(color)
        while bracket_color == opponent:
            bracket = [bracket[0] + direction[0], bracket[1] + direction[1]]
            bracket_color = self.board[bracket[0]][bracket[1]]

        return None if self.board[bracket[0]][bracket[1]] in (Board.OUTER, Board.EMPTY) else bracket

    def _opponent(self, color):
        return Board.BLACK if color is Board.WHITE else Board.WHITE
