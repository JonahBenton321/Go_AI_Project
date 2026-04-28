# Introduction
Our system was designed with the primary motivation of providing users with a human-like opponent for the Chinese game Go. Most Go-based software is designed to offer a virtual opponent optimized around winning matches.  We wanted to create a virtual set of opponents that would play more in a human-like style while still presenting some moderate challenge to the end user. The system creates a virtual Go game and presents an interactive UI for the user. The software offers the user the choice between three different AI models trained on three different skill levels of data. This creates a set of optional opponents at varying levels of difficulty. The software also utilizes the model trained on the highest tier of human data to serve as a move rating and recommendation system. These functions help the user to improve their skill with the game and make decisions in tough areas of strategy. Overall, the goal of the software is to help users improve skill in the game without presenting virtual opponents optimized for victory alone.
# Time Log
| Name | Hours | Time | Description |
| :--- | :----: | :----: | :--- |
| Casey | 4 hours | Mar. 18, 2026, 9:00pm - 1:00am | Introduced myself to tkinter and its UI capabilities. |
| Casey | 2 hours | Mar. 19, 2026, 9:30am - 11:30am | Started small by coding GO to display and play in the terminal. |
| Casey | 6 hours | April 9, 2026, 12:00pm - 4:00pm; 10:00pm - 12:00am | Begun to, and made ample progress in, creating the GO game to run in tkinter. |
| Casey | 2 hours | April 15, 2026, 11:00pm - 1:00am | Attempted to make progress on the process of windows setting and help menus. |
| Casey | 7 hours | April 16, 2026, 11:00am - 4:00pm; 5:00pm - 7:00pm | Refactored SenteGO into classes, and it made the coding process a lot easier. Thanks, Google AI. |
| Casey | 1.5 hours | April 17, 2026, 12:00pm - 1:30pm | Once again looked into the settings and help menu, but this time made noticeable progress. |
| Casey | 5.5 hours | April 19, 2026, 2:30pm - 5:00pm; 10:00pm - 1:00am | Got all the menus sorted out and working along with setting up for what should hopefully be an easy plug-n-play process for the AI models. |
| Casey | 7 hours | April 20, 2026, 11:00am - 1:00pm; 2:00pm - 4:00pm; 9:00pm - 12:00m | Attempted to do things regarding plugging the AI model into the code and so far nothing is working. I also attempted to add a winnerPage for the end of the game. |
| Casey | 5 hours | April 24, 2026, 12:30pm - 1:30pm; 8:00pm - 12:00m | After a break I’m trying again and it didn’t work, so instead I’m working on other aspects like creating toggleable features like the move rater/recommenders. I’ve discovered the problem, and it’s because I have a MacBook. |
| Casey | 4 hours | April 25, 206, 9:00pm - 1:00am | I've gotten the code to work on my machine now and I'm starting to implement end game aspects such as the final results screen. |
| Casey | 11 hours | April 26, 2026, 12:00n-5:00pm; 6:00pm-12:00m | Now it’s the final stretch of making sure everything works and everything is implemented such as the toggleable settings. Along with making sure all AI code is flagged as such. |
| Casey TOTAL | 55 hours | . | . |

| Name | Hours | Task | Accomplished |
| :--- | :----: | :----: | :--- |
| Jonah | ~5  | Create data pipline for training | Wrote conversion code to convert SGF files to memmory mapped numpy arrays|
| Jonah | 6.5 | Train RF model to play Go | None (complete failure)|
| Jonah | 5 | Train logistic regression model to play Go | None (complete failure) |
| Jonah | 1.7| Train pytorch model to play Go at 8d skill level | Completed successfully |
| Jonah | 2| Write first version of model componet | Added infer move function, and test cases |
| Jonah | 2 | Improve model code to allow pass/resign moves| Added Bouzy Algorithm to estimate game outcomes for passing/resigning at the right time |
| Jonah | 4.5 | Add the rest of model componet, and test cases | Added rate/recommend move functionality, and test cases |
| Jonah | 1.5 | Train two more models, 1k, 18k skill level, and polished existing code | Used existing data pipline to create more models, added more commets to code |
| Jonah | 1 hours| Fix known issue where AI would play moves in the wrong space | Fixed translation math |
| Jonah | 2 hours | Fix issues with model and main game logic componets not interacting without crash/wrong behavior| Fixed self play logic, fixed issue where models whould not run on cpu, fixed poor UI scaling, fixed wrong UI colors fixed issue where resigning would break game over screen |
| Jonah | 1 hours | Play test game| Found that code works as needed |
| Jonah TOTAL | 32.2 hours | . | . |


