from Piece import Piece


class Queen(Piece):
    def __init__(self, location):
        super().__init__("Queen", location)
