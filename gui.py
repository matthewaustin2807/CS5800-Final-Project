# Matthew Chandra, Theresa Fu-Hsing Hsu
# CS5800 Final Project
# Summer 2024
# Bruce Maxwell
# Visualization Program for Knight's Tour with Backtracking

import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk

squareSize = 50  # Size of each square on the chessboard

# Example inputs for testing the GUI (these would typically come from the main algorithm)
example_input = [[0, 0], [1, 2], [0, 4], [2, 3], [4, 4], [3, 2], [4, 0], [2, 1], [0, 2], [1, 0], [3, 1], [4, 3], [2, 4], [0, 3], [1, 1], [3, 0], [4, 2], [3, 4], [1, 3], [0, 1], [2, 0], [4, 1], [2, 2], [1, 4], [3, 3]]
example_no_sol_input = [[0, 0], [1, 2], [2, 0], [0, 1], [2, 2], [1, 0], [0, 2], [2, 1], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [2, 1], [0, 2], [1, 0], [2, 2], [0, 1], [2, 0], [1, 2], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack']
example_input_2 = [[2, 2], [0, 1], [1, 3], [3, 4], [5, 3], [7, 4], [6, 2], [7, 0], [5, 1], [3, 0], [1, 1], [0, 3], [2, 4], [4, 3], [6, 4], [7, 2], [6, 0], [4, 1], [2, 0], [3, 2], [4, 0], [6, 1], [7, 3], [5, 4], [3, 3], [1, 4], [0, 2], [1, 0], [3, 1], [1, 2], [0, 0], [2, 1], [4, 2], [5, 0], [7, 1], [5, 2], [4, 4], [6, 3], 'backtrack', [2, 3], [0, 4], 'backtrack', 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 4], [5, 2], 'backtrack', [2, 3], [0, 4], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [2, 3], [0, 4], 'backtrack', [4, 4], [5, 2], [7, 1], [5, 0], 'backtrack', [6, 3], 'backtrack', 'backtrack', 'backtrack', [6, 3], [7, 1], [5, 0], 'backtrack', [5, 2], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 4], [2, 3], [0, 4], 'backtrack', 'backtrack', [5, 2], [7, 1], [5, 0], 'backtrack', 'backtrack', 'backtrack', 'backtrack', [7, 1], [5, 0], 'backtrack', [5, 2], [4, 4], [2, 3], [0, 4], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [0, 4], [2, 3], [4, 4], [5, 2], [7, 1], [5, 0], [4, 2], [6, 3], 'backtrack', [2, 1], [0, 0], 'backtrack', 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 2], [5, 0], 'backtrack', [2, 1], [0, 0], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 2], [2, 1], [0, 0], 'backtrack', 'backtrack', [5, 0], [7, 1], [5, 2], 'backtrack', 'backtrack', 'backtrack', 'backtrack', [7, 1], [5, 2], 'backtrack', [5, 0], [4, 2], [2, 1], [0, 0], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [4, 2], [2, 1], [0, 0], 'backtrack', 'backtrack', [5, 0], [7, 1], [5, 2], [4, 4], [6, 3], 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 4], [5, 2], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [6, 3], [4, 4], [5, 2], [7, 1], [5, 0], 'backtrack', 'backtrack', 'backtrack', 'backtrack', [7, 1], [5, 0], 'backtrack', [5, 2], [4, 4], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [5, 0], [7, 1], [5, 2], [4, 4], [6, 3], [4, 2], [2, 1], [0, 0], [1, 2], [0, 4], [2, 3]]