# Requirements
## Go Game Engine - complete
Our system presents a fully functional game of Go to the user using the Sente library as the primary engine to run the game of Go on the back end. Our system offers an interactive UI to allow human users to smoothly input moves and see model responses displayed on the game board.
## Neural Network AI - complete
Our software presents three convolutional neural networks which trained on one million board states from their respective skill categories. The following data conveys the accuracy score each model achieved on a 10,000-board state test set which models were not trained on. The data effectively conveys how statistically human each model plays the game of Go.
| **Model Training data**| **Top-1 accuracy**| **Top-5 accuracy**| **Training data skill bracket**|
|----------------------------|---------------------|-------------------------------------------------|----|
| Hard Model| 25%|50% |8d |
| Intermediate Model|24% |45% |1k |
| Essay Model|21% |47% |18k |

The above data conveys that models are able to select which move a human would have played in 201 to 25 per cent of cases. If the model's top five moves are evaluated, it correctly guesses the human move in up to 50% of cases. Because there are 361 total board spaces the model can select from at any given point, the base rate for successfully picking a human-like move is 0.27%. Based on these figures our models perform almost two orders of magnitude superior to random guessing, even the weakest model is 78 times more likely to pick the correct move than random chance. What this means is that our models can successfully play statistically human moves in many states of the game. It should be noted that our method does not include search trees which consider future possible states of the game and as such our models will not perform as well as other techniques when it comes to global strategy. A consequence of that is that even our strongest model in terms of skill level could still be beaten by a competent user. What our models can do is play in a human fashion in local, moment-to-moment gameplay achieving our goal of constructing humanlike opponents even if they're not capable of posing a significant challenge to a skilled user.
## Move Quality Rater - complete
Our move quality rater queries the model trained on the highest skill level of human data, 8d, and creates a ranking of every possible move and how good the model believes them to be. The model's first choices are at the top of the list and by comparing the players’ chosen move to the model's chosen to move it creates an approximation of how good that move is based on the model’s reasoning. If the user's chosen move is in the top 20 moves selected by the model the move is rated as excellent if it is in the top 200 it is rated as mediocre if it is in the bottom 161 it is rated as a blunder.
## Move Recommendations - complete
The move recommendation system works in a similar manner to the move quality rater. The best model is shown in the current state of the board and asked to predict which move is the best. The move is shown to the users as a coordinate on the game board and they may freely choose if they wish to play the recommended move.

## Unfinished
The following are a list of wanted features which we did not start development on for this project.
-	Option to undo moves.
-	Option to Save the current game state.
-	Create a fine-tuned AI opponent using self-play.
-	Option to watch games between different AI models.
-	Option to add handicap cap stones.
-	Nine AI opponents three in the beginner, adept, and professional categories of increasing difficulty.
-	Options to pick board size from 7x7, 9x9, 13x13, and 19x19.
-	Game highlight review, which allows the user to review moves of great consequence to the game’s outcome.
-	Players’ game statistics such as average move quality, average time spent thinking per move and total number of mistakes.
# Design and Overall Structure
Our system uses Three main frameworks spread over five individual components to achieve the system core functionality. Below can be seen a diagram which describes the relationships between our core components. The arrow represents which components talk to which other components. Dashed connections represent relationships not used during normal play but were used during model training.
![Alt text](Images/diagram.png)

Our code structure is mainly organized around five main components
-	Main Game Logic System
-	Go Engine
-	User Interface
-	AI models
-	Data Pipeline
## General Design
Our Code is structured around the Main Game Logic System which is responsible for creating and maintaining a game of Go between a human and our AI models. The Game Logic system will manage all other major components in order to facilitate a functional game of Go. This component will create a game of Go using Sente and call the human user and AI models to make moves at the correct time. The component is also responsible for calling the system's UI to visually display the game to the user and offer menu functionality. The User Interface, Go Engine, and AI models work together to create a competitive game of Go. The User Interface and AI models both talk to the Go Engine so both entities can play moves and update the board state. The Data Pipeline, while not used during a normal game, is used in tandem with the Go Engine to create training data for the AI models component. Each comment when put together creates a fully functional game of Go complete with virtual opponents.
Our project uses three main frameworks to achieve core functionality Pytorch, Sente, NumPy, and Tkinker. 
-	Pytorch is used to create and train AI models
-	Sente serves as the system Go engine running and managing the game
-	NumPy creates data frames for AI training.
-	Tkinker is used to create a User Interface
## Desing Pattern
The Data Pipeline component employes and iterator design pattern to loop over every file in a directory for the purpose of converting those files to training data.
# Implementation
The following is description of key components frameworks, and other systems are implemented.
## Sente and the GO Engine
Sente is a python library that allows for managing and running a game of Go in the python program. In our structure Sente serves as a go between the user and AI models. Sente internally stores the current state of the board which can be displayed to either the user or AI models. Once the user or AI model has played their move Sente updates its internal board state which permits both entities to play a competitive game. Sente is also used to police interactions between the user and AI models ensuring all played moves are legal and identifying the winner at the end of the game. Sente’s convert to numpy function is also used to generate training data for the systems AI models.
## The Data Pipeline
The Data Pipeline component is not used during standard user software interaction but does serve the critical role of generating training data for the AI models used in the main system. The Data Pipeline is tasked with modernizing our old SGF files to be compatible with Sente, Converting SGF files to numpy arrays for training purposes, and training convolutional neural networks on the data. The pipeline loops over each SGF file and converts each board state into X data, and the human moves into y data.

