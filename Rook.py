from typing import override

from Piece import Piece


class Rook(Piece):
    def __init__(self, location,color):
        super().__init__("Rook", location,color)
        self.has_moved = False
    @override
    def move(self, new_location):
        self.location = new_location
        print(f"{self.name} moved to {self.location}")
        self.has_moved = True
    @override
    def checkMovements(self, board):
        x, y = self.getPosition()
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
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