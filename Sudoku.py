# Class code for the sudoku game logic.
import json

class Sudoku:
    def __init__(self):
        self.gameList = [0] * 81
        self.editable = [not x for x in self.gameList]

    def importList(self, puzzleFile):
        with open(puzzleFile, 'r') as f:
            self.puzzleJSON = json.load(f)
        self.gameList = self.puzzleJSON['puzzleValues']
        self.editable = self.puzzleJSON['editableValues']

    def exportList(self, saveFile):
        # Need to figure out the structure of the JSON for both read/write.
        # Currently only supports read only
        puzzleDict = {}
        puzzleDict['puzzleValues'] = self.gameList
        puzzleDict['editablevalues'] = self.editable
        with open(saveFile, 'w') as f:
            json.dump(puzzleDict, f)


    # If reference is given, assuming valid number(s) given.
    def setNumber(self, value, num1=None, num2=None):
        # If both num1 and num2 are used when this is called,
        #       assume they refer to row and column respectively.
        # If only one number is passed then assume it is an index (from 0 to 80)
        # If no numbers are passed then abort the change. (print error message)
        if (num1 is None and num2 is None):
            print('Please pass in a reference to where the value ' + value + ' should go.')
            print('Acceptable formats:')
            print('\tsetValue(value, row, column)')
            print('\tsetValue(value, index)')
        if (num1 is not None and num2 is not None):
            #row/column
            index = self.__rowColumnToIndex(num1, num2)
            self.__setNumberHelper(value, index)
        else:
            if (num2 is not None):
                num1 = num2
            self.__setNumberHelper(value, num1)

    def __setNumberHelper(self, value, index):
        if (self.editable[index] == True):
            self.gameList[index] = value
        else:
            print('Cannot edit this value, part of puzzle definition')

    # output can equal 'String', 'List', or 'Matrix', default to 'List'
    # list can equal 'Game' or 'Edit'
    def getList(self, output=None, list=None):
        if list is None:
            list = 'Game'
        if list not in ['Game', 'Edit']:
            print("Parameter 'list': " + list + " not valid. Please choose either 'Game' or 'Edit'.")
        if list == 'Game':
            chosenList = self.gameList
        else:
            chosenList = self.editable

        if output is None:
            output = 'List'
        if output not in ['List', 'String', 'Matrix']:
            print("Parameter 'output': " + output + " not valid. Please choose either 'String', 'List', or 'Matrix'.")
            pass

        if output == 'List':
            return chosenList
        if output == 'String':
            outString = ''
            for x in chosenList:
                outString += str(x)
            return outString
        if output == 'Matrix':
            outMatrix = []
            for r in range(1,10):
                line = []
                for c in range(1,10):
                    line.append(chosenList[self.__rowColumnToIndex(r,c)])
                outMatrix.append(line)
            return outMatrix

    def checkSolution(self):
        goodSolution = True
        for i in range(81):
            row = self.checkGroup(self.isolateRow(i))
            column = self.checkGroup(self.isolateColumn(i))
            square = self.checkGroup(self.isolateSquare(i))
            #print(str(i) + '\t' + str(row) + '\t' + str(column) + '\t' + str(square) + '\t' + str(row and column and square))
            if (row and column and square) == False:
                goodSolution = False
                print('The value at index ' + str(i) + ' violates the rules for a completed board')
        return goodSolution

    def __rowColumnToIndex (self, row, column):
        return (row - 1) * 9 + (column - 1)

    def checkGroup (self, groupList):
        # Assume that groupList is a list of 9 numbers contained in the row/column/square to be checked.
        valid = True
        product = 1
        check = [1,2,3,4,5,6,7,8,9]
        for x in groupList:
            if x not in check:
                valid = False
            product *= x
        #print(product)
        if product != 362880: # 9! = 9*8*7*6*5*4*3*2*1 = 362880
            valid = False
        return valid

    def isolateRow(self, index):
        r = (index // 9) + 1
        row = []
        for c in range(1,10):
            row.append(self.gameList[self.__rowColumnToIndex(r,c)])
        return row

    def isolateColumn(self, index):
        c = (index % 9) + 1
        column = []
        for r in range(1,10):
            column.append(self.gameList[self.__rowColumnToIndex(r,c)])
        return column

    def isolateSquare(self, index):
        square = []
        topLeft = [0,1,2,9,10,11,18,19,20]
        topCenter = [3,4,5,12,13,14,21,22,23]
        topRight = [6,7,8,15,16,17,24,25,26]
        midLeft = [27,28,29,36,37,38,45,46,47]
        midCenter = [30,31,32,39,40,41,48,49,50]
        midRight = [33,34,35,42,43,44,51,52,53]
        botLeft = [54,55,56,63,64,65,72,73,74]
        botCenter = [57,58,59,66,67,68,75,76,77]
        botRight = [60,61,62,69,70,71,78,79,80]
        '''
        The grid-index association
        0  1  2   3  4  5   6  7  8
        9  10 11  12 13 14  15 16 17
        18 19 20  21 22 23  24 25 26

        27 28 29  30 31 32  33 34 35
        36 37 38  39 40 41  42 43 44
        45 46 47  48 49 50  51 52 53

        54 55 56  57 58 59  60 61 62
        63 64 65  66 67 68  69 70 71
        72 73 74  75 76 77  78 79 80
        '''
        if index in topLeft:
            squareIndex = topLeft
        elif index in topCenter:
            squareIndex = topCenter
        elif index in topRight:
            squareIndex = topRight
        elif index in midLeft:
            squareIndex = midLeft
        elif index in midCenter:
            squareIndex = midCenter
        elif index in midRight:
            squareIndex = midRight
        elif index in botLeft:
            squareIndex = botLeft
        elif index in botCenter:
            squareIndex = botCenter
        elif index in botRight:
            squareIndex = botRight
        for i in squareIndex:
            square.append(self.gameList[i])
        return square



s = Sudoku()
s.setNumber(1,0)
s.setNumber(2,1,2)
print(s.getList(output='Matrix'))
print(s.getList(output='Matrix', list='Edit'))
print('\n\n')
s.importList('puzzle.json')
print(s.getList())
print(s.getList(list='Edit'))
s.setNumber(1,0)
s.setNumber(4,5)
print(s.getList(output='Matrix'))
print('\n\nChecking index 10:')
print('Row: ' + str(s.isolateRow(10)))
print('Col: ' + str(s.isolateColumn(10)))
print('Sqr: ' + str(s.isolateSquare(10)))
print('\n\nChecking index 80:')
print('Row: ' + str(s.isolateRow(80)))
print('Col: ' + str(s.isolateColumn(80)))
print('Sqr: ' + str(s.isolateSquare(80)))
print('\n\n')
print(s.checkSolution())
print('\n\n')
s.importList('solvedPuzzle.json')
for line in s.getList('Matrix'):
    print(line)
print(s.checkSolution())
