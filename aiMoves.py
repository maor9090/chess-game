from Piece import Piece
from Bishop import Bishop
from King import King
from Knight import Knight
from Pawn import Pawn
from Queen import Queen
from Rook import Rook
import Functions
import random


def randomMoves(board, color, last_move):
    options = []  # This will store tuples of (Piece, start_position, end_position)

    # Loop through all pieces on the board
    for row_idx, row in enumerate(board):
        for col_idx, piece in enumerate(row):
            # Skip if the element is None or not a valid piece
            if piece is None:
                continue

            # Check if the piece is of the correct color
            if piece.color == color:
                # Get possible moves for each piece
                if isinstance(piece, King) or isinstance(piece, Pawn):
                    moves = piece.checkMovements(board, last_move)
                else:
                    moves = piece.checkMovements(board)

                # Store each move along with the piece and its starting position
                for move in moves:
                    options.append((piece, (row_idx, col_idx), move))  # (piece, start_position, end_position)

    # If there are no possible moves, return None or handle as needed
    if not options:
        return None

    # Select a random move from the available options
    selected_piece, start_pos, end_pos = random.choice(options)

    # Return the selected piece and its move
    return selected_piece, start_pos, end_pos


def startGameWithAIw():
    board = Functions.createBoard()
    winner = 0
    last_move = None  # Track the last move

    while winner == 0:
        Functions.printBoard(board)
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
                        if len(start_pos) == 2:
                            if start_pos[0] >= 'A' and start_pos[0] <= 'H' and start_pos[1] > '0' and start_pos[
                                1] < '9':
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
                        if isinstance(board[start_row][start_col], Pawn) or isinstance(board[start_row][start_col],
                                                                                       King):
                            moveCheck = board[start_row][start_col].checkMovements(board, last_move)
                        else:
                            moveCheck = board[start_row][start_col].checkMovements(board)
                        if Functions.moveBreaksCheck(board, (start_row, start_col), (end_row, end_col), "White"):
                            if (end_row, end_col) in moveCheck:
                                Functions.handleEnPassant(board, (start_row, start_col), (end_row, end_col), last_move)
                                Functions.handleCastling(board, (start_row, start_col), (end_row, end_col))
                                piece = board[start_row][start_col]
                                piece.move(end_pos)
                                board[end_row][end_col] = piece
                                board[start_row][start_col] = None
                                if isinstance(board[end_row][end_col], Pawn) and end_row == 3:
                                    last_move = (end_row, end_col)
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
                    piece_pos = piece_pos.upper()
                    piece_row, piece_col = int(piece_pos[1]) - 1, ord(piece_pos[0]) - ord('A')
                    if isinstance(board[piece_row][piece_col], Pawn) or isinstance(board[piece_row][piece_col], King):
                        possible_moves = board[piece_row][piece_col].checkMovements(board, last_move)
                        Functions.printBoardPM(board, possible_moves)
                        break
                    elif isinstance(board[piece_row][piece_col], Piece):
                        possible_moves = board[piece_row][piece_col].checkMovements(board)
                        Functions.printBoardPM(board, possible_moves)
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
                Functions.printBoard(board)
            else:
                print("Invalid choice, please try again.")

        # Check if Black is in checkmate
        if Functions.hasNoPossibleMoves(board, "Black"):
            print("White wins!")
            winner = 1
            break

        # AI Move
        Functions.printBoard(board)
        ai_move = randomMoves(board, "Black", last_move)
        if ai_move:
            selected_piece, start_pos, end_pos = ai_move
            # Update the board with the AI's move
            board[start_pos[0]][start_pos[1]] = None  # Clear the starting position
            board[end_pos[0]][end_pos[1]] = selected_piece  # Move the piece to the new position
            selected_piece.move(end_pos)

            # Set `last_move` if it's a two-square pawn move
            if isinstance(selected_piece, Pawn) and abs(start_pos[0] - end_pos[0]) == 2:
                last_move = end_pos
            else:
                last_move = None

        # Check if White is in checkmate
        if Functions.hasNoPossibleMoves(board, "White") and Functions.isKingInCheck(board,"White"):
            print("Black wins!")
            winner = 1
            break

    if winner == 1:
        print("Black wins!")
    elif winner == 2:
        print("White wins!")
    else:
        print("Draw!")




def aiVsai():
    board = Functions.createBoard()
    winner = 0
    last_move = None  # Track the last move

    while winner == 0:
        Functions.printBoard(board)
        ai_move = randomMoves(board, "White", last_move)
        if ai_move:
            selected_piece, start_pos, end_pos = ai_move
            # Update the board with the AI's move
            board[start_pos[0]][start_pos[1]] = None  # Clear the starting position
            board[end_pos[0]][end_pos[1]] = selected_piece  # Move the piece to the new position
            selected_piece.move(end_pos)

            # Set `last_move` if it's a two-square pawn move
            if isinstance(selected_piece, Pawn) and abs(start_pos[0] - end_pos[0]) == 2:
                last_move = end_pos
            else:
                last_move = None

        # Check if White is in checkmate
        if Functions.hasNoPossibleMoves(board, "Black") and Functions.isKingInCheck(board,"Black"):
            winner = 2
            break

        Functions.printBoard(board)
        ai_move2 = randomMoves(board, "Black", last_move)
        if ai_move2:
            selected_piece, start_pos, end_pos = ai_move2
        # Update the board with the AI's move
            board[start_pos[0]][start_pos[1]] = None  # Clear the starting position
            board[end_pos[0]][end_pos[1]] = selected_piece  # Move the piece to the new position
            selected_piece.move(end_pos)

        # Set `last_move` if it's a two-square pawn move
            if isinstance(selected_piece, Pawn) and abs(start_pos[0] - end_pos[0]) == 2:
                last_move = end_pos
            else:
                last_move = None

    # Check if White is in checkmate
        if Functions.hasNoPossibleMoves(board, "White") and Functions.isKingInCheck(board,"White"):
            winner = 1
            break

    if winner == 1:
        print("Black wins!")
    elif winner == 2:
        print("White wins!")
    else:
        print("Draw!")