The X data takes the shape (Nx19x19x4) where:
N, is the number of converted boards in the data frame
19x19, is the shape of a single Go board
4, is the number of channels the model will see (White Stones, Black Stones, Empty Intersections, Ko Points)
These channels are create by Sente’s numpy conversion which is why they are chosen for our purposes.

The y data is a one-dimensional array of integers between 0-360 which encodes for all possible moves a human may take.

All the X and y data pairs from all converted games are collected into master arrays which are saved to the disk for training purposes.
## Pytorch and Model Structure
Pytorch is the machine learning library used to create and run models in this project. Pytorch was used to create and train residual convolutional neural networks. Our models take as input a 19x19x4 array which encodes the current state of the board as has been previously discussed. The hidden layer of models is a 20-layer Residual Network (ResNet) at 128 channels. Because Go is a very shape and structure-based game, a ResNet architecture is ideal for picking up and recognizing complex and abstract features of the board. Because we are using a rather large deep learning network ResNet has the additional advantage of mitigating the degradation problem often suffered by deep networks. The output layer of the models is a linear network which maps to 361 coordinates to represent where the model predicts a human would play a stone.
## NumPy
NumPy is used to create and save training data using memmap arrays. Memmap are functionally similar to a standard numpy array with the exception of allowing memory streaming from the disk. Numpy’s memmap arrays enable revival of training data files which may exceed the system's available ram by streaming the array data directly from the disk during model training. This ensures that training data is accessible even if the raw files are larger than our computers can handle.
Tkinter and the User Interface
The user interface is the primary component the user interacts with. The system manages user moves and allows for the selection of options like move recommendation or model diffaculty. The system interacts with Sente and the Main Game Logic system primarily to help facilitate a functional game of Go. The UI elements themselves are created using the Tkinter library which features built-in support for window creation, menu options, and user input.
## The Model Component
The Model Component acts as a virtual adversary for the end user. The system primarily interacts with Sente and the Main Game Logic System. The component is primarily responsible for making moves to oppose the user along with rating and recommending moves to the user. One of the primary functions of this component is to convert the models’ default tensor output into playable moves. This is done by ordering the tensors by highest to lowest value and pulling their corresponding board locations between 0-360. This rank order of moves can be converted to standard x, y coordinates on the board which allows the models to play a move or rate/recommend moves to the user.

In order to ensure the AI behavior is always nondeterministic there's a 20% chance that the model’s highest rated move will be skipped and the runner up move will take its place which will be subject to the same 20% chance of being skipped. This process of skipping moves can happen a maximum of five times. The main reason this is done is to prevent the AI models from playing the same moves in the same situations, by introducing an element of randomness to move selection. This system also has the added benefit of preventing the models from playing the same type of move repeatedly.

Lastly the model component is tasked with estimating the game’s outcome and using that figure to resign on behalf of the AI systems. The component employees Bouzy's Algorithm to estimate the outcome of the game after for every move passed 150. If the model is severely disfavored by the score estimation algorithm, predicted to lose by at least 15 points, it will automatically resign from the game.

## Main Game Logic
The Main Game Logic system interacts with all the components described above. Its primary job is to facilitate smooth interactions between all the core system components. It is responsible for handling user selected options along with instructing Sente to set up and restart games appropriately. Additionally, this system handles user AI interaction by passing user moves into Sente and calling AI models to generate opposing moves or recommend and rate moves. Essentially this system serves as a glue for all other program components (barring the Data Pipeline).
## Training Data
The training data for our models came from a publicly available Go data set on GitHub. This repository was chosen because it hosts human games broken down into different skill levels and stored in smart game format (SGF) files. These files store every move played for a given game of Go and can be read and converted into numpy arrays by Sente. In order to train three different models at three different skill levels we chose the directories in the 18K, 11K, and 8d skill brackets.
The breakdown of the skill levels is as follows:

| **Model Difficulty**|**Skill Rank**|**description of skill level**|
|---------------------|---------------|------------------------|
|Essay model|18k|This rank is often given to beginners who are just starting|
|Intermediate Model|1k|This rank is achieved by skilled beginners|
|Hard Model 8d|8d|This rank is just before professional level and only achieved after years of experience|

Unfortunately, the public repository we used did not have enough games at the professional level to serve as sufficient training data, so we used next best rank ‘dan’ as a replacement. Altogether our models trained on approximately 5000 games in their respective categories.

# exemplary pieces of code
# Jonah Benton - convertSGFtoNumpy.py
The section of code convertSGFtoNumpy.py is the primary element of the Data Pipeline and is responsible for converting raw SGF files to numpy data frames which can serve as X and y data for model training. Because our models attempt to predict what a human would play for a given board state the X data represents the state of the board and the y data represents the move a real human played on that state. 

