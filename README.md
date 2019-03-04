# pygame-sudoku
soduku game in python and pygame.  Class project

This code includes two sides of sudoku, 1) a playable space that will load a random game (one of five) and let users play the game.  The features of this game include a) hints, b) showing erros, c) Undo functionality and d) a "pencil" space where the user can note the possible answers as they go along.  The other side (2) is a solver.  This space allows the user to enter any sudoku game (e.g., from the newspaper) and the program will attempt to solve the puzzle.  Currently, the logic includes a) sole possible, b) unique possibility and c) "naked subset" pair logic.

Most basic to medium rated puzzles can be solved.

If a new puzzle is solved, it is saved to then be used by the playable space for a future game play.

Logic steps are formalized here: https://www.kristanix.com/sudokuepic/sudoku-solving-techniques.php and I am coding them into my python logic.

This project also incoproates pygame so that the entire game is visual and interactive.

