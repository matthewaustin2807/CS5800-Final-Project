# CS5800 Final Project - Knight's Tour with Backtracking

## Description
The Knight's Tour problem involves moving a knight on a chessboard such that it visits every square exactly once. This project implements the Knight's Tour using a backtracking algorithm. The algorithm recursively attempts to complete the tour by trying all possible knight moves from the current position, backtracking if it reaches a dead end. Additionally, this implementation includes a visualization of the knight's tour using the Tkinter library and a separate timing analysis feature using matplotlib.

## Algorithm
The algorithm uses a depth-first search (DFS) approach with backtracking to explore all possible knight moves from a given starting position. It marks each square as visited and attempts to move the knight to the next valid position. If it completes a full tour, it outputs the sequence of moves; otherwise, it backtracks and tries a different path.

## Inputs and Outputs
### Inputs
- **Board size (N x M)**: N and M are integers representing the number of rows and columns respectively.
- **Starting position of the knight (start_x, start_y)**: Optional, default is (0, 0).
- **Mode flag**: 0 for visualization, 1 for timing analysis.

### Outputs
- **A sequence of moves** representing the knight's tour if one exists.
- **An error message** if no tour exists.

## Usage
### Command Line
To run the Knight's Tour algorithm, use the following command format:

```sh
python knightstour.py <rows> <columns> <start_x> <start_y> <0 for visual, 1 for time>
```

### Example Commands
- **Visualization Mode**: To run the Knight's Tour on an 8x8 board starting from position (2, 2) with visualization enabled:
```sh
python knightstour.py 8 8 2 2 0
```

- **Timing Analysis Mode**: To run the Knight's Tour on a 5x7 board starting from position (0, 0) with timing analysis enabled:
```sh
python knightstour.py 5 7 2 2 1
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