class ChessBoard:
    """ChessBoard class to create and manage the chessboard visualization for the Knight's Tour."""

    def __init__(self, rows, columns, root, all_knight_moves):
        """
        Initialize the ChessBoard Graphic Object.

        Args:
            rows (int): Number of Rows on the Board.
            columns (int): Number of Columns on the Board.
            root (Tk): Tkinter Root Window.
            all_knight_moves (list): A list of coordinates of all of the knight's moves in order from the starting position.
        """
        self.rows = rows
        self.columns = columns
        self.root = root
        self.board_childrens = {}
        self.board_state = [[{} for _ in range(self.columns)] for _ in range(self.rows)]
        self.backtrackStatus = []
        self.moveStack = []
        self.buttons = {}
        self.all_knight_moves = all_knight_moves
        self.prevGrid = None
        self.icon = self.loadImage('knight.png')
        self.image_label = None
        self.paused = False
        self.iter = -1
        self.backtrackIter = 0
        self.backtrackStart = 0
    
    def setupMoves(self):
        """Set the series of moves to be made by the visualization program
        """
        i = 0
        numBacktrack = 0
        lastNonBacktrackIndex = 0
        while i < len(self.all_knight_moves): 
            knight_move = self.all_knight_moves[i]
            if knight_move != 'backtrack':
                numBacktrack = 0
                self.moveStack.append(knight_move + [i])
                lastNonBacktrackIndex = i
                self.backtrackStatus.append(False)
            else:
                numBacktrack += 1
                move = self.moveStack[lastNonBacktrackIndex-numBacktrack]
                self.moveStack.append([move[0], move[1], move[2]])
                self.backtrackStatus.append(True)
            i += 1    
       
    def populateButtons(self):
        """Create and add control buttons to the Tkinter window."""
        
        # Frame for holding buttons at the bottom of the window
        buttonsArea = Frame(master=self.root, height=200, width=200, pady=25, padx=25)
        buttonsArea['bg'] = buttonsArea.master['bg']
        buttonsArea.pack(side=BOTTOM)
        
        # Start/Play button
        startButton = Button(master=buttonsArea, text="Play", command=self.play, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        startButton.grid(row=0, column=0, sticky='nsew')
        self.buttons['play'] = startButton
        
        # Next move button
        nextButton = Button(master=buttonsArea, text="Next", command=self.nextMove, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        nextButton.grid(row=0, column=1, sticky='nsew')
        self.buttons['next'] = nextButton
        
        # Previous move button
        prevButton = Button(master=buttonsArea, text="Previous", command=self.prevMove, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3', state=DISABLED)
        prevButton.grid(row=0, column=2, sticky='nsew')
        self.buttons['prev'] = prevButton
        
        # Pause button
        pauseButton = Button(master=buttonsArea, text="Pause", command=self.pause, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3', state=DISABLED)
        pauseButton.grid(row=0, column=3, sticky='nsew')
        self.buttons['pause'] = pauseButton
        
        # Restart button
        restartButton = Button(master=buttonsArea, text="Restart", command=self.restartProgram, borderwidth=3, relief=RAISED, width=10, height=2, state=DISABLED, bg='seashell3')
        restartButton.grid(row=0, column=4, sticky='nsew')
        self.buttons['restart'] = restartButton
        
        # Quit button to close the program
        quitButton = Button(master=buttonsArea, text="Quit", command=self.quitProgram, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        quitButton.grid(row=0, column=5, sticky='nsew')
        self.buttons['quit'] = quitButton
            
    def populateGrids(self):
        """Create the grid layout for the chessboard."""
        # Define alternating colors for the chessboard squares
        def boardColor(i, j):
            if i % 2 == 0:
                return 'bisque4' if j % 2 == 0 else 'bisque2'
            else:
                return 'bisque2' if j % 2 == 0 else 'bisque4'
            
       # Main title of the visualization
        title = Label(master=self.root, pady=15, text=f"Knight's Tour Visualization on a {self.rows}x{self.columns} board starting at ({self.all_knight_moves[0][0]}, {self.all_knight_moves[0][1]})", font=('bold'), padx=15)
        title['bg'] = title.master['bg']
        title.pack(side=TOP)
        
        # Frame to hold the chessboard grid
        board = Frame(self.root, height=squareSize * self.rows, width=squareSize * self.columns, pady=15)
        board['bg'] = board.master['bg']
        board.pack()
        
        # Create and position each square of the chessboard
        for i in range(self.rows):
            for j in range(self.columns):
                frame = tk.Frame(
                    master=board,
                    relief=tk.RAISED,
                    borderwidth=1,
                    width=squareSize,
                    height=squareSize,
                    bg=boardColor(i, j)
                )
                # Prevent Frame Auto Resizing
                frame.pack_propagate(False)
                frame.grid(row=i, column=j, sticky='nsew') 
                self.board_state[i][j]['frame'] = frame

    def fillKnight(self, n, m):       
        """Place a knight image on a specific square.

        Args:
            move (list): Coordinates [x, y] where the knight should be displayed.
        """
        self.board_state[n][m]['knight_icon'] = Label(master=self.board_state[n][m]['frame'], image=self.icon, anchor=CENTER) 
        self.board_state[n][m]['knight_icon']['bg'] = self.board_state[n][m]['knight_icon'].master['bg']
        self.board_state[n][m]['knight_icon'].image = self.icon
        self.board_state[n][m]['knight_icon'].pack(fill="both", expand=1)
    
    def fillMoveNumber(self, n, m, moveNumber):
        """Display the move number at a specific square.

        Args:
            move (list): Coordinates [x, y] where the move number should be displayed.
        """
        # Remove the knight icon and replace it with the move number
        self.board_state[n][m]['knight_icon'].destroy()
        self.board_state[n][m]['moveNumber_icon'] = Label(master=self.board_state[n][m]['frame'], text=f'{moveNumber}', anchor=CENTER, font=('bold'))
        self.board_state[n][m]['moveNumber_icon']['bg'] = self.board_state[n][m]['moveNumber_icon'].master['bg']
        self.board_state[n][m]['moveNumber_icon'].pack(fill="both", expand=1)
            
    def nextMove(self):       
        """Move the Knight on the ChessBoard to the next Position."""
        if self.iter == len(self.moveStack)-1:
            # If this is the last move, display the end message
            self.iter += 1
            
            # If the lastmove in the set of moves is backtrack, then no solution is found
            if self.backtrackStatus[-1]:
                self.board_state[self.all_knight_moves[0][0]][self.all_knight_moves[0][1]]['moveNumber_icon'].destroy()
                self.displayBacktrackingMessage(display=False)
                self.displayEndMessage(solution=False, display=True)
            
            # Otherwise solution is found
            else:
                self.fillMoveNumber(self.moveStack[-1][0], self.moveStack[-1][1], self.moveStack[-1][2])
                self.displayEndMessage(solution=True, display=True)
            return
        
        self.iter += 1
            
        # If there was a previous move, mark that square with the move number
        if self.prevGrid is not None:
            self.fillMoveNumber(self.prevGrid[0], self.prevGrid[1], self.prevGrid[2])
        
        # Enable the Previous and Restart buttons
        self.buttons['prev']['state'] = ACTIVE
        self.buttons['restart']['state'] = ACTIVE 
        
        # Get the move for the current iteration
        move = self.moveStack[self.iter]
        
        # If the current move is a backtrack
        if self.backtrackStatus[self.iter]:
            # display backtracking message
            self.displayBacktrackingMessage(display=True)
            
            # remove all widgets from the grid we are backtracking to
            self.board_state[self.prevGrid[0]][self.prevGrid[1]]['knight_icon'].destroy()
            self.board_state[self.prevGrid[0]][self.prevGrid[1]]['moveNumber_icon'].destroy()
            self.board_state[move[0]][move[1]]['moveNumber_icon'].destroy()
        else:
            # if not, remove backtracking message
            self.displayBacktrackingMessage(False)   
        
        # fill in the knight at the correct grid and destroy any existing widgets on that square
        if 'knight_icon' in self.board_state[move[0]][move[1]]:
            self.board_state[move[0]][move[1]]['knight_icon'].destroy()
        if 'moveNumber_icon' in self.board_state[move[0]][move[1]]:
            self.board_state[move[0]][move[1]]['moveNumber_icon'].destroy()
        self.fillKnight(move[0], move[1])
        
        # Set the prevGrid to the current move
        self.prevGrid = move           
                   
    def prevMove(self):
        """Move to the previous move in the sequence."""
        if self.iter == 1:
            # Disable the Previous button if the knight is at the starting position
            self.buttons['prev']['state'] = DISABLED
        elif self.iter == len(self.moveStack):
            # Allow further moves if we were at the last move
            self.displayEndMessage(False)
        
        # Get the current move before hitting previous button
        currentMove = self.moveStack[self.iter]
        
        # Destroy knight icon on the current square
        self.board_state[currentMove[0]][currentMove[1]]['knight_icon'].destroy()
        
        # If the current move is a backtracking move, display backtracking message and restore the move number
        if self.backtrackStatus[self.iter]:
            self.displayBacktrackingMessage(display=True)
            self.fillMoveNumber(currentMove[0], currentMove[1], currentMove[2])
        # Else, remove backtracking message
        else:
            self.displayBacktrackingMessage(display=False)
        
        # Decrement iter count
        self.iter -= 1
        
        # Get the previous move
        prevMove = self.moveStack[self.iter]
            
        # Destroy knight and move number icon from the previous square indicated by the previous move
        self.board_state[prevMove[0]][prevMove[1]]['knight_icon'].destroy()
        self.board_state[prevMove[0]][prevMove[1]]['moveNumber_icon'].destroy()
        
        # Add the knight icon to the previous square
        self.fillKnight(prevMove[0], prevMove[1])
        
        # Set the previous grid as the previous move
        self.prevGrid = prevMove
    
    def play(self):  
        """Automatically move the knight across the chessboard according to the moves from the algorithm."""
        self.buttons['play']['state'] = DISABLED
        self.buttons['restart']['state'] = DISABLED
        self.buttons['pause']['state'] = ACTIVE
        self.paused = False
        
        while self.iter < len(self.all_knight_moves) and not self.paused:
            self.nextMove()        
            # Enables Frame by Frame Visualization
            time.sleep(0.2)
            self.root.update()
            
    def displayEndMessage(self, solution, display):
        """Display the message indicating whether the Knight's Tour is complete or no solution was found."""
        if display:
            self.done = True
            self.board_childrens['done_label'] = Label(master=self.root, text="Knight's Tour Complete" if solution else "No Solution Found", pady=15)
            self.board_childrens['done_label']['bg'] = self.board_childrens['done_label'].master['bg']           
            # Disable buttons
            self.buttons['next']['state'] = DISABLED
            self.buttons['pause']['state'] = DISABLED
            self.buttons['prev']['state'] = DISABLED            
            # Display done label
            self.board_childrens['done_label'].pack()
        
        else:
            # Activate next button
            self.buttons['next']['state'] = ACTIVE
            self.buttons['play']['state'] = ACTIVE
            # Remove done label
            self.board_childrens['done_label'].destroy()
            
    def displayBacktrackingMessage(self, display):
        """Display a backtracking message on the frame when the algorithm backtracks."""
        if display:
            if 'backtrackingMessage' not in self.board_childrens:       
                self.board_childrens['backtrackingMessage'] = Label(master=self.root, text="Backtracking...", anchor=CENTER)
                self.board_childrens['backtrackingMessage']['bg'] = self.board_childrens['backtrackingMessage'].master['bg']
                self.board_childrens['backtrackingMessage'].pack()
        else:
            if 'backtrackingMessage' in self.board_childrens:
                self.board_childrens['backtrackingMessage'].destroy()
                del self.board_childrens['backtrackingMessage']
     
    def pause(self):
        """Pause the visualization."""
        self.paused = True
        self.buttons['play']['state'] = ACTIVE
        self.buttons['pause']['state'] = DISABLED  
                
    def quitProgram(self):
        """Exit the visualization program."""
        self.root.quit()
    
    def restartProgram(self):
        """Restart the visualization from the beginning."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.buttons.clear()
        self.iter = -1
        self.prevGrid = None
        self.paused = True
        self.done = False
        self.moveStack = []
        self.runVisualization()
      
    def loadImage(self, filename):
        """Load a PNG image to be used in the GUI.

        Args:
            filename (string): Path to the PNG file.

        Returns:
            ImageTk.PhotoImage: The PNG image as a PhotoImage object that is usable by Tkinter.
        """
        image = Image.open(filename)
        image = image.resize((25, 25), Image.NEAREST)
        return ImageTk.PhotoImage(image)
      
    def runVisualization(self):
        """Run the Visualization Program by setting up the grid and buttons."""
        self.populateGrids()
        self.populateButtons()
        self.setupMoves()
    
# Test Method
def main():
    """Main function to run a test visualization with example inputs."""
    root = tk.Tk()
    root.title("Knight's Tour Visualization")
    root.minsize(width=400, height=400)
    root.configure(background="papaya whip")
    chessBoard = ChessBoard(8, 5, root, example_input_2)
    chessBoard.runVisualization()
    
    root.mainloop()

if __name__ == "__main__":
    main()