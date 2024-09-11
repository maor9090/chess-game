import Functions
import aiMoves

def mainMenu():
    while True:
        print("Hello player!\nPlease type what option you want:\n"
              "[1] Start game with two players\n"
              "[2] Start game with AI\n"
              "[3] AI VS AI\n"
              "[4] Settings")
        choice = input().strip()

        if choice == "1":
            print("Starting a two-player game...")
            Functions.twoPlayerGame()
            break  # Exit the menu loop after starting the game
        elif choice == "2":
            print("Starting a game with AI...")
            # Call the function to start the AI game
            aiMoves.startGameWithAIw()
            break  # Exit the menu loop after starting the game
        elif choice == "3":
            print("Starting a game with AI Vs AI...")
            # Call the function to start the AI game
            aiMoves.aiVsai()
            break  # Exit the menu loop after starting the game
        elif choice == "4":
            print("Opening settings...")
            # Call the function to open settings
            openSettings()
            break  # Exit the menu loop after opening settings
        else:
            print("Invalid choice, please try again.")



def openSettings():
    pass  # Implement settings logic here

mainMenu()
