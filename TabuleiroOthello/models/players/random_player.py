class RandomPlayer:
    def __init__(self, color):
        self.color = color


    import random

    def play(self, board):
        return self.random.choice(board.valid_moves(self.color))
