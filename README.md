# CS5800 Final Project - Knight's Tour with Backtracking

## Description
The Knight's Tour problem involves moving a knight on a chessboard such that it visits every square exactly once. This project implements the Knight's Tour using a backtracking algorithm. The algorithm recursively attempts to complete the tour by trying all possible knight moves from the current position, backtracking if it reaches a dead end. Additionally, this implementation includes a visualization of the knight's tour using the Tkinter library.

## Algorithm
The algorithm uses a depth-first search (DFS) approach with backtracking to explore all possible knight moves from a given starting position. It marks each square as visited and attempts to move the knight to the next valid position. If it completes a full tour, it outputs the sequence of moves; otherwise, it backtracks and tries a different path.

## Inputs and Outputs
### Inputs
- **Board size (N x M):** N and M are integers representing the number of rows and columns respectively.
- **Starting position of the knight (start_x, start_y):** Optional, default is (0, 0).
- **Visualization flag:** 0 for no visualization, 1 for visualization.
- **Timing analysis flag:** 0 for a single run, 1 for analysis.

### Outputs
- **A sequence of moves** representing the knight's tour if one exists.
- **An error message** if no tour exists.

## Usage
### Command Line
To run the Knight's Tour algorithm, use the following command format:

```sh
python knightstour.py <rows> <cols> <start_x> <start_y> <0 for no Visualization, 1 for Visualization> <0 for single run, 1 for analysis>
```

### Example Commands
- To run the Knight's Tour on an 8x8 board starting from position (2, 2) with visualization and analysis enabled:
```sh
python knightstour.py 8 8 2 2 1 1
```

- To run the Knight's Tour on a 5x7 board starting from position (0, 0) without visualization and analysis:
```sh
python knightstour.py 5 7 0 0 0 0
```

## Implementation
### knightstour.py
This script implements the backtracking algorithm for the Knight's Tour problem and handles command-line input. It includes optional visualization using Tkinter. It also performs a timing analysis of the algorithm and provides a graphical representation of the performance using 'matplotlib'.

### gui.py
This script contains the implementation of the visualization using Tkinter. It creates a graphical representation of the chessboard and animates the knight's moves.

## Dependencies
- Python 3.11
- Pillow (Python Imaging Library) for handling images in the visualization.
- Matplotlib for timing analysis visualization.

### Installation
To install the necessary dependencies, run:
```sh
pip install pillow matplotlib
```

## Group Members
- Matthew Chandra 
- Zuoyin Chen 
- Theresa Fu-Hsing Hsu 
- Md Mushfiqur Rahman Khan 