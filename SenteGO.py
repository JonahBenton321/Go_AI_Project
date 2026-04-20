# NOTICE: The was restructured into the __init__() and other def X() style under classes through
# the direct involvement of Google AI.
# The underlying code was freshly sourced through articles and YouTube tutorials.

import sente
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from model_handler import AIHandler
black = sente.stone.BLACK
white = sente.stone.WHITE
root = tk.Tk()
root.title('CS331 GO Project')

# The Starting screen.
class SelectionScreen:
    # Starting Game UI State.
    topLabel = tk.Label(root, text="\n\nGO", fg = "White", font = "Courier 35")
    topLabel.pack()
    topLabelParens = tk.Label(root, text="(THE BOARD GAME)\n", fg = "White", font = "Courier 10")
    topLabelParens.pack()
    turnIndicator = tk.Label(root, text="\nSTART\n", font = "Verdana 15 bold")
    turnIndicator.pack()

    def playGO():
        global game
        game = sente.Game()
        new_window = tk.Toplevel(root)
        GOGame(new_window)

    def goToSettings():
        new_window = tk.Toplevel(root)
        settingsPage(new_window)

    def goToExplanation():
        new_window = tk.Toplevel(root)
        explanationPage(new_window)

    button = tk.Button(root, text='PLAY GO', width=25, command=playGO).pack()
    button = tk.Button(root, text='SETTINGS', width=25, command=goToSettings).pack()
    button = tk.Button(root, text='HOW TO PLAY', width=25, command=goToExplanation).pack()

