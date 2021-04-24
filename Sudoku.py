# Author: Kit Vander Wilt

"""
Game Logic for playing Sudoku.

Classes:
    Sudoku
    Number

Functions:

Misc variables:

"""


class Number:
    """
    Structure to hold all relevant data associated to a number/square in a Sudoku game

    Attributes:
        value: An integer between 1 and 9
        editable: A boolean representing if the value can be changed. Should only be set during initialization.
        valid: A boolean to keep track of whether or not the value is considered correct in the puzzle.
    """

    def __init__(self, value: int, editable: bool, valid: bool):
        self.value = value
        self.editable = editable
        self.valid = valid

    def get_value(self):
        return self.value

    def set_value(self, value: int):
        self.value = value

    def get_editable(self):
        return self.editable

    def get_valid(self):
        return self.valid

    def set_valid(self, valid: bool):
        self.valid = valid


class Sudoku:
    """
    A Module implementing the game of Sudoku.

    To create a game, pass in a string or list of numbers where 0's represent blank squares.

    Attributes:
        numbers: A list of Numbers (see above). Will always be 81 elements long, indices 0-8 are the "top row",
            indices 9-17 are the "second row", and so on until indices 72-80 represent the "bottom row".
            suppose that r in range(9) and c in range(9) then r*9+c is the index in numbers for the (r, c) square.

    Functions:
        get_number()
        set_number()
        get_puzzle()
        check_puzzle()
        solve_puzzle()
        clear_progress()
    """

    def __init__(self, input):
        self.numbers = []
        if len(input) == 81:
            if isinstance(input, str):
                nums = [int(x) for x in input]
            elif isinstance(input, list):
                nums = input
            else:
                raise TypeError(f'Unable to create sudoku game with {input}')
            for num in nums:
                if num == 0:
                    self.numbers.append(Number(num, True, False))
                else:
                    self.numbers.append(Number(num, False, True))

    def get_number(self, index: int):
        """
        Get the value of the number at the specified index.

        :param index: An integer between 0 and 80.
        :return: An integer between 1 and 9.
        """
        return self.numbers[index].get_value()

    def get_editable(self, index: int):
        return self.numbers[index].get_editable()

    def get_valid(self, index: int):
        return self.numbers[index].get_valid()

    def set_number(self, index: int, value: int):
        """
        Set the value of the number at the specified index.

        :param index: An integer between 0 and 80.
        :param value: An integer between 1 and 9.
        :return: A boolean to show whether or not the number was allowed to be set. Equals Number.editable
        """
        if self.numbers[index].get_editable():
            self.numbers[index].set_value(value)
            self.numbers[index].set_valid(self.__check_value(index))
        return self.numbers[index].get_editable()

    def __check_value(self, index):
        row = self.__check_value_list(index, self.__gen_row_list(index))
        col = self.__check_value_list(index, self.__gen_column_list(index))
        sqr = self.__check_value_list(index, self.__gen_square_list(index))
        return row and col and sqr

    def __check_value_list(self, index, my_list):
        output = True
        for x in my_list:
            if x != index and self.numbers[index].get_value() == self.numbers[x].get_value():
                output = False
        return output

    def __gen_row_list(self, index):
        x = index // 9
        return list(range(9 * x, 9 * x + 9))

    def __gen_column_list(self, index):
        x = index % 9
        return [k*9+x for k in range(9)]

    def __gen_square_list(self, index):
        squares = [
            [0, 1, 2, 9, 10, 11, 18, 19, 20],
            [3, 4, 5, 12, 13, 14, 21, 22, 23],
            [6, 7, 8, 15, 16, 17, 24, 25, 26],
            [27, 28, 29, 36, 37, 38, 45, 46, 47],
            [30, 31, 32, 39, 40, 41, 48, 49, 50],
            [33, 34, 35, 42, 43, 44, 51, 52, 53],
            [54, 55, 56, 63, 64, 65, 72, 73, 74],
            [57, 58, 59, 66, 67, 68, 75, 76, 77],
            [60, 61, 62, 69, 70, 71, 78, 79, 80]
        ]
        output = None
        for s in squares:
            if index in s:
                output = s
        return output

    def get_puzzle(self):
        """
        Get the current state of the puzzle all at once.

        :return: A list of 81 Numbers representing the current game state.
        """
        return self.numbers

    def check_puzzle(self):
        """
        Check the current game state to see if you won.

        :return: A boolean representing whether or not the sudoku puzzle is complete and correct.
        """
        output = True
        for r in range(9):
            for c in range(9):
                loc = r*9+c
                self.numbers[loc].set_valid(self.__check_value(loc))
                if not self.numbers[loc].get_valid():
                    output = False
        return output

    def solve_puzzle(self):
        """
        Function to fill in all blank squares, regardless of the correctness of previously input data.

        :return: Void
        """
        pass

    def clear_progress(self):
        """
        Function to clear all progress on the Numbers that are editable.

        :return: Void
        """
        pass