The following function in convertSGFtoNumpy.py is responsible for converting an entire SGF file into X data.

```python
def convert_move_to_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_moves = np.zeros((len(sequence)),dtype=np.uint16)

    for i in range(len(sequence)):
        x = sequence[i].get_x()
        y = sequence[i].get_y()
        game.play(sequence[i])
        all_moves[i]=(y*19)+x

    return all_moves
```
The game object passed into this function is used to represent and store an entire game of Go from an SGF file; how this object is created will be discussed later. 
```python
game.advance_to_root()
sequence = game.get_default_sequence()
```
The first line ensures that the game is ‘advanced to root’ that it is in the state of an empty board with no moves played. The sequence object stores the list of all moves played in the game object. 
```python
all_board_states = np.zeros((len(sequence), 19, 19, 4), dtype=np.uint8)
all_board_states[0, :, :,2]=1 # Fills the first frame with the values found in an empty board
```
The all_board_states variable will be used to store every converted board state for each game. The length of the array is set to the length of sequence or the total number of moves played in the game. The following 19x19x4 parameters represent a single board state where 19 by 19 is the dimension of a standard Go board and four represent each channel that will be presented to the model during training. The channels represent white stones, black stones, empty points and ko points. The following line sets the second index of the array's first position to all ones which represents an empty board. If this is not done the first index will erroneously store board with the first move all ready played rather than an empty board.
```python
for i in range(len(sequence)-1):
    game.play(sequence[i])
    board = game.numpy()

    if game.get_active_player() == stone.WHITE: # Flips white and black stones if its white's turn
        board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)

    all_board_states[i+1] = board # Adds board array to i+1 because the first index is an empty board
```
This loop progressively updates the game object with the next move from the sequence object; this has the effect of iterating over every move played in the game. After a move is played the board variable is used to store the numpy equivalent of the board state. The board is converted to a numpy array using Sente’s built-in ‘numpy()’ function. The board variable is passed into the next index of the all_board_states variable which effectively compiles every individual numpy array into one master array which stores every board state for an entire game. Some things to note here are that the loop only iterates for the length of the sequence minus one; this is because the final board state has no accompanying move as it is the last state of the game. All individual boards are passed into all_board_states[i+1] as the first index of that array is reserved to store an empty board.
```python
if game.get_active_player() == stone.WHITE: # Flips white and black stones if its white's turn
    board = np.stack([board[..., 1], board[..., 0], board[..., 2], board[..., 3]], axis=2)
```
This if statement essentially flips the position of the white and black stones whenever it is White's turn. Only the first two channels are flipped because Go is symmetric across color, so the other channels need not be changed. The reason this is done is to essentially trick the model into always believing it is playing as black. Doing this removes the need to add a color input to the data frame.

The following functions are responsible for converting individual human moves into a numpy array; it functions in a similar manner to the above function which converts entire board states.
```python
def convert_move_to_numpy(game):
    game.advance_to_root()
    sequence = game.get_default_sequence()
    all_moves = np.zeros((len(sequence)),dtype=np.uint16)

    for i in range(len(sequence)):
        x = sequence[i].get_x()
        y = sequence[i].get_y()
        game.play(sequence[i])
        all_moves[i]=(y*19)+x

    return all_moves
```
This code is used to iterate over every move played in a given Go from an SGF file and convert them into target data.
```python
game.advance_to_root()
sequence = game.get_default_sequence()
all_moves = np.zeros((len(sequence)),dtype=np.uint16)
```
This code sets the game to root and creates the sequence object along with creating a numpy array all_moves which is a one-dimensional array equal to the length of the sequence used to store y data.
```python
for i in range(len(sequence)):
    x = sequence[i].get_x()
    y = sequence[i].get_y()
    game.play(sequence[i])
    all_moves[i]=(y*19)+x
```
This loop iterates over every single move played in the game and converts each move into a number ranging from 0 – 360 (resenting all possible 361 moves). The first two lines in the loop find the x and y coordinates of the human made move which both scale from 0 to 18. The next line iterates the game object to the following move. The last line passes in the human move into the all_moves array by multiplying y by 19 and adding x creating a number from 0 - 360.

