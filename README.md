# CS5800 Final Project - Knight's Tour with Backtracking

## Description
The Knight's Tour problem involves moving a knight on a chessboard such that it visits every square exactly once. This project implements the Knight's Tour using a backtracking algorithm. The algorithm recursively attempts to complete the tour by trying all possible knight moves from the current position, backtracking if it reaches a dead end.

## Algorithm
The algorithm uses a depth-first search (DFS) approach with backtracking to explore all possible knight moves from a given starting position. It marks each square as visited and attempts to move the knight to the next valid position. If it completes a full tour, it outputs the sequence of moves; otherwise, it backtracks and tries a different path.

## Inputs and Outputs
### Inputs
- Board size (N x N) where N is an integer.
- Starting position of the knight (optional, default is (0, 0)).

### Outputs
- A sequence of moves representing the knight's tour if one exists.
- An error message if no tour exists.

## Usage
### Command Line
To run the Knight's Tour algorithm, use the following command format:

```sh
python knights_tour.py <board_size> [start_x] [start_y]