# Class code for the GUI
from tkinter import filedialog # used for opening/saving files
from tkinter import *
from Sudoku import *

#learn / use curry method for event handling ... otherwise lambda functions

class Board:
    def __init__(self, parent):
        # need a frame/container for the 3x3 grid of Entry widgets
        # need another frame/container for the buttons at the bottom.
        self.playingGrid = Frame(parent)
        self.playingGrid.grid(column=1, row=1, sticky=(N, W, E, S))
        self.playingGrid['borderwidth'] = 2
        self.playingGrid['relief'] = 'sunken'
        self.buttonRow = Frame(parent)
        self.buttonRow.grid(column=1, row=2)

        #--------------playingGrid initialization-------------
        '''
        The grid-index association
        0  1  2  3  4  5  6  7  8
        9  10 11 12 13 14 15 16 17
        18 19 20 21 22 23 24 25 26
        27 28 29 30 31 32 33 34 35
        36 37 38 39 40 41 42 43 44
        45 46 47 48 49 50 51 52 53
        54 55 56 57 58 59 60 61 62
        63 64 65 66 67 68 69 70 71
        72 73 74 75 76 77 78 79 80
        '''
        self.topLeft = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.topCenter = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.topRight = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.midLeft = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.midCenter = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.midRight = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.botLeft = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.botCenter = Frame(self.playingGrid, borderwidth=2, relief='ridge')
        self.botRight = Frame(self.playingGrid, borderwidth=2, relief='ridge')

        self.topLeft.grid(column=1, row=1)
        self.topCenter.grid(column=2, row=1)
        self.topRight.grid(column=3, row=1)
        self.midLeft.grid(column=1, row=2)
        self.midCenter.grid(column=2, row=2)
        self.midRight.grid(column=3, row=2)
        self.botLeft.grid(column=1, row=3)
        self.botCenter.grid(column=2, row=3)
        self.botRight.grid(column=3, row=3)

        self.entryValues = []
        for i in range(81):
            self.entryValues.append(StringVar())
        self.entryList = []
        for i in range(81):
            r = i % 9
            if i < 27:
                if r == 0 or r == 1 or r == 2:
                    print(str(i) + '\t' + str(len(self.entryValues)))
                    self.entryList.append(Entry(self.topLeft, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 3 or r == 4 or r == 5:
                    self.entryList.append(Entry(self.topCenter, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 6 or r == 7 or r == 8:
                    self.entryList.append(Entry(self.topRight, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
            elif i < 54:
                if r == 0 or r == 1 or r == 2:
                    self.entryList.append(Entry(self.midLeft, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 3 or r == 4 or r == 5:
                    self.entryList.append(Entry(self.midCenter, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 6 or r == 7 or r == 8:
                    self.entryList.append(Entry(self.midRight, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
            else:
                if r == 0 or r == 1 or r == 2:
                    self.entryList.append(Entry(self.botLeft, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 3 or r == 4 or r == 5:
                    self.entryList.append(Entry(self.botCenter, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))
                if r == 6 or r == 7 or r == 8:
                    self.entryList.append(Entry(self.botRight, width=3, textvariable=self.entryValues[i]))
                    self.entryList[i].grid(column=(r+1), row=((i // 9) + 1))


        #--------------buttonRow initialization---------------
        self.loadGame = Button(self.buttonRow, text='load', command=self.openPuzzle)
        self.saveGame = Button(self.buttonRow, text='save')
        self.checkGame = Button(self.buttonRow, text='check', command=self.check)

        self.loadGame.grid(column=1, row=1)
        self.saveGame.grid(column=2, row=1)
        self.checkGame.grid(column=3, row=1)

        #--------------initializing the puzzle----------------
        self.puzzle = Sudoku()
        self.updateGrid()

    def updateGrid(self):
        currentList = self.puzzle.getList()
        for i in range(81):
            if currentList[i]==0:
                self.entryValues[i].set('')
            else:
                self.entryValues[i].set(currentList[i])

    def openPuzzle(self):
        fileName = filedialog.askopenfilename(initialdir = ".",title = "Choose puzzle",filetypes = (("json files","*.json"),("all files","*.*")))
        self.puzzle.importList(fileName)
        self.updateGrid()

    def savePuzzle(self):
        pass

    def check(self):
        print(self.puzzle.checkSolution())