The last major function convert_all_games() loops over every single SGF file in a directory and converts the contents of each game into a master collection of data frames representing the entire directory including all games. The first major section of this function can be seen below:
```python
def convert_all_games():

    x_file = rf'{training_data_path}\X_file.npy'
    y_file = rf'{training_data_path}\y_file.npy'

    x = np.zeros((num_frames, 19, 19, 4), dtype=np.uint8)
    x.tofile(x_file)

    y = np.zeros((num_frames,), dtype=np.uint16)
    y.tofile(y_file)

    x = np.memmap(x_file, dtype=np.uint8, mode='r+', shape=(num_frames, 19, 19, 4))
    y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(num_frames,))

    total_errors=0
    total_frames=0
```
The purpose of the above code is to establish the file locations where the master collection will be stored, create the arrays to store the data in, and establish variables to track progress and number of errors.
```python
x_file = rf'{training_data_path}\X_file.npy'
y_file = rf'{training_data_path}\y_file.npy'
```
These two variables represent the file location in which the training data will be stored. The training_data_path variable holds the location internal to the projects directory where data should be held.
```python
x = np.zeros((num_frames, 19, 19, 4), dtype=np.uint8)
x.tofile(x_file)

y = np.zeros((num_frames,), dtype=np.uint16)
y.tofile(y_file)
```
This code is responsible for creating memory maped numpy arrays to store the converted training data. The num_frames variable is used to control the total number of board states/moves which need to be converted into data frames. X and y possess the same shape as has been described above with the exception that they are far longer in length to accompany more frames than are found in a single game. By default, x and y will be over one million indices in length to store approximately 5000 converted games. The function tofile() saves the arrays to the disk.
```python
x = np.memmap(x_file, dtype=np.uint8, mode='r+', shape=(num_frames, 19, 19, 4))
y = np.memmap(y_file, dtype=np.uint16, mode='r+', shape=(num_frames,))
```
Here x and y are redefined into memmep arrays which are capable of holding more data than can fit in system RAM. This is done to ensure that training data is accessible even if the file size is larger than system memory allows.
```python
total_errors=0
total_frames=0
```
Not every game in our data set is consistent with Sente’s internal rules and as a result will throw an error when attempting to convert into a numpy array. The total_errors variable is used to track the total number of such errors so that data loss can be measured. The total_frames variable is used to track the total amount of board states/moves that have been converted as the function iterates over the directory. 
```python
for index, file_path in enumerate(SGF_directory_path.iterdir()):
    # Loads one game from the SGF directory
    try:
        game = sgf.load(str(file_path), ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
        sequence = game.get_default_sequence()
        current_frames = len(sequence)
    except sente.exceptions.InvalidSGFException:
        total_errors += 1
        continue

    try: # Fills the Training data frames with the converted data
        x[total_frames:total_frames+current_frames] = convert_board_state_to_numpy(game)
        y[total_frames:total_frames+current_frames] = convert_move_to_numpy(game)
        total_frames += current_frames

    # Some games are not compatible with sente's rule so this track to number of games which cannot be converted
    except sente.exceptions.IllegalMoveException:
        total_errors+=1
```
Above is the main loop which systematically iterates over every SGF file in the directory and converts the individual games within to data frames.
```python
game = sgf.load(str(file_path), ignore_illegal_properties=True, fix_file_format=True, disable_warnings=True)
sequence = game.get_default_sequence()
current_frames = len(sequence)
```
This code converts an SGF file into a game object and stores the length of the game and the current frames variable. It is encapsulated in an exception statement because some SGF files break Sente’s internal rules and as a result cannot be converted.
```python
x[total_frames:total_frames+current_frames] = convert_board_state_to_numpy(game)
y[total_frames:total_frames+current_frames] = convert_move_to_numpy(game)
total_frames += current_frames
```
This code converts the current SGF file into its associated numpy data frames as has already been described. The critical difference here is that those data frames are then passed into the master collections of x and y. The correct indices of x and y to pass in the freshly converted data frames can be found by traversing from the total number of already converted frames to the length of the data frames which are being passed in. Finally, this code updates total frames with the number of frames just processed and collected. The code is encapsulated in an exception statement to catch any instances of games which do not match Sente’s rules and prevent the entire system from crashing.
```python
if index%100==0: # Prints progress updates to the console
    print(f'Converted {index} games')

if total_frames>num_frames-1000: # Stops loop before the array size limit is reached
    print(f'Total Errors {total_errors}\nTotal Frames {total_frames}')
    x.flush()
    y.flush()
    break
```
This code is tasked with periodically printing updates to the console and ending the loop when the target number of board states/moves are converted. The code will print a simple update every 100 converted games. The final statement is responsible for ending the loop once all necessary conversions are complete. It does this by checking if the total number of converted frames is greater than the number of desired frames minus a buffer window of 1000 frames. Because games of Go are not deterministic it's impossible to know how many frames will be converted per game so here a buffer of 1000 frames are used to ensure that the memory limitations of the numpy arrays are never exceeded as it's virtually impossible for game of Go to exceed 1000 moves. The final lines of code are the flush function which commits the changes to the x and y memmap arrays to the disk.

All put together this code can convert an arbitrary number of SGF files into usable numpy data frames for model training and evaluation.

