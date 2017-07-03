class CornerPlayer:
    def __init__(self, color):
        self.color = color

    def play(self, board):
        return self.getNearestCorner(board.valid_moves(self.color))

    def getNearestCorner(self, moves):
        import math
        corners = [[1,1],[1,8], [8,1], [8,8]]
        minDist = 10
        retMove = None
        for move in moves:
            for corner in corners:
                distX = abs(corner[0] - move.x)
                distY = abs(corner[1] - move.y)
                dist    = math.sqrt(distX*distX + distY*distY)
                if dist < minDist:
                    minDist = dist
                    retMove = move

        return retMove
