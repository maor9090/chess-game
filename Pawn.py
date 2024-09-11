from typing import override

from Piece import Piece


class Pawn(Piece):
    def __init__(self, location: str, color: str):
        super().__init__("Pawn", location, color)
        self.has_moved = False

    def promote(self):
        print(f"The {self.name} at {self.location} is being promoted!")

    def move(self, new_location: str):
        self.location = new_location
        print(f"{self.name} moved to {self.location}")
        self.has_moved = True

    @override
    def checkMovements(self, board, last_move):
        x, y = self.getPosition()
        possible_moves = []

        direction = 1 if self.color == "White" else -1

        # Move forward by one square
        if 0 <= x + direction < 8 and board[x + direction][y] is None:
            possible_moves.append((x + direction, y))

        # Move forward by two squares from the starting position
        if not self.has_moved and 0 <= x + 2 * direction < 8 and board[x + 2 * direction][y] is None:
            possible_moves.append((x + 2 * direction, y))

        # Capture diagonally
        for dy in [-1, 1]:
            new_x = x + direction
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece_at_new_position = board[new_x][new_y]
                if piece_at_new_position and isinstance(piece_at_new_position,
                                                        Piece) and piece_at_new_position.color != self.color:
                    possible_moves.append((new_x, new_y))

        # En passant capture
        if last_move:
            last_x, last_y = last_move[0], last_move[1]

            # Check if the last move was a pawn's two-square move from the 4th rank to the 5th or 6th rank
            if (last_x == x and
                    abs(last_y - y) == 1 and
                    isinstance(board[last_x][last_y], Pawn) and
                    board[last_x][last_y].color != self.color and
                    not board[last_x][last_y].has_moved):
                possible_moves.append((x + direction, last_y))

        return possible_moves