# Casey Perlinger-Jett - main_game_logic.py
The section of code main_game_logic.py is the main file for all UI elements of the project. The file itself contains all code for menuing, UI, and the user-side of playing the game of GO, with the occasional AI Model call too. This is the front-end of the GO project powered by python tkinter.
```python
# NOTICE: The was restructured into the __init__() and other def X() style under classes through
# the direct involvement of Google AI.
# The underlying code was freshly sourced through articles and YouTube tutorials.
```
This is what you’ll find lining the top of the code. This is because personally I started the code with a bunch of loose functions that I figured would progress into multiple files. Then while learning how to create a new window in tkinter, with Google AI assistance, I informed me that classes would be the best way to go about the multiple screens. 
```python
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
```
Leading into our first bit of real code found within the SelectionScreen class. This here shows off the widely used buttons. Here we have the main menu buttons, which all have the same variable name because it did not matter what their names were, since nothing else is calling them. They first call root, as almost everything else does, because that is calling to the base window, and from there, all other windows can be formed. 
This method brought on one unique issue, which was sometimes buttons would instead of displaying on their respective window, would display on the main menu. 
From there, you have the display text and the width of the button. Then you have ‘command’. This simply is a function call upon the button being pressed. One thing I learned is that if the function has parentheses on it, it loads immediately on the code loading, but without them, it loads when the button is clicked. Here we see each call an above function, without parentheses, because it failed with them, all three of which open a new window.
The three functions all have functionally the same code. playGO() also has the global variable game, which contains the entire gameboard that gets printed out on the game window. However, each defines a new window with the built-in tk.Toplevel(root) and then calls its respective class within the file that will then populate the new window.
The idea of everything being its own window rather than maneuvering through one window was chosen because it was a lot easier due to the fact that at no point does data need to be deleted except for when a window is closed.
```python
model8dON = tk.Radiobutton(root, text = "Turn ON MODEL 8d", value = "model8dON", variable = radioVar2, command = self.turnOnModel8d)
model8dON.pack()
model1kON = tk.Radiobutton(root, text = "Turn ON MODEL 1k", value = "model1kON", variable = radioVar2, command = self.turnOnModel1k)
model1kON.pack()
model18kON = tk.Radiobutton(root, text = "Turn ON MODEL 18k", value = "model18kON", variable = radioVar2, command = self.turnOnModel18k)
model18kON.pack()
```
Moving on to another form of button is the radio button. Above is the code for choosing the AI model in settings. Similar to the other buttons, all apart from the variable aspect of them. This determines which set the button is associated with. Since all three above have the same variable, they are part of the same set (i.e., only one of the three above can be selected at a given time).
```python
def turnOnModel8d(self):
    global model8dON, model1kON, model18kON
    model8dON = True; model1kON = False; model18kON = False
    print("Go_model_8d.pth")
```
One of the three functions called from the above radio buttons. Each sets the other two model variables to False and its own to True such that you can click the buttons as many times as you want and not have to worry about issues arising. (Also because by default model 8d is set to True in case the user doesn’t go into settings so that it doesn’t crash.) It also contains a print statement to test that the buttons are working.
```python
model_path = ''
if model8dON:
    model_path = "Go_model_8d.pth"
    print("Go_model_8d.pth")
elif model1kON:
    model_path = "Go_model_1k.pth"
    print("Go_model_1k.pth")
elif model18kON:
    model_path = "Go_model_18k.pth"
    print("Go_model_18k.pth")
```
Getting into the GOGame class now, here actually sets the AI model by going into the AIHandler file with the respective model path, and then prints out the path to test which model actually gets sent to the model_handler file.
```python
### USER TURN
rateMove = "N/A (Pass)"

user_input = simpledialog.askstring("Input", f"Move (ie: X,Y) or 'pass' or 'resign': ")
user_input = user_input.replace(" ", "").replace("(", "").replace(")", "")

# Specify that user intends to pass.
if user_input == "pass" or user_input == "":
    game.pss()
elif user_input == "resign":
    self.game.resign()
    self.endGame()
    return
elif user_input == "switch":
    self.modelSwitcher()
    return
else: 
    x, y = map(int, user_input.split(','))
    rateMove = AIHandler.rate_user_move(self, game, (x, y))
    game.play(x,y)
# Update UI with move.
self.gameBoard.config(text=str(self.game), font = "Courier 20")
self.turnIndicator.config(text="\nAI TURN", font = "Verdana 15 bold")

if game.is_over():
    self.endGame()
    return
```
Now this is the core of the game: the user’s turn in the game of GO. Breaking it down
```python
user_input = simpledialog.askstring("Input", f"Move (ie: X,Y) or 'pass' or 'resign' or 'switch: ")
user_input = user_input.replace(" ", "").replace("(", "").replace(")", "")
```
This prompts, receives, and cleans the user’s input. Using the built-in simpledialog prompting, and then removing any spaces or parentheses the user might’ve put into their input (i.e. '( 4, 4)' → '4,4') This is needed for the sake of reading the data into a playable move later on, and for the sake of having some leeway in the user input so that it's not so strict.
```python
if user_input == "pass" or user_input == "":
    game.pss()
elif user_input == "resign":
    self.game.resign()
    self.endGame()
    return
elif user_input == "switch":
    self.modelSwitcher()
    return
else: 
    x, y = map(int, user_input.split(','))
    rateMove = AIHandler.rate_user_move(self, game, (x, y))
    game.play(x,y)
```
Reading the input now we check for three special cases before defaulting to mapping the cleaned input into an x and y for a playable move. Which is also run through the AIHandler file for the move to be rated and then have that rating stored in this file for it to be printed out if the setting is selected. PASS or "" voluntary skips your turn. RESIGN which immediately ends the game. Along with SWITCH which then prompts you to select one of the three models to switch to mid-game. 
Beyond that it updates the displayed text on the screen and checks if the game has concluded or not using a built-in Sente function. Which doesn’t have anything all that complex to it. Except for the self.endGame() call. Within that statement it is immediately followed by a return which is required to exist otherwise the statement wouldn't work because the mainloop() iterating over everything would just pass on by it. 
```python
def makeMoveWhite(self, event=None):
    self.root.bind("<Return>", self.makeMoveBlack)
    rateMove = "N/A (Pass)"
    
    ### AI TURN
    self.button.config(text='Make Move', command=self.makeMoveBlack)
    self.button.pack()
    self.turnIndicator.config(text="\nYOUR TURN", font = "Verdana 15 bold")

    if game.is_over():
        self.endGame()
        return
```python
This was, what I thought, a semi-clever solution to the codebase. makeMoveBlack() does not have anything about it that ties it to the user playing the black pieces, except for the user going first and alternating with the AI, thus preserving their black pieces' stature. So instead of repeating the code, but flipped, I only put the AI turn in makeMoveWhite(), and furthermore set it so that the keybind and displayed button flip to call the makeMoveBlack() function after the AI plays. I did so because by setting apart the one AI turn, then all subsequent turns move up one turn in the sequence, putting the user back on player 1 and the AI up after the user, allowing for the switch into the makeMoveBlack() function.
Another point to note is the event=None in the function intake. This allows for keybinds to occur within and during the function.
```python
if __name__ == '__main__':
    app = SelectionScreen() # This was brought to you by Google AI.
    root.focus_set() # Allows for hotkeys
    root.mainloop() # Main loop over entire file.
```
The last piece of code I’d like to discuss here is the intializer at the bottom of the file because it contains three key pieces of code that need explained. First is the app = … Which was brought to my attention by Google AI while discussing tkinter windows. This line defines the starting window that will first display when the code is launched. Second is the root.focus_set() which is the built in tkinter function that allows for keybinds to work. Lastly root.mainloop(), which is the built in loop function of tkinter that continuously updates the entire project while its running, allowing for very cool things like the makeMoveBlack() function looping until the game finishes without any explicit code telling that function to do that. The downside is that it completely breaks other loops like for and while, which I found out while trying to implement a while loop.
All code discussed is what I’d call important pieces either for the understanding of widely used pieces of code across the main_game_logic.py file or for the understanding of crucial pieces of code within main_game_logic.py. 

