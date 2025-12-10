import os

import numpy as np


class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path:str) -> None:

        # list of lists (rows)
        #load sudoku from file with split and list comprehension
        loaded_rows : list[list[int]] = []
        with open(file_path, encoding="utf8") as file:
            for line in file:
                numbers = line.split(";")
                b = [int(num) for num in numbers]
                loaded_rows.append(b)
                    
                

        # convert nested list to numpy array
        self.field = np.array(loaded_rows)



    def check_sequence(self, sequence:np.ndarray) -> bool:
        #Checks if something repeats in a sequence
        array = [0,0,0,0,0,0,0,0,0]


        for num in sequence:
            match num:
                case 1:
                    array[0] += 1
                case 2:
                    array[1] += 1
                case 3:
                    array[2] += 1
                case 4:
                    array[3] += 1
                case 5:
                    array[4] += 1
                case 6:
                    array[5] += 1
                case 7:
                    array[6] += 1
                case 8:
                    array[7] += 1
                case 9:
                    array[8] += 1
                case _:
                    pass
        
        for i in array:
            if(i>1):
                return False
        return True

    def check_row(self, row_index:int) -> bool:
        return self.check_sequence(self.field[row_index , :])
        

    def check_column(self, column_index:int) -> bool:
        return self.check_sequence(self.field[: , column_index])

    def check_block(self, row_index:int, column_index:int) -> bool:
        #Calculates the start of the block and then takes all the arrays in the block flattened into one
        startRow= (row_index // 3 ) * 3
        startColumn = (column_index // 3) * 3
    
        block = self.field[startRow:startRow + 3, startColumn:startColumn + 3].flatten()
        
        return self.check_sequence(block)
    


    def check_one_cell(self, row_index:int , column_index:int) -> bool:
        #Checks one cell for every possibility
        return (self.check_row(row_index) and
                self.check_column(column_index) and
                self.check_block(row_index,column_index))

    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """
        for i in range(self.field.shape[0]):
            for j in range(self.field.shape[1]):
                if(self.field[i][j] == 0):
                    return (i,j)
        return None

    def solve(self) -> bool:
        """ Recursively solves the sudoku. """
        empty_cell = self.get_empty_cell()
        if empty_cell is None:
            return True
        
        #Tries to add every possible number into the block
        #Then checks if its possible solution, if yes it calls itself again, if not it goes back

        row, col = empty_cell
        for cell_value in range(1,10):
            self.field[row,col] = cell_value
            if not self.check_one_cell(row,col):
                continue

            if(self.solve()):
                return True
        
        self.field[row,col] = 0
        return False 





def main() -> None:
    sudoku_solver = SudokuSolver()
    sudoku_solver.load("sudoku.csv")
    sudoku_solver.solve()
    print(sudoku_solver.field)

if __name__ == "__main__":
    main()

