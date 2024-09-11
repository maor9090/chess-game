from Piece import Piece
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook
import copy
import aiMoves

def createBoard():
    board = [[None for _ in range(8)] for _ in range(8)]

    # Place white pieces
    white_pieces = [
        Rook("A1", "White"), Knight("B1", "White"), Bishop("C1", "White"),
        Queen("D1", "White"), King("E1", "White"), Bishop("F1", "White"),
        Knight("G1", "White"), Rook("H1", "White")
    ]
    for i, piece in enumerate(white_pieces):
        row = 0
        col = i
        board[row][col] = piece

    white_pawns = [Pawn(f"{chr(65 + i)}2", "White") for i in range(8)]
    for i, pawn in enumerate(white_pawns):
        row = 1
        col = i
        board[row][col] = pawn

    black_pawns = [Pawn(f"{chr(65 + i)}7", "Black") for i in range(8)]
    for i, pawn in enumerate(black_pawns):
        row = 6
        col = i
        board[row][col] = pawn

    # Place black pieces
    black_pieces = [
        Rook("A8", "Black"), Knight("B8", "Black"), Bishop("C8", "Black"),
        Queen("D8", "Black"), King("E8", "Black"), Bishop("F8", "Black"),
        Knight("G8", "Black"), Rook("H8", "Black")
    ]
    for i, piece in enumerate(black_pieces):
        row = 7
        col = i
        board[row][col] = piece

    return board


def printBoard(board):
    print("    A      B      C      D      E      F      G      H")
    for i in range(8):
        print(i + 1, end=' ')
        for j in range(8):
            if isinstance(board[i][j], Piece):
                print("[", board[i][j].getLetter(), "]", end=' ')
            else:
                print("[    ]", end=' ')
        print(i + 1, end=' ')
        print("\n")
    print("    A      B      C      D      E      F      G      H")


def printBoardPM(board, moves):
    if moves is None:
        moves = []

    print("    A      B      C      D      E      F      G      H")

    for i in range(8):
        print(i + 1, end=' ')
        for j in range(8):
            if (i, j) in moves:
                if isinstance(board[i][j], Piece):
                    if board[i][j].getLetter().lower() == 'p':  # Assuming 'p' for pawn
                        print("!", board[i][j].getLetter(), "!", end=' ')  # Highlight en passant
                    else:
                        print("?", board[i][j].getLetter(), "?", end=' ')  # Highlight regular move
                else:
                    print("[ ???? ]", end=' ')  # Highlight possible move square
            elif isinstance(board[i][j], Piece):
                print("[", board[i][j].getLetter(), "]", end=' ')  # Print regular piece
            else:
                print("[    ]", end=' ')  # Print empty square
        print(i + 1, end=' ')
        print("\n")

    print("    A      B      C      D      E      F      G      H")

def castle(self, board, side):
    if self.canCastle(board, side):
        row = 0 if self.color == "White" else 7
        if side == 'kingside':
            self.move((row, 6))
            board[row][5] = board[row][7]
            board[row][7] = None
            board[row][5].move((row, 5))
        elif side == 'queenside':
            self.move((row, 2))
            board[row][3] = board[row][0]
            board[row][0] = None
            board[row][3].move((row, 3))


def isKingInCheck(board, king_color):
    king_position = None

    # Find the King's position on the board
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if isinstance(piece, King) and piece.color == king_color:
                king_position = (i, j)
                break
        if king_position:
            break

    if not king_position:
        raise ValueError("King not found on the board.")

    # Check if any enemy piece can move to the King's position
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if isinstance(piece, Piece) and piece.color != king_color:
                if isinstance(piece,Pawn) or isinstance(piece,King):
                    possible_moves = piece.checkMovements(board,None)
                else:
                    possible_moves = piece.checkMovements(board)
                if king_position in possible_moves:
                    return True

    return False


def kingMoveCausesCheck(board, start_pos, end_pos, king_color):
    board_copy = [row[:] for row in board]

    king = board_copy[start_pos[0]][start_pos[1]]
    board_copy[end_pos[0]][end_pos[1]] = king
    board_copy[start_pos[0]][start_pos[1]] = None

    king.move(end_pos)

    if isKingInCheck(board_copy, king_color):
        print("Invalid move! The King cannot move to a position that puts him in check.")
        return True

    return False


def moveBreaksCheck(board, start_pos, end_pos, king_color):
    # Deep copy the entire board
    board_copy = copy.deepcopy(board)

    piece = board_copy[start_pos[0]][start_pos[1]]
    board_copy[end_pos[0]][end_pos[1]] = piece
    board_copy[start_pos[0]][start_pos[1]] = None

    piece.move(end_pos)

    if not isKingInCheck(board_copy, king_color):
        return True
    else:
        return False


