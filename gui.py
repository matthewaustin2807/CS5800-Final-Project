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
        self.buttonPress = -1
        self.buttons = {}
        self.all_knight_moves = all_knight_moves
        self.prevGrid = None
        self.icon = self.loadImage('knight.png')
        self.image_label = None
        self.paused = False
    
    def pause(self):
        """Callback function to pause visualization
        """
        self.paused = True
        self.buttons['play']['state'] = ACTIVE
        self.buttons['pause']['state']= DISABLED
        
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
        prevButton = Button(master=buttonsArea, text="Previous", command=self.prevMove, borderwidth=3, relief=RAISED, width=10, height=2, bg='seashell3')
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
                   
    def prevMove(self):
        """Move to the previous move
        """
        # If we are the second element, the next press will move the knight to the original starting position. Disable prev button in this case
        if self.buttonPress == 1:
            self.buttons['prev']['state'] = DISABLED
        # If we are at the last element, pressing the prev button will remove the done label and reactive next button
        elif self.buttonPress == len(self.all_knight_moves):
            self.displayEndMessage(False)
        
        # Decrement button press
        self.buttonPress -= 1

        # Get the previous move and remove all widgets from the current square
        previousKnightMove = self.all_knight_moves[self.buttonPress]
        self.image_label.destroy()
        for widget in self.board_status[previousKnightMove[0]][previousKnightMove[1]].winfo_children():
            widget.destroy()
        
        # Set the Knight to the previous visited square
        self.image_label = Label(master=self.board_status[previousKnightMove[0]][previousKnightMove[1]], image=self.icon, anchor=CENTER)
        self.image_label['bg'] = self.image_label.master['bg']
        self.image_label.image = self.icon
        self.image_label.pack(fill="both", expand=1)
        
        # Set the previous grid as the previous move.
        
        self.prevGrid = self.all_knight_moves[self.buttonPress]
        
    def nextMove(self):        
        """Move the Knight on the ChessBoard to the next Position
        """
        # If the number of button press equals the total moves, finish algorithm.
        if self.buttonPress == len(self.all_knight_moves)-1: 
            self.image_label.destroy()
            x_label = Label(master=self.board_status[self.prevGrid[0]][self.prevGrid[1]], text=f'{self.buttonPress}', anchor=CENTER, font=('bold'))
            x_label['bg'] = x_label.master['bg']
            x_label.pack(fill="both", expand=1)
            self.displayEndMessage(True)
            self.buttonPress += 1
            return
        
        # Increment buttonpress 
        self.buttonPress += 1
        
        self.buttons['prev']['state'] = ACTIVE
        self.buttons['restart']['state'] = ACTIVE 
        
        # Mark the previously visited square with the move number
        if self.prevGrid is not None:
                self.image_label.destroy()
                x_label = Label(master=self.board_status[self.prevGrid[0]][self.prevGrid[1]], text=f'{self.buttonPress - 1}', anchor=CENTER, font=('bold'))
                x_label['bg'] = x_label.master['bg']
                x_label.pack(fill="both", expand=1)
         
        # Get the move from the move list
        move = self.all_knight_moves[self.buttonPress]
        
        # Set the Knight on the correct square on the board
        self.image_label = Label(master=self.board_status[move[0]][move[1]], image=self.icon, anchor=CENTER)
        self.image_label['bg'] = self.image_label.master['bg']
        self.image_label.image = self.icon
        self.image_label.pack(fill="both", expand=1)
        
        # Set the current visited grid as the previous grid
        self.prevGrid = move
        
    def displayEndMessage(self, active):
        """State that the algorithm finished running and disable pause and next buttons
        """
        if active:
            # Add done label
            self.board_childrens['done_label'] = Label(master=self.root, text="Knight's Tour Complete", pady=15)
            self.board_childrens['done_label']['bg'] = self.board_childrens['done_label'].master['bg']
            
            # Disable buttons
            self.buttons['next']['state'] = DISABLED
            self.buttons['pause']['state'] = DISABLED
            
            # Display done label
            self.board_childrens['done_label'].pack()
        else:
            # Activate next button
            self.buttons['next']['state'] = ACTIVE
            self.buttons['play']['state'] = ACTIVE
            # Remove done label
            self.board_childrens['done_label'].destroy()
            
        
    def play(self):  
        """Automatically moves the knights across the chessboard according to the moves from the algorithm.
        """
        # Disable Start Button, Enable Pause Button, and set Paused to False
        self.buttons['play']['state'] = DISABLED
        self.buttons['restart']['state'] = DISABLED
        self.buttons['pause']['state'] = ACTIVE
        self.paused = False
        
        # Mark Knight's Move Frame by Frame
        while self.buttonPress < len(self.all_knight_moves):
            # If paused button is pressed, stop
            if self.paused:
                return
            self.nextMove()        
            # Enables Frame by Frame Visualization
            time.sleep(0.5)
            self.root.update()
    
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
        self.buttonPress = -1
        self.prevGrid = None
        self.paused = True
        self.runVisualization()
        
    def runVisualization(self):
        """Runs the Visualization Program
        """
        self.populateGrids()
        self.populateButtons()
    
# Test Method
def main():
    root = tk.Tk()
    root.title("Knight's Tour Visualization")
    root.minsize(width=400, height=400)
    root.configure(background="papaya whip")
    
    chessBoard = ChessBoard(5, 5, root, example_input)
    chessBoard.runVisualization()
    
    root.mainloop()

    
if __name__ == "__main__":
    main()