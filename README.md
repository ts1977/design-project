# design-project
Design project proposal
Topic: checkers game with artificial intelligence

 

Rules of checkers: Two players game. Each player has 12 chess pieces. The board is composed with 8*8 grids. Only the dark colored square 
are used in play. The object of the game is to capture all of opponent's checkers so that your opponent has no available moves. 

Movement: Basic movement is to move a checker one space diagonally forward. You can not move a checker backwards until it becomes a King. 

Jumping: If the jump is available, you must take the jump. If one of your opponents checkers is on a forward diagonal next to one of your
checkers, and the next space beyond the opponent's checker us empty, then your checker must jump the opponent's checker and land in the
space beyond.

Crowning: when one of your checkers reaches the opposite side of the board, it is crowd a and becomes a King. Your turn ends there. The 
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
