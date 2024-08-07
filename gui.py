# Matthew Chandra
# CS5800 Final Project
# Visualization Program for Knight's Tour with Backtracking
# 8/5/2024

import tkinter as tk
import time
from tkinter import *
from PIL import Image, ImageTk

squareSize = 50
# example_input = [[0, 0], [1, 2], [0, 4], [2, 3], [4, 4], [3, 2], [4, 0], [2, 1], [0, 2], [1, 0], [3, 1], [4, 3], [2, 4], [0, 3], [1, 1], [3, 0], [4, 2], [3, 4], [1, 3], [0, 1], [2, 0], [4, 1], [2, 2], [1, 4], [3, 3]]

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
        self.buttonPress = 0
        self.buttons = {}
        self.all_knight_moves = all_knight_moves
        
    def populateButtons(self):
        """Populate an area on the Tkinter Window for Clickable Buttons to Start, Restart or Quit the Visualization
        """
        
        # Frame for Buttons
        buttonsArea = Frame(master=self.root, height=200, width=200, pady=25, padx=25)
        buttonsArea['bg'] = buttonsArea.master['bg']
        buttonsArea.pack(side=BOTTOM)
        
        # Next Button
        nextButton = Button(master=buttonsArea, text="Start", command=self.fillGrids,borderwidth=3, relief=RAISED, width=10, height=2, bg='SeaGreen2')
        nextButton.grid(row=0, column=0, sticky='nsew')
        self.buttons['start'] = nextButton
        
        # Restart Button
        restartButton = Button(master=buttonsArea, text="Restart", command=self.restartProgram, borderwidth=3, relief=RAISED, width=10, height=2, state=DISABLED, bg='OliveDrab1')
        restartButton.grid(row=0, column=1, sticky='nsew')
        self.buttons['restart'] = restartButton
        
        # Quit Button
        quitButton = Button(master=buttonsArea, text="Quit", command=self.quitProgram, borderwidth=3, relief=RAISED, width=10, height=2, bg='coral1')
        quitButton.grid(row=0, column=2, sticky='nsew')
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

    def fillGrids(self):  
        """Fills in the grids one at a time based on the passed in knight's move
        """
        icon = self.loadImage('knight.png')
        
        # Disable Start Button
        self.buttons['start'].config(state=DISABLED)
        prevGrid = None
        
        # Mark Knight's Move Frame by Frame
        while self.buttonPress < self.rows*self.columns:
            # Label previous move as an X on the board
            if prevGrid is not None:
                image_label.destroy()
                x_label = Label(master=self.board_status[entry[0]][entry[1]], text="X", anchor=CENTER, font=('bold'))
                x_label['bg'] = x_label.master['bg']
                x_label.pack(fill="both", expand=1)
            
            # Get the Knight's move based on the move number
            entry = self.all_knight_moves[self.buttonPress]
            image_label = Label(master=self.board_status[entry[0]][entry[1]], image=icon, anchor=CENTER)
            image_label['bg'] = image_label.master['bg']
            image_label.pack(fill="both", expand=1)
            prevGrid = [entry[0], entry[1]]
            self.buttonPress += 1
            
            # Enables Frame by Frame Visualization
            time.sleep(0.5)
            self.root.update()
    
        # Last Move to be Marked by an X before Completion
        image_label.destroy()
        x_label = Label(master=self.board_status[entry[0]][entry[1]], text="X", anchor=CENTER, font=('bold'))
        x_label['bg'] = x_label.master['bg']
        x_label.pack(fill="both", expand=1)
       
        time.sleep(0.5)
        self.root.update()
        
        # Enable Restart Button and Display Complete Message
        self.buttons['restart'].config(state=ACTIVE)
        done_label = Label(master=self.root, text="Knight's Tour Complete", pady=15)
        done_label['bg'] = done_label.master['bg']
        done_label.pack()
    
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
        self.buttonPress = 0
        self.runVisualization()
        
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
    
#     chessBoard = ChessBoard(5, 5, root, example_input)
#     chessBoard.runVisualization()
    
#     root.mainloop()

    
# if __name__ == "__main__":
#     main()