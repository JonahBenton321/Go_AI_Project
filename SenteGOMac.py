# NOTICE: The was restructured into the __init__() and other def X() style under classes through
# the direct involvement of Google AI.
# The underlying code was freshly sourced through articles and YouTube tutorials.
from math import gamma
import random
import sente
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
import model_handler_mac as AIHandlerFile
black = sente.stone.BLACK
white = sente.stone.WHITE
root = tk.Tk()
root.title('CS331 GO Project')
turnedOnRater = True
turnedOnRecommended = True
model8d = True

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
        radioVar = tk.StringVar()
        radioVar1 = tk.StringVar()
        radioVar2 = tk.StringVar()
        self.topLabel = tk.Label(root, text="SETTINGS\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        
        moveRaterON = tk.Radiobutton(root, text = "Turn ON Move Rater", value = "moveRaterON", variable = radioVar, command = self.turnOnRater)
        moveRaterON.pack()
        moveRaterOFF = tk.Radiobutton(root, text = "Turn OFF Move Rater", value = "moveRaterOFF", variable = radioVar, command = self.turnOffRater)
        moveRaterOFF.pack()
        self.breaker = tk.Label(root, text="- - - - - - - - - - - -", fg = "White", font = "Courier 25")
        self.breaker.pack()

        recBestON = tk.Radiobutton(root, text = "Turn ON Move Recommendations", value = "recBestON", variable = radioVar1, command = self.turnOnRecBest)
        recBestON.pack()
        recBestOFF = tk.Radiobutton(root, text = "Turn OFF Move Recommendations", value = "recBestOFF", variable = radioVar1, command = self.turnOffRecBest)
        recBestOFF.pack()
        self.breaker2 = tk.Label(root, text="- - - - - - - - - - - -", fg = "White", font = "Courier 25")
        self.breaker2.pack()

        model8dON = tk.Radiobutton(root, text = "Turn ON MODEL 8d", value = "model8dON", variable = radioVar2, command = self.turnOnModel8d)
        model8dON.pack()
        model1kON = tk.Radiobutton(root, text = "Turn ON MODEL 1k", value = "model1kON", variable = radioVar2, command = self.turnOnModel1k)
        model1kON.pack()
        model18kON = tk.Radiobutton(root, text = "Turn ON MODEL 18k", value = "model18kON", variable = radioVar2, command = self.turnOnModel18k)
        model18kON.pack()

    def turnOnRater(self):
        global turnedOnRater
        turnedOnRater = True
        print("Turned On")
    def turnOffRater(self):
        global turnedOnRater
        turnedOnRater = False
        print("Turned Off")

    def turnOnRecBest(self):
        global turnedOnRecommended
        turnedOnRecommended = True
        print("Turned On")
    def turnOffRecBest(self):
        global turnedOnRecommended
        turnedOnRecommended = False
        print("Turned Off")

    def turnOnModel8d(self):
        global model8dON, model1kON, model18kON
        model8dON = True; model1kON = False; model18kON = False
        print("Go_model_8d.pth")
    def turnOnModel1k(self):
        global model8dON, model1kON, model18kON
        model8dON = False; model1kON = True; model18kON = False
        print("Go_model_1k.pth")
    def turnOnModel18k(self):
        global model8dON, model1kON, model18kON
        model8dON = False; model1kON = False; model18kON = True
        print("Go_model_18k.pth")

# The HOW TO PLAY section.
class explanationPage:
    def __init__(self, root):
        self.topLabel = tk.Label(root, text="HOW TO PLAY\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        
        self.howToPlay = tk.Label(root, text="\nGO is a strategy boardgame where:", font = "Verdana 15 bold")
        self.printedRules = tk.Label(root, text="- Black goes first.\n"
                                  "- Players may Pass (leave blank) their turn.\n"
                                  "- Pieces are captured through encirclement (on Vertical-Horizontal).\n"
                                  "- Points are acquired through capturing space.\n"
                                  "- The player with the most points wins.\n"
                                  "\n", font = "Verdana 13")
        self.howToPlay.pack()
        self.printedRules.pack()

        self.gameHelper = tk.Label(root, text="When playing, the game will ask you some prompts:", font = "Verdana 15 bold")
        self.gameHelper.pack()
        self.gameExplainer = tk.Label(root, text="- Black(B) or White(W) --> 'b' for player 1 and 'w' for player 2.\n"
                                   "- Click 'Make Move' button to make a move of (X,Y) format.\n"
                                   "- (X,Y) are standard X and inverted Y as shown by the side board grids.\n"
                                   "- 'Best Move' displays what the AI model would play in that position.\n"
                                   , font = "Verdana 13")
        self.gameExplainer.pack() 

# The code that actually plays the game of GO.
class GOGame:
    def __init__(self, root):
        global user_color
        self.root = root
        self.game = sente.Game()
        if model8dON:
            self.aihandler = AIHandlerFile.AIHandler("Go_model_8d.pth")
            print("Go_model_8d.pth")
        elif model1kON:
            self.aihandler = AIHandlerFile.AIHandler("Go_model_1k.pth")
            print("Go_model_1k.pth")
        elif model18kON:
            self.aihandler = AIHandlerFile.AIHandler("Go_model_18k.pth")
            print("Go_model_18k.pth")
        self.manual_move_history = [] # AI
        user_color = simpledialog.askstring("Input", "Black(B) or White(W) or Self(S): ")
        # Starting Game UI State.
        self.topLabel = tk.Label(root, text="GO (THE BOARD GAME)\n", fg = "White", font = "Courier 25")
        self.topLabel.pack()
        self.gameBoard = tk.Label(root, text=str(game), font = "Courier 20")
        self.gameBoard.pack()
        self.gameCordKey = tk.Label(root, text="    1  2  3   4  5  6  7  8  9  10 11 12 13  14 15 16 17 18 19", fg="White", font = "Courier 19")
        self.gameCordKey.pack()
        self.moveRating = tk.Label(root, text="Previous Move Rating: (0.XXX)", fg = "White", font = "Verdana 15 bold")
        self.moveRating.pack()
        self.bestMove = tk.Label(root, text="Best Move: (X,Y)\n", fg = "White", font = "Verdana 15 bold")
        self.bestMove.pack()
        self.turnIndicator = tk.Label(root, text="\nYOUR TURN", font = "Verdana 15 bold")
        self.turnIndicator.pack()

        # Due to root.mainloop(), a while loop won't work
        # Thus a 'make move' button was deemed the solution as it allows for n moves.
        # Since I've hotkeyed 'Enter' to also make a move.
        if user_color.lower() == "b":
            self.root.bind("<Return>", self.makeMoveBlack)
            self.button = tk.Button(root, text='Make Move', width=25, command=self.makeMoveBlack)
            self.button.pack()
        elif user_color.lower() == "w":
            self.root.bind("<Return>", self.makeMoveWhite)
            self.button = tk.Button(root, text='Make Move', width=25, command=self.makeMoveWhite)
            self.button.pack()
        else:
            self.root.bind("<Return>", self.aiSelfPlay)
            self.button = tk.Button(root, text='Start Sim', width=25, command=self.aiSelfPlay)
            self.button.pack()
            # In manual testing I found that all models processed the same game every playthrough.
            # This sets out to bring some form of game variation.
            self.game.play(random.randint(1, 19),random.randint(1, 19))
            self.game.play(random.randint(1, 19),random.randint(1, 19))

    # Collects necessary results, and opens the results window.
    def endGame(self):
        global results, whiteScore, blackScore, whiteWon, blackWon
        finalscores = self.game.score()
        results, whiteScore, blackScore  = finalscores.values()
        whiteWon = 'W' in results
        blackWon = 'B' in results
        
        new_window = tk.Toplevel(root)
        winnerPage(new_window)

    def modelSwitcher(self):
        global model8dON, model1kON, model18kON
        model8dON = False; model1kON = False; model18kON = False
        userModelSelect = simpledialog.askstring("Input", "(1) model_8d | (2) model_1k | (3) model_18k: ")
        if userModelSelect == "1":
            self.aihandler = AIHandlerFile.AIHandler("Go_model_8d.pth")
            print("Go_model_8d.pth")
        elif userModelSelect == "2":
            self.aihandler = AIHandlerFile.AIHandler("Go_model_1k.pth")
            print("Go_model_1k.pth")
        elif userModelSelect == "3":
            self.aihandler = AIHandlerFile.AIHandler("Go_model_18k.pth")
            print("Go_model_18k.pth")

    # Player and AI Moves in Game
    # I've realized this serves as a user goes second function, not a hardcoded user is black pieces.
    def makeMoveBlack(self, event=None):
        ### USER TURN
        rateMove = "N/A (Pass)"

        user_input = simpledialog.askstring("Input", f"Move (ie: X,Y) or 'pass' or 'resign' or 'switch: ")
        user_input = user_input.replace(" ", "").replace("(", "").replace(")", "")

        #Specify that user intends to pass.
        if user_input == "pass" or user_input == "":
            self.game.play(None)
            self.manual_move_history.append((None, sente.stone.BLACK)) # AI
        elif user_input == "resign":
            self.game.resign()
            self.endGame()
            return
        elif user_input == "switch":
            self.modelSwitcher()
            return
        else: 
            x, y = map(int, user_input.split(','))
            self.game.play(x, y) 
            self.manual_move_history.append((x - 1, y - 1, sente.stone.BLACK)) # AI
            rateMove = self.aihandler.rate_user_move(self.manual_move_history, (x, y)) # AI
            
        self.gameBoard.config(text=str(self.game), font="Courier 20")
        self.turnIndicator.config(text="\nAI TURN", font="Verdana 15 bold")
        ### END USER TURN

        ### AI TURN (Made by AI for AI)
        # 1. Ask the model for the best move
        ai_move = self.aihandler.infer_best_move(self.aihandler, self.game)
        
        # Check if the AI returned None or a pass string
        if ai_move is None or isinstance(ai_move, str):
            print("AI has no valid moves left or decided to pass/resign.")
            
            # Fix 1: Push a NATIVE pass directly to the C++ engine
            # This makes consecutive passes fire Sente's internal win state!
            self.game.play(None) 
            
            # Fix 2: Add None coordinates to tracking to prevent inhomogeneous shape crashes
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
            
            # 3. Immediately evaluate if the native passes ended the game
            if self.game.is_over():
                print("Game officially over! Sente recognized consecutive passes.")
                self.endGame()
                return
            return 
            
        # 4. If it's a valid coordinate, unpack it safely
        model_x, model_y = ai_move

        recommendMove = self.aihandler.recommend_move(self.manual_move_history, self.game, exclude_move=(model_x, model_y))
        if isinstance(recommendMove, tuple):
            recommend_str = f"({int(recommendMove[0])}, {int(recommendMove[1])})"
        else:
            recommend_str = str(recommendMove) 
        
        # Shift the 0-18 model coordinates to your 1-19 legal range
        ai_x = int(model_x)
        ai_y = int(model_y)
        
        try:
            self.game.play(ai_x, ai_y)
            # Add play to tracker
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((model_x, model_y, active_color))
            
        except sente.exceptions.IllegalMoveException:
            print(f"AI self-play picked occupied spot at {ai_x}, {ai_y}. Passing turn.")
            self.game.play(None)
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
        ### END AI TURN
        self.gameBoard.config(text=str(self.game), font="Courier 20")
        
        global turnedOnRater
        if turnedOnRater:
            self.moveRating.config(text="User Move Rating: " + rateMove, font="Verdana 15 bold")
        else:
            pass
        
        global turnedOnRecommended
        if turnedOnRecommended:
            self.bestMove.config(text="Recommend Move: " + recommend_str, font="Verdana 20 bold")
        else:
            pass
        
        self.turnIndicator.config(text="\nYOUR TURN", font="Verdana 15 bold")

    # Player and AI Moves in Game
    # Allow for a single 'buffer' AI move, then switch to makeMoveBlack.
    # As with a buffer it then falls to the user going 'first' again.
    # This allows for a simpler codebase.
    def makeMoveWhite(self, event=None):
        self.root.bind("<Return>", self.makeMoveBlack)
        rateMove = "N/A (Pass)"
        ### AI TURN (Made by AI for AI)
        # 1. Ask the model for the best move
        ai_move = self.aihandler.infer_best_move(self.manual_move_history, self.game)
        
        # Check if the AI returned None or a pass string
        if ai_move is None or isinstance(ai_move, str):
            print("AI has no valid moves left or decided to pass/resign.")
            
            # Fix 1: Push a NATIVE pass directly to the C++ engine
            # This makes consecutive passes fire Sente's internal win state!
            self.game.play(None) 
            
            # Fix 2: Add None coordinates to tracking to prevent inhomogeneous shape crashes
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
            
            # 3. Immediately evaluate if the native passes ended the game
            if self.game.is_over():
                print("Game officially over! Sente recognized consecutive passes.")
                self.endGame()
                return
            return 
            
        # 4. If it's a valid coordinate, unpack it safely
        model_x, model_y = ai_move

        recommendMove = self.aihandler.recommend_move(self.manual_move_history, self.game, exclude_move=(model_x, model_y))
        if isinstance(recommendMove, tuple):
            recommend_str = f"({int(recommendMove[0])}, {int(recommendMove[1])})"
        else:
            recommend_str = str(recommendMove) 
        
        # Shift the 0-18 model coordinates to your 1-19 legal range
        ai_x = int(model_x)
        ai_y = int(model_y)
        
        try:
            self.game.play(ai_x, ai_y)
            # Add play to tracker
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((model_x, model_y, active_color))
            
        except sente.exceptions.IllegalMoveException:
            print(f"AI self-play picked occupied spot at {ai_x}, {ai_y}. Passing turn.")
            self.game.play(None)
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
        ### END AI TURN

        global turnedOnRater
        if turnedOnRater:
            self.moveRating.config(text="User Move Rating: " + rateMove, font="Verdana 15 bold")
        else:
            pass
        
        global turnedOnRecommended
        if turnedOnRecommended:
            self.bestMove.config(text="Recommend Move: " + recommend_str, font="Verdana 20 bold")
        else:
            pass
        
        self.button.config(text='Make Move', command=self.makeMoveBlack)
        self.button.pack()
        self.turnIndicator.config(text="\nYOUR TURN", font="Verdana 15 bold")

    # Repeatedly calls the AI to make a move
    def aiSelfPlay(self, event=None):
        ### AI TURN (Made by AI for AI)
        # 1. Ask the model for the best move
        ai_move = self.aihandler.infer_best_move(self.manual_move_history, self.game)
        
        # Check if the AI returned None or a pass string
        if ai_move is None or isinstance(ai_move, str):
            print("AI has no valid moves left or decided to pass/resign.")
            
            # Fix 1: Push a NATIVE pass directly to the C++ engine
            # This makes consecutive passes fire Sente's internal win state!
            self.game.play(None) 
            
            # Fix 2: Add None coordinates to tracking to prevent inhomogeneous shape crashes
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
            
            # 3. Immediately evaluate if the native passes ended the game
            if self.game.is_over():
                print("Game officially over! Sente recognized consecutive passes.")
                self.endGame()
                return
            return 
            
        # 4. If it's a valid coordinate, unpack it safely
        model_x, model_y = ai_move

        recommendMove = self.aihandler.recommend_move(self.manual_move_history, self.game, exclude_move=(model_x, model_y))
        if isinstance(recommendMove, tuple):
            recommend_str = f"({int(recommendMove[0])}, {int(recommendMove[1])})"
        else:
            recommend_str = str(recommendMove) 
        
        # Shift the 0-18 model coordinates to your 1-19 legal range
        ai_x = int(model_x)
        ai_y = int(model_y)
        
        try:
            self.game.play(ai_x, ai_y)
            # Add play to tracker
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((model_x, model_y, active_color))
            
        except sente.exceptions.IllegalMoveException:
            print(f"AI self-play picked occupied spot at {ai_x}, {ai_y}. Passing turn.")
            self.game.play(None)
            active_color = sente.stone.BLACK if len(self.manual_move_history) % 2 == 0 else sente.stone.WHITE
            self.manual_move_history.append((None, None, active_color))
        ### END AI TURN

        # Update UI with the active board
        self.gameBoard.config(text=str(self.game), font="Courier 20")

class winnerPage:
    global whiteWon, blackWon, results, whiteScore, blackScore, user_color
    def __init__(self, root):
        # USER beat AI
        if (whiteWon and user_color.lower() == 'w') or (blackWon and user_color.lower() == 'b'):
            winner = "USER"
            self.userVictory = tk.Label(root, text="USER HAS DEFEATED THE AI!", font = "Courier 30")
            self.userVictory.pack()
        # AI beat USER
        elif (whiteWon and user_color.lower() == 'b') or (blackWon and user_color.lower() == 'w'):
            winner = "AI"
            self.userDefeat = tk.Label(root, text="USER HAS BEEN DEFEATED BY THE AI!", font = "Courier 30")
            self.userDefeat.pack()
        # AI beat AI scenarios.
        elif (blackWon):
            winner = "BLACK"
            self.blackVictory = tk.Label(root, text="\nBLACK HAS WON THE GAME!", font = "Courier 30")
            self.blackVictory.pack()
        elif (whiteWon):
            winner = "WHITE"
            self.whiteVictory = tk.Label(root, text="WHITE HAS WON THE GAME!", font = "Courier 30")
            self.whiteVictory.pack()

        # General stats to print in all cases.
        self.blackVictoryMargin = tk.Label(root, text="FINAL MARGIN: " + results, font = "Courier 20")
        self.blackVictoryMargin.pack()
        self.blackVictoryBlack = tk.Label(root, text="\nBLACK SCORE: " + str(blackScore), font = "Courier 20")
        self.blackVictoryBlack.pack()
        self.blackVictoryWhite = tk.Label(root, text="WHITE SCORE: " + str(whiteScore), font = "Courier 20")
        self.blackVictoryWhite.pack()
        self.blackVictoryPlayAgain = tk.Label(root, text="\nTo play again, close the game tabs and select 'Play Game' on the home screen.", font = "Courier 13")
        self.blackVictoryPlayAgain.pack()
            
        
if __name__ == '__main__':
    app = SelectionScreen() # This was brought to you by Google AI.
    root.focus_set() # Allows for hotkeys.
    root.mainloop() # Main loop entire file.
