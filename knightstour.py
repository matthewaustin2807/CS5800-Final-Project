# Theresa Fu-Hsing Hsu, Matthew Chandra, Zuoyin Chen
# CS5800 Final Project
# Summer 2024
# Bruce Maxwell
# Knight's Tour problem using backtracking in Python.

import sys
import time
import tkinter as tk
import random
from matplotlib import pyplot as plt
from gui import ChessBoard, squareSize

# Function to visualize the Knight's Tour Algorithm using Tkinter
def visualize_algorithm(all_knight_moves, n, m):
    """Visualize the Knight's Tour Algorithm using Tkinter.

    Args:
        all_knight_moves (list): A list of coordinates of all of the knight's move in order from the starting position.
        n (int): Number of Rows on the Board.
        m (int): Number of Columns on the Board.
    """
    # Initialize the main Tkinter window
    root = tk.Tk()

    # Set the title of the window
    root.title("Knight's Tour Visualization")
    
    # Set the minimum size of the window based on the board dimensions and square size
    root.minsize(width=squareSize * m + 100, height=squareSize * n + 100)
    
    # Configure the background color of the window
    root.configure(background="papaya whip")

    # Create an instance of the ChessBoard class and pass the required parameters
    chessBoard = ChessBoard(n, m, root, all_knight_moves)
    
    # Run the visualization of the Knight's Tour
    chessBoard.runVisualization()

    # Start the Tkinter main loop to display the window
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
    """Count the number of valid moves from the current position."""
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

    # If no possible moves are available, return False (trigger backtracking)
    if not possible_moves:
        return False

    # Sort the possible moves by the count of subsequent valid moves (Warnsdorff's heuristic)
    possible_moves.sort()

    # Try all possible moves for the knight
    for _, next_x, next_y in possible_moves:
        board[next_x][next_y] = move_i
        all_knight_moves.append([next_x, next_y])
        if solve_knights_tour(next_x, next_y, move_i + 1, board, N, M, x_move, y_move, all_knight_moves):
            return True
        # Backtracking
        board[next_x][next_y] = -1
        all_knight_moves.append('backtrack')

    return False

# Function to initialize and solve the Knight's Tour problem
def knights_tour(N, M, visualize=False):
    """Initialize the board and start the Knight's Tour.

    Args:
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
        visualize (bool): Whether to visualize the Knight's Tour using Tkinter.
    """
    print("Starting Knight's Tour on a {}x{} board".format(N, M))

    # Initialize the board with -1
    board = [[-1 for _ in range(M)] for _ in range(N)]

    # Initial position of the knight
    start_x, start_y = 0, 0
    board[start_x][start_y] = 0
    all_knight_moves = [[start_x, start_y]]

    # All possible moves for the knight
    x_move = [2, 1, -1, -2, -2, -1, 1, 2]
    y_move = [1, 2, 2, 1, -1, -2, -2, -1]

    start_time = time.time()
    if not solve_knights_tour(start_x, start_y, 1, board, N, M, x_move, y_move, all_knight_moves):
        print("Solution does not exist")
        elapsed_time = None
    else:
        end_time = time.time()
        print_solution(board, N, M)
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.4f} seconds")
        if visualize:
            visualize_algorithm(all_knight_moves, N, M)
    
    return elapsed_time

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
            sys.stdout.write(f"{board[i][j]:2} ")
        sys.stdout.write("\n")

# Function to analyze and plot running time
def analyze_knights_tour(N, M, runs=10):
    """Analyze the Knight's Tour by running multiple trials and plotting the timing results.

    Args:
        N (int): The number of rows of the board.
        M (int): The number of columns of the board.
        runs (int): The number of runs to perform (default is 10).
    """
    # ------------------------- Analysis with Increasing Board Sizes ------------------------- #
    size_timings = []

    for size in range(1, 21):  # Range 1-21 for 20 sizes
        total_time = 0
        for _ in range(runs):
            elapsed_time = knights_tour(size, size)
            if elapsed_time is not None:
                total_time += elapsed_time
            else:
                total_time += 0

        average_time = total_time / runs  # Calculate average time for the size
        size_timings.append((average_time, size, size))

    # Prepare data for plotting
    valid_sizes = range(1, 21)  # Plot all sizes 1 through 20
    size_execution_times = [timing[0] for timing in size_timings]
    board_sizes = [f"{timing[1]}x{timing[2]}" for timing in size_timings]

    plt.figure(figsize=(12, 6))  # Adjusted figure size for better readability

    # Plot with board sizes on the x-axis
    plt.plot(valid_sizes, size_execution_times, marker='o', color='g')

    # Add labels and title
    plt.title('Knight\'s Tour Timing Analysis (Same Starting Point, Increasing Board Size)')
    plt.xlabel('Board Size (NxM)')
    plt.ylabel('Time (seconds)')
    plt.xticks(valid_sizes, board_sizes)
    plt.grid()
    plt.tight_layout()  # Adjust layout for better fit
    plt.show()

    # ------------------------- Print Timings for the Analyses ------------------------- #
    # Print timings for each size
    print("\nTimings for increasing board sizes:")
    for i, (timing, n, m) in enumerate(size_timings):
        print(f"Board Size = {n}x{m}, Average Time = {timing:.4f} seconds")

# Main function to handle command-line input and start the knight's tour
def main():
    """Main function to parse command-line arguments and start the Knight's Tour."""
    if len(sys.argv) < 4:
        print("Usage: python knightstour.py <rows> <cols> <0 for visualization, 1 for timing analysis>")
        sys.exit(1)

    N = int(sys.argv[1])
    M = int(sys.argv[2])
    mode = int(sys.argv[3])

    if mode == 0:
        # Single run of the Knight's Tour with Visualization
        knights_tour(N, M, visualize=True)
    elif mode == 1:
        # Multiple run of the Knight's Tour with Timing Analysis
        analyze_knights_tour(N, M, runs=10)
    else:
        print("Invalid mode. Use 0 for visualization and 1 for timing analysis.")
        sys.exit(1)

if __name__ == "__main__":
    main()