# Machine Learning Checkers


Rules of checkers: Two players game. Each player has 12 chess pieces. The board is composed with 8*8 grids. Only the dark colored square
are used in play. The object of the game is to capture all of opponent's checkers so that your opponent has no available moves.

Movement: Basic movement is to move a checker one space diagonally forward. You can not move a checker backwards until it becomes a King.

Jumping: If the jump is available, you must take the jump. If one of your opponents checkers is on a forward diagonal next to one of your
checkers, and the next space beyond the opponent's checker us empty, then your checker must jump the opponent's checker and land in the
space beyond.

Crowning: When one of your checkers reaches the opposite side of the board, it is crowd a and becomes a King. Your turn ends there. The
king can move backward as well as forward.

## Dependencies

* Python3
* Keras
* Numpy
* Tk (for graphics)

We used the latest version that ships with anaconda3.

## Running the Game

To run the game:

```bash
python game.py --model <model> [--train]
```

The `--model` flag allows the user to select a trained model from the disk. These are stored in
the `save` directory. There are many pretrained model provided in the repository. To load the model associated with a `*.h5` file in the `save`directory, for example, `simp11.h5`, used `--model simp11`, without the `.h5` extension.

The `--train` specifies whether or not you want the model to be trained on the result of the game.

When running the game the GUI will pop up and prompt the user to choose going first or second.
The Red pieces play first. To make a move, select the checker you wish to move. The selected checker
will be highlighted gray. Then select the destination spot to finish the move. An error will appear if any
of the mouse clicks were invalid.

## Training

To train a model:

```bash
python train.py --model <model> --episodes <number_of_games>
```

Similar to the game, `--model` will continue training the model specified (as before, no path or extension is used). You can also provide a new name, and it will begin training a new model from scratch.

The `--episodes` is used to specify the number of games that should be played in the training process.

Because the model is trained at the end of each game, and results are periodically stored to disk,
a training session can be aborted and resumed later.

