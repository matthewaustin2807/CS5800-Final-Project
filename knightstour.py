# Theresa Fu-Hsing Hsu, Matthew Chandra
# CS5800
# Summer 2024
# Bruce Maxwell
# Knight's Tour problem using backtracking in Python.

import sys
import time
import tkinter as tk
import random
from matplotlib import pyplot as plt
from gui import ChessBoard, squareSize

def visualize_algorithm(all_knight_moves, n, m):
    """Visualize the Knights Tour Algorithm using Tkinter

    Args:
        all_knight_moves (list): A list of coordinates of all of the knight's move in order from the starting position
        n (int): Number of Rows on the Board
        m (int): Number of Columns on the Board
    """
    root = tk.Tk()
    root.title("Knight's Tour Visualization")
    root.minsize(width=squareSize * m + 100, height=squareSize * n + 100)
    root.configure(background="papaya whip")

    chessBoard = ChessBoard(n, m, root, all_knight_moves)
    chessBoard.runVisualization()

    root.mainloop()

def visualize_algorithm(all_knight_moves, n, m):
    """Visualize the Knights Tour Algorithm using Tkinter

    Args:
        all_knight_moves (list): A list of coordinates of all of the knight's move in order from the starting position
        n (int): Number of Rows on the Board
        m (int): Number of Columns on the Board
    """
    root = tk.Tk()
    root.title(f"Knight's Tour Visualization")
    root.minsize(width=squareSize*m+100, height=squareSize*n+100)
    root.configure(background="papaya whip")
    
    chessBoard = ChessBoard(n, m, root,all_knight_moves)
    chessBoard.runVisualization()
    
    root.mainloop()
    
