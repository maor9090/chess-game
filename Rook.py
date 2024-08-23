from Piece import Piece


class Pawn(Piece):
    def __init__(self, location):
        super().__init__("Pawn", location)

    def promote(self):
        print(f"The {self.name} at {self.location} is being promoted!")