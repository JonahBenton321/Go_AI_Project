# Introduction
Our system was designed with the primary motivation of providing users with a human-like opponent for the Chinese game Go. Most Go-based software is designed to offer a virtual opponent optimized around winning matches.  We wanted to create a virtual set of opponents that would play more in a human-like style while still presenting some moderate challenge to the end user. The system creates a virtual Go game and presents an interactive UI for the user. The software offers the user the choice between three different AI models trained on three different skill levels of data. This creates a set of optional opponents at varying levels of difficulty. The software also utilizes the model trained on the highest tier of human data to serve as a move rating and recommendation system. These functions help the user to improve their skill with the game and make decisions in tough areas of strategy. Overall, the goal of the software is to help users improve skill in the game without presenting virtual opponents optimized for victory alone.
# Time Log
# Requirements
## Go Game Engine - complete
Our system presents a fully functional game of Go to the user using the Sente library as the primary engine to run the game of Go on the back end. Our system offers an interactive UI to allow human users to smoothly input moves and see model responses displayed on the game board.
## Neural Network AI - complete
Our software presents three convolutional neural networks which rrained on one million board states from their respective skill categories. The following data conveys the accuracy score each model achieved on a 10,000-board state test set which models were not trained on. The data effectively conveys how statistically human each model plays the game of Go.
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