# Test Procedures
Because our AI systems are not deterministic most of our tests revolve around ensuring that the model is producing correctly structured data. This involves things such as ensuring the model is inferring correct rankings of all possible moves, that the code is selecting only legal moves, and labeling user moves appropriately. The following is a series of test protocols designed to achieve these aims.
## Model Inference
Because the model needs to output a ranking of moves across the entire board space of 361 possible moves a test can be designed to ensure the model output is appropriately structured. This test protocol ensures that the output distribution of the model is a list of integers 361 indexes in length.
## Move Legality
Because our models are tasked with playing a game of Go, their output needs to consist of moves on a 19 by 19 grid and be legal relative to the current board state. This means that the model's output of rank moves in the form of a single integers. must be converted into a two-dimensional coordinate. This test procedure ensures that the two-dimensional coordinate output by the code is within the confines of a standard game of Go in legal as per the rules.
## Move Ranking
Our system is tasked with offering move ratings to the user upon request. This involves predicting a best to worse ranking of all moves across the entire board space. And finding the user’s move in that list. Our system tests this functionality by submitting a mock distribution with known rankings for individual move coordinates. If the code correctly labels individual coordinates with the correct ranking this validates the underlying ranking logic.
Along with finding the ordinal ranking of the user's move the system must also correctly label it as either excellent mediocre or a blunder. This can be done by creating a mock distribution of numbers 1 to 361 randomly shuffled in a deterministic fashion to mimic a distribution created by the models. Because the distribution is deterministic, certain coordinate locations of moves have predefined labels which can then be tested. If the code correctly returns the correct labels for the correct move coordinates, then it is working appropriately.
## Manual Play Testing
The final test our AI model undergoes is a play test to catch problems with move selection, rating, or recommendation which cannot be caught by automated tests. This manual test looks for problems like illogical moves, nonsensical ratings, or non alignment between recommendations and move quality rating. This testing helps to eliminate problems with non-deterministic code which automated tests cannot identify.
## Model Selection/Switching
Our project employs three distinct AI models for the user to go up against in the game of GO, so it’s important that each is able to be properly selected somehow. We do so through the settings window branched from the starting menu. By manually testing this, by selecting each model and printing the results to the terminal, we ensure that each model can be correctly selected from the settings menu. This also applies to mid-game model switching selection.
## Toggleable Move Rating/Recommendation 
The project allows for the user to toggle whether they want to have Moves Recommended and/or Rated during their game of GO. This manual test sets to show that all four ways of toggling move Rater and Recommender work as intended. Such that within the game, moves are only rated if and only if Move Rater is toggled on in settings, and only recommended if and only if Move Recommender is toggled on in settings. 
## Black/White/AIvAI Selection
The project allows for the user to select their piece color when they decide to play a game of GO within the project. This manual test sets to show that the user’s selection of piece color works as intended, along with allowing for the user to select a third AI vs. AI mode.
## Game Ends
The project should be able to detect the end of a game so that it can display the results. By employing the AI model to play against itself, we are able to run through a simulated game quickly to test whether the game will properly end or if an error regarding the mainloop() occurs.
## UI Game Output
The project utilizes tkinter for its UI. This test is a manual test that simply looks to observe that the game board is correctly updated after every user turn and AI turn, including the removal of captured stones. Along with the Move Rater and Move Recommender, getting correctly updated after each round of user and AI moves.
## Test Driven Development
The purpose of this test was to ensure that the inference function produced a list of 361 distinct integers which serve as a ranking of each possible move. Should the function fail to return a list of integers of the appropriate properties the test will fail.