def handleEnPassant(board, start_pos, end_pos, last_move):
    # En passant is only valid if the last move was a two-square advance of a pawn
    if last_move is not None and isinstance(board[start_pos[0]][start_pos[1]],Pawn):
        if start_pos[1] != end_pos[1] and board[end_pos[0]][end_pos[1]] is None:
            board[last_move[0]][last_move[1]] = None  # Remove the captured pawn
            print("En Passant executed!")
            return True
    return False
def handleCastling(board, start_pos, end_pos):
    piece = board[start_pos[0]][start_pos[1]]
    if not isinstance(piece, King):
        return False

    # Check if the move is a castling move (moving two squares horizontally)
    if start_pos[1] - end_pos[1] == 2:  # Queenside castling (king moves left)
        # Move the rook from column 0 to column 3
        board[start_pos[0]][3] = board[start_pos[0]][0]
        board[start_pos[0]][0] = None
        print("Queenside Castling executed!")
        return True
    elif end_pos[1] - start_pos[1] == 2:  # Kingside castling (king moves right)
        # Move the rook from column 7 to column 5
        board[start_pos[0]][5] = board[start_pos[0]][7]
        board[start_pos[0]][7] = None
        print("Kingside Castling executed!")
        return True

    return False


def twoPlayerGame():
    board = createBoard()
    winner = 0
    last_move = None  # Track the last move

    while winner == 0:
        printBoard(board)
        while True:
            print("Whites' turn, please choose what you want to do:\n"
                  "[1] Make a move\n"
                  "[2] Look for possible movements\n"
                  "[3] Surrender\n"
                  "[4] Offer draw\n"
                  "[5] Print board again")
            choice = input()
            if choice == "1":
                while True:
                    while True:
                        start_pos = input("Enter the location of the piece you want to move: ")
                        start_pos = start_pos.upper()
                        if len(start_pos)==2:
                            if start_pos[0] >= 'A' and start_pos[0] <= 'H' and start_pos[1] > '0' and start_pos[1] < '9':
                                break
                    start_row, start_col = int(start_pos[1]) - 1, ord(start_pos[0]) - ord('A')
                    if isinstance(board[start_row][start_col], Piece) and board[start_row][start_col].color == "White":
                        while True:
                            end_pos = input("Enter the location you want to move the piece into: ")
                            end_pos = end_pos.upper()
                            if len(end_pos) == 2:
                                if end_pos[0] >= 'A' and end_pos[0] <= 'H' and end_pos[1] >= '1' and end_pos[1] < '9':
                                    break
                        end_row, end_col = int(end_pos[1]) - 1, ord(end_pos[0]) - ord('A')
                        if isinstance(board[start_row][start_col], Pawn) or isinstance(board[start_row][start_col],King):
                            moveCheck = board[start_row][start_col].checkMovements(board, last_move)
                        else:
                            moveCheck = board[start_row][start_col].checkMovements(board)
                        if moveBreaksCheck(board, (start_row, start_col), (end_row, end_col), "White"):
                            if (end_row, end_col) in moveCheck:
                                handleEnPassant(board, (start_row, start_col), (end_row, end_col), last_move)
                                handleCastling(board, (start_row, start_col), (end_row, end_col))
                                piece = board[start_row][start_col]
                                piece.move(end_pos)
                                board[end_row][end_col] = piece
                                board[start_row][start_col] = None
                                if isinstance(board[end_row][end_col], Pawn) and end_row==3:
                                        last_move = end_row, end_col
                                else:
                                    last_move = None
                                break
                            else:
                                print("Can't move to that location, please enter new locations")
                        else:
                            print("The king is in check!")
                    else:
                        print("You chose an invalid location, please choose a new one")
                break

            elif choice == "2":
                while True:
                    piece_pos = input("Enter the location of the piece you want to check the moves for: ")
                    piece_pos=piece_pos.upper()
                    piece_row, piece_col = int(piece_pos[1]) - 1, ord(piece_pos[0]) - ord('A')
                    if isinstance(board[piece_row][piece_col], Pawn) or isinstance(board[piece_row][piece_col], King):
                        possible_moves = board[piece_row][piece_col].checkMovements(board, last_move)
                        printBoardPM(board, possible_moves)
                        break
                    elif isinstance(board[piece_row][piece_col], Piece):
                        possible_moves = board[piece_row][piece_col].checkMovements(board)
                        printBoardPM(board, possible_moves)
                        break
                    else:
                        print("You chose an invalid location, please choose a new one")
            elif choice == "3":
                winner = 2
                break
            elif choice == "4":
                print("Black, do you accept the draw? (yes/no)")
                if input().strip().lower() == "yes":
                    winner = 3
                break
            elif choice == "5":
                printBoard(board)
            else:
                print("Invalid choice, please try again.")

        # Check if Black is in checkmate
        if hasNoPossibleMoves(board, "Black") and isKingInCheck(board,"Black"):
            print("White wins!")
            winner = 1
            break

        printBoard(board)
        while True:
            print("Blacks' turn, please choose what you want to do:\n"
                  "[1] Make a move\n"
                  "[2] Look for possible movements\n"
                  "[3] Surrender\n"
                  "[4] Offer draw\n"
                  "[5] Print board again")
            choice = input()
            if choice == "1":
                while True:
                    while True:
                        start_pos = input("Enter the location of the piece you want to move: ")
                        start_pos = start_pos.upper()
                        if len(start_pos)==2:
                            if start_pos[0] >= 'A' and start_pos[0] <= 'H' and start_pos[1] > '0' and start_pos[1] < '9':
                                break
                    start_row, start_col = int(start_pos[1]) - 1, ord(start_pos[0]) - ord('A')
                    if isinstance(board[start_row][start_col], Piece) and board[start_row][start_col].color == "Black":
                        while True:
                            end_pos = input("Enter the location you want to move the piece into: ")
                            end_pos = end_pos.upper()
                            if len(end_pos) == 2:
                                if end_pos[0] >= 'A' and end_pos[0] <= 'H' and end_pos[1] >= '1' and end_pos[1] < '9':
                                    break
                        end_row, end_col = int(end_pos[1]) - 1, ord(end_pos[0]) - ord('A')
                        if isinstance(board[start_row][start_col], Pawn) or isinstance(board[start_row][start_col],King):
                            moveCheck = board[start_row][start_col].checkMovements(board, last_move)
                        else:
                            moveCheck = board[start_row][start_col].checkMovements(board)

                        if moveBreaksCheck(board, (start_row, start_col), (end_row, end_col), "Black"):
                            if (end_row, end_col) in moveCheck:
                                handleEnPassant(board, (start_row, start_col), (end_row, end_col), last_move)
                                handleCastling(board, (start_row, start_col), (end_row, end_col))
                                piece = board[start_row][start_col]
                                piece.move(end_pos)
                                board[end_row][end_col] = piece
                                board[start_row][start_col] = None
                                if isinstance(board[end_row][end_col], Pawn) and end_row==4:
                                    last_move = end_row, end_col
                                else:
                                    last_move=None
                                break
                            else:
                                print("Can't move to that location, please enter new locations")
                        else:
                            print("The king is in check!")
                    else:
                        print("You chose an invalid location, please choose a new one")
                break

            elif choice == "2":
                while True:
                    piece_pos = input("Enter the location of the piece you want to check the moves for: ")
                    piece_pos=piece_pos.upper()
                    piece_row, piece_col = int(piece_pos[1]) - 1, ord(piece_pos[0]) - ord('A')
                    if isinstance(board[piece_row][piece_col], Pawn) or isinstance(board[piece_row][piece_col], King):
                        possible_moves = board[piece_row][piece_col].checkMovements(board, last_move)
                        printBoardPM(board, possible_moves)
                        break
                    elif isinstance(board[piece_row][piece_col], Piece):
                        possible_moves = board[piece_row][piece_col].checkMovements(board)
                        printBoardPM(board, possible_moves)
                        break
                    else:
                        print("You chose an invalid location, please choose a new one")

            elif choice == "3":
                winner = 1
                break
            elif choice == "4":
                print("White, do you accept the draw? (yes/no)")
                if input().strip().lower() == "yes":
                    winner = 3
                break
            elif choice == "5":
                printBoard(board)
            else:
                print("Invalid choice, please try again.")

        # Check if White is in checkmate
        if hasNoPossibleMoves(board, "White") and isKingInCheck(board,"White"):
            print("Black wins!")
            winner = 1
            break

    if winner == 1:
        print("Black wins!")
    elif winner == 2:
        print("White wins!")
    else:
        print("Draw!")


def hasNoPossibleMoves(board, color):
    # Find the king of the specified color
    king_position = None
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == color and isinstance(piece, King):
                king_position = (row, col)
                break
        if king_position:
            break

    if not king_position:
        return True  # No king found, should not happen in normal play

    # Check if the king is in check
    if not isKingInCheck(board, color):
        return False  # King is not in check, so checkmate cannot occur

    # Iterate through all pieces of the specified color
    possible_moves=[]
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == color and isinstance(piece, King) or isinstance(piece,Pawn):
                possible_moves = piece.checkMovements(board, None)
            elif piece and piece.color == color:
                possible_moves = piece.checkMovements(board)
            if possible_moves is None:
                for move in possible_moves:
                    if moveBreaksCheck(board, (row, col), move, color):
                        return False
    return True