# The HELP section.
class settingsPage:
    def __init__(self, root):
        self.topLabel = tk.Label(root, text="HELP\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        
        self.gameHelper = tk.Label(root, text="When playing, the game will ask you some prompts:\n", font = "Verdana 13 bold")
        self.gameHelper.pack()
        self.gameExplainer = tk.Label(root, text="- Black(B) or White(W) --> 'b' for player 1 and 'w' for player 2.\n"
                                   "- Click 'Make Move' button to make a move of (X,Y) format.\n"
                                   "- (X,Y) are standard X and inverted Y as shown by the side board grids.\n"
                                   "- 'Best Move' displays what the AI model would play in that position.\n"
                                   , font = "Verdana 13")
        self.gameExplainer.pack()

# The HOW TO PLAY section.
class explanationPage:
    def __init__(self, root):
        self.topLabel = tk.Label(root, text="HOW TO PLAY\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        
        self.howToPlay = tk.Label(root, text="\nGO is a strategy boardgame where:\n", font = "Verdana 13 bold")
        self.printedRules = tk.Label(root, text="- Black goes first.\n"
                                  "- Players may Pass (leave blank) their turn.\n"
                                  "- Pieces are captured through encirclement (on Vertical-Horizontal).\n"
                                  "- Points are acquired through capturing space.\n"
                                  "- The player with the most points wins.\n"
                                  "\n", font = "Verdana 13")
        self.howToPlay.pack()
        self.printedRules.pack()
        

# The code that actually plays the game of GO.
class GOGame(AIHandler):
    def __init__(self, root):
        user_color = simpledialog.askstring("Input", "Black(B) or White(W): ")
        # # AIStrength = simpledialog.askstring("Input", "AI Level (0) (1) or (2)?: ")
        # Starting Game UI State.
        self.topLabel = tk.Label(root, text="GO (THE BOARD GAME)\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        self.gameBoard = tk.Label(root, text=str(game), font = "Courier 20")
        self.gameBoard.pack()
        self.moveRating = tk.Label(root, text="Previous Move Rating: (0.XXX)\n", fg = "White", font = "Verdana 15 bold")
        self.moveRating.pack()
        self.bestMove = tk.Label(root, text="Best Move: (X,Y)\n", fg = "White", font = "Verdana 15 bold")
        self.bestMove.pack()
        self.turnIndicator = tk.Label(root, text="\nYOUR TURN", font = "Verdana 15 bold")
        self.turnIndicator.pack()

        # Due to root.mainloop(), a while loop won't work
        # Thus a 'make move' button was deemed the solution as it allows for n moves.
        if user_color.lower() == "b":
            self.button = tk.Button(root, text='Make Move', width=25, command=self.makeMoveBlack)
            self.button.pack()
        else:
            self.button = tk.Button(root, text='Make Move', width=25, command=self.makeMoveWhite)
            self.button.pack()

    def endGame():
        results = game.get_results()
        white_won = 'w' in results.lower()
        black_won = 'b' in results.lower()
        
        new_window = tk.Toplevel(root)
        winnerPage(new_window)
            

    # Player and AI Moves in Game
    def makeMoveBlack(self):
        ### USER TURN
        # Allow for leway in user input for more accessible gameplay.
        user_input = simpledialog.askstring("Input", f"Move (ie: X,Y): ")
        user_input = user_input.replace(" ", "")
        user_input = user_input.replace("(", "")
        user_input = user_input.replace(")", "")
        # Specify that user intends to pass.
        if user_input == "no" or user_input == "":
            game.pss()
        else: 
            x, y = map(int, user_input.split(','))
            # Flip coordinates to match classic X,Y Graph coordinates.
            # y = 20 - y
            game.play(x,y)
        # Update UI with move.
        self.gameBoard.config(text=str(game), font = "Courier 20")
        self.turnIndicator.config(text="\nAI TURN", font = "Verdana 15 bold")

        ### AI TURN
        game.play(19,19)

        rateMove = AIHandler.rate_user_move(self, game, user_input)
        recommendMove = AIHandler.recommend_move(self, game)
        
        # Update UI with move.
        self.gameBoard.config(text=str(game), font = "Courier 20")
        self.moveRating.config(text="\nUser Move Rating: : " + rateMove, font = "Verdana 15 bold")
        self.bestMove.config(text="Recommend Move: " + recommendMove, font = "Verdana 20 bold")
        self.turnIndicator.config(text="\nYOUR TURN", font = "Verdana 15 bold")

    # Player and AI Moves in Game
    def makeMoveWhite(self):
        ### AI TURN
        game.play(19,19)

        # Update UI with move.
        self.gameBoard.config(text=str(game), font = "Courier 20")
        self.turnIndicator.config(text="\nYOUR TURN", font = "Verdana 15 bold")
        self.bestMove.label
        
        ### USER TURN
        # Allow for leway in user input for more accessible gameplay.
        user_input = simpledialog.askstring("Input", f"Move (ie: X,Y): ")
        user_input = user_input.replace(" ", "")
        user_input = user_input.replace("(", "")
        user_input = user_input.replace(")", "")
        # Specify that user intends to pass.
        if user_input == "no" or user_input == "":
            game.pss()
        else: 
            x, y = map(int, user_input.split(','))
            # Flip coordinates to match classic X,Y Graph coordinates.
            # y = 20 - y
            game.play(x,y)


        rateMove = AIHandler.rate_user_move(self, game, user_input)
        recommendMove = AIHandler.recommend_move(self, game)
        
        # Update UI with move.
        self.gameBoard.config(text=str(game), font = "Courier 20")
        self.moveRating.config(text="\nUser Move Rating: : " + rateMove, font = "Verdana 15 bold")
        self.bestMove.config(text="Recommend Move: " + recommendMove, font = "Verdana 20 bold")
        self.turnIndicator.config(text="\nAI TURN", font = "Verdana 15 bold")

        if game.is_over():
            end_game()

#class winnerPage:
    #if (white_won and user_color.lower() == 'w') or (black_won and user_color.lower() == 'b'):
        #winner = "USER"
        #print(game.get_results)
        #print("USER HAS DEFEATED THE AI!")
        #print("\nTo play again, select 'Play Game' on the home screen.")
        
    #else if (white_won and user_color.lower() == 'b') or (black_won and user_color.lower() == 'w'):
        #winner = "AI"
        #print(game.get_results)
        #print("USER HAS BEEN DEFEATED BY THE AI!")
        #print("\nTo play again, select 'Play Game' on the home screen.")
        
if __name__ == '__main__':
    app = SelectionScreen() # This was brought to you by Google AI.
    root.mainloop()
