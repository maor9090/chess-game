from typing import override

from Piece import Piece


class Bishop(Piece):
    def __init__(self, location,color):
        super().__init__("Bishop", location,color)
    @override
    def checkMovements(self, board):
        x, y = self.getPosition()
        directions = [
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        possible_moves = []

        for dx, dy in directions:
            step = 1
            while True:
                new_x, new_y = x + dx * step, y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    piece_at_new_position = board[new_x][new_y]
                    if not isinstance(piece_at_new_position,Piece):
                        possible_moves.append((new_x, new_y))
                    elif piece_at_new_position.color != self.color:
                        possible_moves.append((new_x, new_y))
                        break
                    else:
                        break
                else:
                    break
                step += 1

        return possible_moves