Failing test:

![Alt text](Images/fail_1.png)

This test failed because the function returned an integer object rather than an array of distinct integers. The function incorrectly returned an editor object in an attempt to convert the model output into an integer array. Code was refactored to return the entire data object without casting to an integer.


Second Failure:

![Alt text](Images/fail_2.png)

The test failed because the function returned an array of two data objects, the output tensor and a list of integers which encodes the board locations from highest to lowest quality. The code was refactored to return the second object.

Third Failure:

![Alt text](Images/fail_3.png)

This test failed because the array of integers that needed to be outputted was wrapped in another object array which caused its length to be interpreted as one rather than 361. Code was refactored to incorporate a numpy conversion which unwrapped the object and successfully returned the array of 361 integers passing the test.
## Test Driven Development 2
The purpose of this test is to ensure that the game opens the ending results window when the game comes to an end. To test this I used the AI self play to quickly iterate through a test game. The test began with its first failure of what happens when the AI runs out of moves. At the time it turns out the code just creashed.
![Alt text](Images/Refactoring_endGame()_1.png)
So the code needed a few cases patched up, which is what happened afterwards. However then a new problem arised.
![Alt text](Imasges/Refactoring_endGame()_2.png)
The issue is that in the game of GO when both players pass their turn consecutively, the game ends, however, as we can see that wasn't the case here. Instead it just continued on forever.
![Alt text](Images/Refactoring_endGame()_3.png)
Here on the third, documented, iteration of the testing, we were able to get it to recognize a statement within the function upon the game ending, however, it was not able to call a function outside of the iteratng selfplay function which I found very odd.
![Alt text](Images/Refactoring_endGame()_4.png)
In this case it there was a slight bit of human error. 'self.endGame()' is the working code, however, it requires a 'return' after the function call otherwise it can't escape the playing loop the game was currently in. Thus after adding a 'return' to the end of the endGame statement it was able to properly load the results screen, passing our test.

## References
During development we used ChatGPT and Google Gemini mainly as knowledge tools to help with using frameworks like NumPy, Sente, and Pytorch. Due to unfamiliarity with Pytorch Gemini was used to generate code which creates and evaluates AI models although the code was altered for our purposes. All AI generated code is marked by comments in the project files

The medium article Understanding ResNet Architecture: A Deep Dive into Residual Neural Network by Azeem – 1 was used to help understand and explain ResNet Architecture.

Azeem - 1. (2023, November 14). Understanding resnet architecture: A deep dive into residual neural network | by Azeem - I | Medium. https://medium.com/@ibtedaazeem/understanding-resnet-architecture-a-deep-dive-into-residual-neural-network-2c792e6537a9

GeeksforGeeks. (2025, July 14). Python tkinter tutorial. https://www.geeksforgeeks.org/python/python-tkinter-tutorial/
GeeksforGeeks was accessed many times to learn how to utilize tkinter and its built-in functions.

Klein, B. (2022, February 1). Tkinter - the python interface for Tk. Tkinter - the python interface for Tk | Tkinter. https://python-course.eu/tkinter/
Python documents and tutorials were also accessed to learn and understand tkinter for this project.




