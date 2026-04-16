import sente
import tkinter as tk
from tkinter import simpledialog
game = sente.Game()
black = sente.stone.BLACK
white = sente.stone.WHITE
root = tk.Tk()
root.title('CS331 GO Project')

# Starting Game UI State.
topLabel = tk.Label(root, text="GO (THE BOARD GAME)\n", fg = "White", font = "Courier 25")
topLabel.pack()
gameBoard = tk.Label(root, text=str(game), font = "Courier 20")
gameBoard.pack()
turnIndicator = tk.Label(root, text="\nYOUR TURN", font = "Verdana 15 bold")
turnIndicator.pack()

# Player and AI Moves in Game
def makeMove():
    ### User Turn
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
    gameBoard.config(text=str(game), font = "Courier 20")
    turnIndicator.config(text="\nAI TURN", font = "Verdana 15 bold")

    #
    # AI CODE HERE
    #

    # Update UI with move.
    gameBoard.config(text=str(game), font = "Courier 20")
    turnIndicator.config(text="\nYOUR TURN", font = "Verdana 15 bold")

# Due to root.mainloop(), a while loop won't work
# Thus a 'make move' button was deemed the solution as it allows for n moves.
button = tk.Button(root, text='Make Move', width=25, command=makeMove).pack()

# Title Select Screen.
def main():
    lbl = tk.Label(root, text="Hello World")
    lbl.pack()
    
if __name__ == '__main__':

    root.mainloop()
