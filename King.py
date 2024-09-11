from typing import override

from Pawn import Pawn
from Rook import Rook
from Piece import Piece


class King(Piece):
    def __init__(self, location,color):
        super().__init__("King", location,color)
        self.has_moved = False
    @override
    def move(self, new_location):
        self.location = new_location
        print(f"{self.name} moved to {self.location}")
        self.has_moved = True
    @override
    def checkMovements(self, board,last_move):
        x, y = self.getPosition()
        moves = [
            (1, 0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        possible_moves = []

        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece_at_new_position = board[new_x][new_y]
                if not isinstance(piece_at_new_position, Piece) or piece_at_new_position.color != self.color:
                    possible_moves.append((new_x, new_y))

        if not self.has_moved:

            if self._is_castling_possible(board, x, 5, 6, 7,last_move):
                possible_moves.append((x, 6))

            # Check if the squares are safe for queenside castling
            if self._is_castling_possible(board, x, 3, 2, 0,last_move):
                possible_moves.append((x, 2))

        return possible_moves

    def _is_castling_possible(self, board, row, king_path_start, king_path_end, rook_col, last_move):
        # Ensure the rook hasn't moved and the spaces are empty
        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            return False

        # Ensure that the path is clear and the king is not moving through or into check
        for col in range(king_path_start, king_path_end + 1):
            if board[row][col] is not None:
                return False
            if self._is_square_under_attack(board, row, col, last_move):
                return False

        return True

    def _is_square_under_attack(self, board, x, y, last_move):
        # Check if the square is under attack by any enemy piece
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color != self.color:
                    # King and Pawn special cases
                    if isinstance(piece, King):
                        if abs(row - x) <= 1 and abs(col - y) <= 1:
                            return True
                    elif isinstance(piece, Pawn):
                        pawn_direction = 1 if piece.color == 'white' else -1
                        if (row + pawn_direction == x and abs(col - y) == 1):
                            return True
                    else:
                        if (x, y) in piece.checkMovements(board):
                            return True
        return False