# Function to check if (x, y) is a valid move for the knight
def is_valid_move(x, y, board, N, M):
    """Check if the move to position (x, y) is valid.

    Args:
        x (int): The x-coordinate of the move.
        y (int): The y-coordinate of the move.
        board (list): The current state of the board.
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return 0 <= x < N and 0 <= y < M and board[x][y] == -1

# Function to count the number of valid moves from position (x, y)
def count_valid_moves(x, y, board, N, M, x_move, y_move):
    count = 0
    for i in range(8):
        if is_valid_move(x + x_move[i], y + y_move[i], board, N, M):
            count += 1
    return count

# Recursive function to solve the Knight's Tour problem
def solve_knights_tour(x, y, move_i, board, N, M, x_move, y_move, all_knight_moves):
    """Recursively solve the Knight's Tour problem using Warnsdorff's heuristic.

    Args:
        x (int): The current x-coordinate of the knight.
        y (int): The current y-coordinate of the knight.
        move_i (int): The current move index.
        board (list): The current state of the board.
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
        x_move (list): List of possible x-coordinates for knight's moves.
        y_move (list): List of possible y-coordinates for knight's moves.

    Returns:
        bool: True if the tour is complete, False otherwise.
    """
    # Base case: If all squares are visited, return True
    if move_i == N * M:
        return True

    # List of possible moves with their counts of subsequent valid moves
    possible_moves = []
    for i in range(8):
        next_x = x + x_move[i]
        next_y = y + y_move[i]
        if is_valid_move(next_x, next_y, board, N, M):
            count = count_valid_moves(next_x, next_y, board, N, M, x_move, y_move)
            possible_moves.append((count, next_x, next_y))

    # Sort the possible moves by the count of subsequent valid moves (Warnsdorff's heuristic)
    possible_moves.sort()
   
    # Try all possible moves for the knight
    for _, next_x, next_y in possible_moves:
        board[next_x][next_y] = move_i
        print("Move {}: ({}, {})".format(move_i, next_x, next_y))  # Debugging statement
        all_knight_moves.append([next_x, next_y])
        if solve_knights_tour(next_x, next_y, move_i + 1, board, N, M, x_move, y_move, all_knight_moves):
            return True
        # Backtracking
        board[next_x][next_y] = -1
        print("Backtracking from ({}, {}) at move {}".format(next_x, next_y, move_i))  # Debugging statement
        all_knight_moves.append('backtrack')

    return False

# Function to initialize and solve the Knight's Tour problem
def knights_tour(N, M, visualize, start_x=0, start_y=0):
    """Initialize the board and start the Knight's Tour.

    Args:
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
        start_x (int): The starting x-coordinate of the knight.
        start_y (int): The starting y-coordinate of the knight.
    """
    print("Starting Knight's Tour on a {}x{} board from position ({}, {})".format(N, M, start_x, start_y))
    # Initialize the board with -1
    board = [[-1 for _ in range(M)] for _ in range(N)]
    # Initial position of the knight
    board[start_x][start_y] = 0
    all_knight_moves = [[start_x, start_y]]
    # All possible moves for the knight
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]

    start_time = time.time()
    if not solve_knights_tour(start_x, start_y, 1, board, N, M, x_move, y_move, all_knight_moves):
        print("Solution does not exist")
        print(all_knight_moves)
        if visualize:
            print("Solution Exists, Visualizing...")
            visualize_algorithm(all_knight_moves, N, M)
    else:
        end_time = time.time()
        print_solution(board, N, M)
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.4f} seconds")
        if visualize:
            print("Solution Exists, Visualizing...")
            visualize_algorithm(all_knight_moves, N, M)
        return elapsed_time  # Return the elapsed time

# Function to print the solution board
def print_solution(board, N, M):
    """Print the solution board.

    Args:
        board (list): The final state of the board.
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
    """
    for i in range(N):
        for j in range(M):
            sys.stdout.write("{:2} ".format(board[i][j]))
        sys.stdout.write("\n")


# Function to analyze and plot running time
def analyze_knights_tour(N, M, visualize, x, y, runs=10):
    """Analyze the Knight's Tour by running multiple trials and plotting the timing results.

    Args:
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
        visualize (bool): Flag indicating whether to visualize the knight's tour.
        x (int): The x-coordinate of the starting position for increasing board size analysis.
        y (int): The y-coordinate of the starting position for increasing board size analysis.
        runs (int): The number of runs to perform (default is 10).
    """

    # ------------------------- Analysis with Different Starting Points ------------------------- #
    timings = []
    unique_starting_points = set()

    # Pick random unique starting points
    while len(timings) < runs:
        start_x = random.randint(0, N - 1)
        start_y = random.randint(0, M - 1)

        if (start_x, start_y) not in unique_starting_points:
            unique_starting_points.add((start_x, start_y))

            elapsed_time = knights_tour(N, M, visualize, start_x, start_y)
            if elapsed_time is not None:
                timings.append((elapsed_time, (start_x, start_y), N, M))

    timings.sort(key=lambda x: x[0])

    # Prepare data for plotting different starting points
    execution_times = [timing[0] for timing in timings]
    starting_points = [f"({timing[1][0]}, {timing[1][1]})" for timing in timings]

    plt.figure(figsize=(10, 5))

    # Plot with numerical indices on the x-axis
    x_indices = list(range(len(starting_points)))
    plt.scatter(x_indices, execution_times, marker='o', color='b')
    plt.plot(x_indices, execution_times, color='b', linestyle='-', alpha=0.5)  # Add lines

    # Remove annotations of starting points
    # for i, start_point in enumerate(starting_points):
    #     plt.annotate(start_point, (x_indices[i], execution_times[i]),
    #                  textcoords="offset points", xytext=(0, 5), ha='center')

    # Add labels and title
    plt.title(f'Knight\'s Tour Timing Analysis for {N}x{M} Board (Different Starting Points)')
    plt.xlabel('Starting Points (Index)')
    plt.ylabel('Time (seconds)')
    plt.xticks(x_indices, starting_points, rotation=45)
    plt.grid()
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

    # ------------------------- Analysis with Increasing Board Sizes ------------------------- #
    size_timings = []

    for size in range(1, 11):
        elapsed_time = knights_tour(size, size, visualize, x, y)
        if elapsed_time is not None:
            size_timings.append((elapsed_time, size, size))
        else:
            size_timings.append((0, size, size))  # Add a placeholder for missing data

    # Prepare data for plotting
    valid_sizes = range(1, 11)  # Ensures we plot all sizes 1 through 10
    size_execution_times = [timing[0] for timing in size_timings]
    board_sizes = [f"{timing[1]}x{timing[2]}" for timing in size_timings]

    plt.figure(figsize=(10, 5))

    # Plot with board sizes on the x-axis
    plt.plot(valid_sizes, size_execution_times, marker='o', color='g')

    # Add labels and title
    plt.title('Knight\'s Tour Timing Analysis (Same Starting Point, Increasing Board Size)')
    plt.xlabel('Board Size (NxN)')
    plt.ylabel('Time (seconds)')
    plt.xticks(valid_sizes, board_sizes)
    plt.grid()
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

    # ------------------------- Print Timings for Both Analyses ------------------------- #
    print("Timings for each run (sorted for different starting points):")
    for i, (timing, point, n, m) in enumerate(timings):
        print(f"Run {i + 1}: Time = {timing:.4f} seconds, Board Size = {n}x{m}, Starting Point = {point}")

    print("\nTimings for increasing board sizes (sorted):")
    for i, (timing, n, m) in enumerate(size_timings):
        print(f"Run {i + 1}: Time = {timing:.4f} seconds, Board Size = {n}x{m}, Starting Point = ({x}, {y})")


# Main function to handle command-line input and start the knight's tour
def main():
    """Main function to parse command-line arguments and start the Knight's Tour."""
    if len(sys.argv) < 6:
        print("Usage: python knightstour.py <rows> <cols> <start_x> <start_y> <0 for no Visualization, 1 for Visualization> <0 for single run, 1 for analysis>")
        sys.exit(1)

    N = int(sys.argv[1])
    M = int(sys.argv[2])
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    visualization = True if int(sys.argv[5]) == 1 else False
    run_mode = int(sys.argv[6])  # 0 for single run, 1 for analysis

    print("Board size: {}x{}, Starting position: ({}, {})".format(N, M, x, y))

    if run_mode == 0:
        # Single run of the Knight's Tour
        knights_tour(N, M, visualization, x, y)
    elif run_mode == 1:
        # Run the timing analysis
        analyze_knights_tour(N, M, visualization, x, y, runs=10)

    else:
        print("Invalid run mode. Use 0 for single run and 1 for analysis.")
        sys.exit(1)

if __name__ == "__main__":
    main()