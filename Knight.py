from typing import override

from Piece import Piece


class Knight(Piece):
    def __init__(self, location,color):
        super().__init__("Knight", location,color)
    @override
    def getLetter(self):
        return f"H{self.color[0]}"
    @override
    def checkMovements(self,board):
        x, y = self.getPosition()
        moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        possible_moves = []

        for dx, dy in moves:
            new_x = x + dx
            new_y = y + dy

            # Check if the new position is within the board boundaries
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Get the piece at the new position
                piece_at_new_position = board[new_x][new_y]

                # Check if there is a piece at the new position and if it's of the same color
                if not isinstance(piece_at_new_position,Piece) or piece_at_new_position.color != self.color:
                    possible_moves.append((new_x, new_y))

        return possible_moves


