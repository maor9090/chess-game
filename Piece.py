


class Piece:
    def __init__(self, name, location,color):
        self.name = name
        self.location = location
        self.color= color

    def __str__(self):
        return f"{self.color} {self.name} at {self.location}"

    def move(self, new_location):
        self.location = new_location
        print(f"{self.name} moved to {self.location}")


    def getLetter(self):
        return f"{self.name[0]}{self.color[0]}"

    def checkMovements(self,board):
        moves = []
        return moves

    def getPosition(self):
        if isinstance(self.location, str):
            col = ord(self.location[0]) - ord('A')
        else:
            col = int(self.location[0])
        row = int(self.location[1])-1
        return row, col