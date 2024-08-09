# Matthew Chandra
# CS5800 Final Project
# Visualization Program for Knight's Tour with Backtracking
# 8/5/2024

import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk

squareSize = 50
example_input = [[0, 0], [1, 2], [0, 4], [2, 3], [4, 4], [3, 2], [4, 0], [2, 1], [0, 2], [1, 0], [3, 1], [4, 3], [2, 4], [0, 3], [1, 1], [3, 0], [4, 2], [3, 4], [1, 3], [0, 1], [2, 0], [4, 1], [2, 2], [1, 4], [3, 3]]
example_no_sol_input = [[0, 0], [1, 2], [2, 0], [0, 1], [2, 2], [1, 0], [0, 2], [2, 1], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', [2, 1], [0, 2], [1, 0], [2, 2], [0, 1], [2, 0], [1, 2], 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack', 'backtrack']

class ChessBoard():
    """ChessBoard class which will generate a chess board of a given size and start the Knight's Tour visualization
    """
    
    # Individual Chess Board Square Size
    squareSize = squareSize
    
    def __init__(self, rows, columns, root, all_knight_moves):
        """Initialize the ChessBoard Graphic Object

        Args:
            rows (int): Number of Rows on the Board
            columns (int): Number of Columns on the Board
            root (int): Tkinter Root Window
            all_knight_moves (list): A list of coordinates of all of the knight's move in order from the starting position
        """
        self.rows = rows
        self.columns = columns
        self.root = root
        self.board_status = [[0 for _ in range(self.columns)] for _ in range(self.rows)] 
        self.board_childrens = {}
        self.board_state = [[{} for _ in range(self.columns)] for _ in range(self.rows)]
        self.moveStack = []
        self.buttons = {}
        self.all_knight_moves = all_knight_moves
        self.prevGrid = None
        self.icon = self.loadImage('knight.png')
        self.image_label = None
        self.paused = False
        self.iter = -1
        
    def populateButtons(self):
        """Populate an area on the Tkinter Window for Clickable Buttons to Start, Restart or Quit the Visualization
        """
        
        # Frame for Buttons
        buttonsArea = Frame(master=self.root, height=200, width=200, pady=25, padx=25)
        buttonsArea['bg'] = buttonsArea.master['bg']
        buttonsArea.pack(side=BOTTOM)
        
        # Start Button
        startButton = Button(master=buttonsArea, text="Play", command=self.play,borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        startButton.grid(row=0, column=0, sticky='nsew')
        self.buttons['play'] = startButton
        
        # Next Button
        nextButton = Button(master=buttonsArea, text="Next", command=self.nextMove, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        nextButton.grid(row=0, column=1, sticky='nsew')
        self.buttons['next'] = nextButton
        
        # Previous Button
        prevButton = Button(master=buttonsArea, text="Previous", command=self.prevMove, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3', state=DISABLED)
        prevButton.grid(row=0, column=2, sticky='nsew')
        self.buttons['prev'] = prevButton
        
        # Pause Button
        pauseButton = Button(master=buttonsArea, text="Pause", command=self.pause, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3', state=DISABLED)
        pauseButton.grid(row=0, column=3, sticky='nsew')
        self.buttons['pause'] = pauseButton
        
        # Restart Button
        restartButton = Button(master=buttonsArea, text="Restart", command=self.restartProgram, borderwidth=3, relief=RAISED, width=10, height=2, state=DISABLED, bg='seashell3')
        restartButton.grid(row=0, column=4, sticky='nsew')
        self.buttons['restart'] = restartButton
        
        # Quit Button
        quitButton = Button(master=buttonsArea, text="Quit", command=self.quitProgram, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
        quitButton.grid(row=0, column=5, sticky='nsew')
        self.buttons['quit'] = quitButton
            
    def populateGrids(self):
        """Populate the ChessBoard with the correct number of Squares based on the passed in Rows and Columns
        """
        # Chess Board Colors
        def boardColor(i, j):
            if i % 2 == 0:
                if j % 2 == 0:
                    return 'bisque4'
                else:
                    return 'bisque2'
            else:
                if j % 2 == 0:
                    return 'bisque2'
                else:
                    return 'bisque4'

        # Main Title
        title = Label(master=self.root, pady=15, text=f"Knight's Tour Visualization on a {self.rows}x{self.columns} board starting at ({self.all_knight_moves[0][0]}, {self.all_knight_moves[0][1]})", font=('bold'),
                      padx=15)
        title['bg'] = title.master['bg']
        title.pack(side=TOP)
        
        # Board Frame to hold the Squares
        board = Frame(self.root, height=self.squareSize * self.rows, width=self.squareSize*self.columns, pady=15)
        board['bg'] = board.master['bg']
        board.pack()
        
        # Initialize each square and store them in a 2D array for storage.
        for i in range(self.rows):
            for j in range(self.columns):
                frame = tk.Frame(
                    master=board,
                    relief=tk.RAISED,
                    borderwidth=1,
                    width=self.squareSize,
                    height=self.squareSize,
                    bg=boardColor(i, j)
                )
                # Prevent Frame Auto Resizing
                frame.pack_propagate(False)
                
                frame.grid(row=i, column=j, sticky='nsew') 
                self.board_status[i][j] = frame

    def fillKnight(self, move):       
        """Fill a knight at a specific square

        Args:
            move ([x, y]): the square at which the knight should be displayed at
        """
        self.board_state[move[0]][move[1]]['knight_icon'] = Label(master = self.board_status[move[0]][move[1]], image=self.icon, anchor=CENTER) 
        self.board_state[move[0]][move[1]]['knight_icon']['bg'] = self.board_state[move[0]][move[1]]['knight_icon'].master['bg']
        self.board_state[move[0]][move[1]]['knight_icon'].image = self.icon
        self.board_state[move[0]][move[1]]['knight_icon'].pack(fill="both", expand=1)
    
    def fillMoveNumber(self, move):
        """Fill a move number at a specific square

        Args:
            move ([x, y]): the square at which the move number should be displayed at
        """
        self.board_state[move[0]][move[1]]['knight_icon'].destroy()
        self.board_state[move[0]][move[1]]['moveNumber_icon'] = Label(master=self.board_status[move[0]][move[1]], text=f'{self.iter-1}', anchor=CENTER, font=('bold'))
        self.board_state[move[0]][move[1]]['moveNumber_icon']['bg'] = self.board_state[move[0]][move[1]]['moveNumber_icon'].master['bg']
        self.board_state[move[0]][move[1]]['moveNumber_icon'].pack(fill="both", expand=1)
            
    def nextMove(self):        
        """Move the Knight on the ChessBoard to the next Position
        """
        
        # If the current iteration is the last in the set of moves, display end message
        if self.iter == len(self.all_knight_moves)-1:
            self.iter += 1
            lastMove = self.all_knight_moves[len(self.all_knight_moves) - 1]
            
            # If the lastmove in the set of moves is backtrack, then no solution is found
            if lastMove == 'backtrack':
                self.displayBacktrackingMessage(display=False)
                self.displayEndMessage(solution=False, display=True)
            # Otherwise solution is found
            else:
                self.fillMoveNumber(lastMove)
                self.displayEndMessage(solution=True, display=True)
            return

        self.iter += 1
        
        # If there is a previous square, fill that square with the move number
        if self.prevGrid is not None:
            self.fillMoveNumber(self.prevGrid)
        
        # Set buttons
        self.buttons['prev']['state'] = ACTIVE
        self.buttons['restart']['state'] = ACTIVE 
        
        # Get the move for the current iteration
        move = self.all_knight_moves[self.iter]
        
        # If the move is backtrack, then backtrack until we exit the backtracking sequence
        if move == 'backtrack':
            self.displayBacktrackingMessage(True)
            self.board_state[self.prevGrid[0]][self.prevGrid[1]]['knight_icon'].destroy()
            self.board_state[self.prevGrid[0]][self.prevGrid[1]]['moveNumber_icon'].destroy()
            self.moveStack.pop(len(self.moveStack) - 1)
            move = self.moveStack[-1]
            self.board_state[move[0]][move[1]]['moveNumber_icon'].destroy()
            self.fillKnight(move)
        # If a normal move is found, move the knight accordingly
        else:
            self.displayBacktrackingMessage(False)
            self.backtracking = False
            self.moveStack.append(move)
            self.fillKnight(self.moveStack[-1])
        
        # Set the previous square as the current move
        self.prevGrid = move        
                   
    def prevMove(self):
        """Move to the previous move
        """
        # If we are the second element, the next press will move the knight to the original starting position. Disable prev button in this case
        if self.iter == 1:
            self.buttons['prev']['state'] = DISABLED
        # If we are at the last element, pressing the prev button will remove the done label and reactive next button
        elif self.iter == len(self.all_knight_moves):
            self.displayEndMessage(False)
        
        # Decrement button press
        self.iter -= 1
        
        # Delete the widgets from the current square
        currentMove = self.moveStack[len(self.moveStack) - 1]
        for widget in self.board_state[currentMove[0]][currentMove[1]]:
            self.board_state[currentMove[0]][currentMove[1]][widget].destroy()
        
        # Pop the move stack and get the previous move
        self.moveStack.pop(len(self.moveStack) - 1)
        prevMove = self.moveStack[len(self.moveStack) - 1]
        
        # Delete widgets from the previous square
        for widget in self.board_state[prevMove[0]][prevMove[1]]:
            self.board_state[prevMove[0]][prevMove[1]][widget].destroy()
        
        # Move the knight to the previous square
        self.fillKnight(prevMove)
        self.prevGrid = self.all_knight_moves[self.iter]
       
    def play(self):  
        """Automatically moves the knights across the chessboard according to the moves from the algorithm.
        """
        # Disable Start Button, Enable Pause Button, and set Paused to False
        self.buttons['play']['state'] = DISABLED
        self.buttons['restart']['state'] = DISABLED
        self.buttons['pause']['state'] = ACTIVE
        self.paused = False
        
        # Mark Knight's Move Frame by Frame
        while self.iter < len(self.all_knight_moves):
            # If paused button is pressed, stop
            if self.paused:
                return
            self.nextMove()        
            # Enables Frame by Frame Visualization
            time.sleep(0.2)
            self.root.update()
            
    def displayEndMessage(self, solution, display):
        """State that the algorithm finished running and disable pause and next buttons
        """
        if display:
            # Add done label
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
        """Display Backtracking Message on the Frame

        Args:
            display (bool): Whether to display the message or not
        """
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
        """Callback function to pause visualization
        """
        self.paused = True
        self.buttons['play']['state'] = ACTIVE
        self.buttons['pause']['state']= DISABLED  
                
    def quitProgram(self):
        """Quits the Visualization Program
        """
        self.root.destroy()
    
    def restartProgram(self):
        """Restarts the Visualization
        """
        for widget in self.root.winfo_children():
            widget.destroy()
        self.buttons.clear()
        self.iter = -1
        self.prevGrid = None
        self.paused = True
        self.runVisualization()
      
    def loadImage(self, filename):
        """Loads a PNG image to be used in the GUI

        Args:
            filename (string): path to the png file

        Returns:
            ImageTk PhotoImage: The PNG image as a PhotoImage object that is usable by Tkinter
        """
        image = Image.open(filename)
        image = image.resize((25, 25), Image.NEAREST)
        return ImageTk.PhotoImage(image)
      
    def runVisualization(self):
        """Runs the Visualization Program
        """
        self.populateGrids()
        self.populateButtons()
    
# Test Method
# def main():
#     root = tk.Tk()
#     root.title("Knight's Tour Visualization")
#     root.minsize(width=400, height=400)
#     root.configure(background="papaya whip")
    
#     chessBoard = ChessBoard(3, 3, root, example_no_sol_input)
#     chessBoard.runVisualization()
    
#     root.mainloop()

    
# if __name__ == "__main__":
#     main()