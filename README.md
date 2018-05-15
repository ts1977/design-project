# design-project
Design project proposal
Topic: checkers game with artificial intelligence



Rules of checkers: Two players game. Each player has 12 chess pieces. The board is composed with 8*8 grids. Only the dark colored square
are used in play. The object of the game is to capture all of opponent's checkers so that your opponent has no available moves.

Movement: Basic movement is to move a checker one space diagonally forward. You can not move a checker backwards until it becomes a King.

Jumping: If the jump is available, you must take the jump. If one of your opponents checkers is on a forward diagonal next to one of your
checkers, and the next space beyond the opponent's checker us empty, then your checker must jump the opponent's checker and land in the
space beyond.

Crowning: When one of your checkers reaches the opposite side of the board, it is crowd a and becomes a King. Your turn ends there. The
king can move backward as well as forward.

Programming language: python or C++

Algorithm: A+ algorithm, alpha beta algorithm, decision tree, neural networking

AI part: The ai improves itself by playing with human. After the ai plays with human, it adds the game records into its storage. In the ai turns, ai will analyse all of possible moves and select the move that has the highest winning probability.

With playing with human, the ai can judge the states of game independently. The states includes
1. number of own uncrowned pieces.
2. number of opponent's uncrowned pieces.
3. number of own crowned pieces.
4. number of opponent's crowned pieces.
5. number of own pieces on the right or left edge of the board
6. number of opponent's pieces on the right or left edge of the board
7. own piece which will be captured in next turn
8. the total vertical moving distance from the starting position

To achieve more advantageous situation, if there is no obligatory capture move, ai tends to make move following rules below.
1. increase the number of own crown pieces
2. prevent opponent changing the uncrown piece to crown piece
3. increase the number of own pieces on the left or right edge because those pieces can't be captured
4. prevent own pieces to be captured by opponent

Plan of project:
First two weeks: learn some related machine learning and artificial intelligence knowledge
Second two weeks: make the GUI part of the checkers
Third two weeks: improve the GUI part to make the interface more beautiful and functional and debug the GUI part
Fourth two weeks: apply the artificial intelligence algorithms to the game. The game will work after applying the algorithms.
Fifth two weeks: Improve the algorithms. Add more details and make it play like a human player.
Sixth two weeks: debug the program and fix all errors.

## Linear Learning Algorithm

The Learning Algorithm we will develop will use a mixture of supervised and unsupervised techniques.

Our goal will be to develop a linear regression model that will be able to convert the state of the board into a single numeric score. This way, given a list of possible legal moves, the algorithm will simply choose the board with the highest score as being the best choice.

We will evaluate each board by extracting a features from that board. For example, the number of pieces of each player, the number of kings, and the number of pieces that each player has threatened. This gives a feature vector, x. To evaluate the board, we calculate the dot product, &omega; * x

To obtain a vector of weights we will use the gradient descent algorithm, on

To set a baseline, we will write the baseline truth examples, such as the states that correspond to win, lose, and the opening state. We will assign these arbitrary values, such as 1000, -1000, and 0 respectively. To find values for the intermediate states we will use the following heuristic. Assuming that we are playing an intelligent player, we can assume that he always chooses the "best" possible move. Thus, we can assume that board that we receive back from the opponent is the optimal play. Since each move is contingent upon the previous move, our algorithm should rate each board as being approximately the same value as the board that will follow afterward. For example, a board that causes the machine to lose on the next round should have about the same value as losing, and a board that leads the machine to win on the next round should have the same value as winning.

We can thus accumulate a training set of data, which contains pairs of moves made by the AI, and the resulting board that the opponent played. Instead of storing the actual configuration of checker pieces, we will store the pair of feature vectors that were extracted from each board.

We can then use the standard gradient descent algorithm to train the weights on the data. There a few variation s that we will try. Either we will store all the data, and on each turn update the weights by doing a single step of gradient descent. Alternatively, we can use online learning, in which we use each board transition as it occurs to make an update, and then discard the training example. If we use online learning, we would probably need to do an update against the baseline truth examples (at some set interval) to make sure that the weights do not stray too far (the fear is that we rely too much on our estimation of the opponent as always making the best choice). (Alternatively, we could use a data aging process, were older data is slowly devalued, and then eventually discarded).

To make an update to the weights we do: &omega; <- &omega; + &alpha; * (h(x<sub>n+1</sub>) - h(x<sub>n</sub>))

## Dependencies

* Python3
* Keras
* Numpy

We used anaconda3 for this project.
