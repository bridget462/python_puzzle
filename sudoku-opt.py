import numpy as np

#Programming for the Puzzled -- Srini Devadas
#You Will Never Want to Play Sudoku Again
#Given a partially filled in Sudoku board, complete the puzzle
#obeying the rules of Sudoku

backtracks = 0
EMPTY = 0 # empty cell value

#x varies from entry1 to entry2 - 1, y varies from entry3 to entry4 - 1 
sectors = [ [0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3],
            [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6],
            [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9] ]

#This procedure finds the next empty square to fill on the Sudoku grid
# return (row, col) or (-1, -1)
def findNextCellToFill(grid):
    #Look for an unfilled grid location
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == EMPTY:
                return row,col
    return -1,-1

#This procedure checks if setting the (i, j) square (cell) to e is valid
def isValid(grid, row, col, val):
    # row validation
    is_row_valid = all([val != grid[row][other_col] for other_col in range(9)])
    if not is_row_valid:
        return False

    # col validation
    is_col_valid = all([val != grid[other_row][col] for other_row in range(9)])
    if not is_col_valid:
        return False

    # subsection validation
    section_row_start, section_col_start = 3 * (row//3), 3 * (col//3)
    for other_row in range(section_row_start, section_row_start+3):
        for other_col in range(section_col_start, section_col_start+3):
            # NOTE: 自分自身の場所は例外的にスキップすべきだけど, どこで行ってる?
            # これがなくてもエラーでないのはなぜだ?
            if other_row == row and other_col == col:
                continue
            if grid[other_row][other_col] == val:
                return False
    return True


# IMPORTANT: This procedure makes implications based on existing numbers on squares
def makeImplications(grid, row, col, val):

    global sectors

    grid[row][col] = val
    impl = [(row, col, val)]


    for k in range(len(sectors)):

        sectinfo = []

        #find missing elements in ith sector
        vset = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] != EMPTY:
                    vset.remove(grid[x][y])

        #attach copy of vset to each missing square in ith sector
        for x in range(sectors[k][0], sectors[k][1]):
            for y in range(sectors[k][2], sectors[k][3]):
                if grid[x][y] == EMPTY:
                    sectinfo.append([x, y, vset.copy()])
        
        for m in range(len(sectinfo)):
            sin = sectinfo[m]
            
            #find the set of elements on the row corresponding to m and remove them
            rowv = set()
            for y in range(9):
                rowv.add(grid[sin[0]][y])
            left = sin[2].difference(rowv)
            
            #find the set of elements on the column corresponding to m and remove them
            colv = set()
            for x in range(9):
                colv.add(grid[x][sin[1]])
            left = left.difference(colv)
                         
            #check if the vset is a singleton
            if len(left) == 1:
                val = left.pop()
                if isValid(grid, sin[0], sin[1], val):
                    grid[sin[0]][sin[1]] = val
                    impl.append((sin[0], sin[1], val))

    return impl

#This procedure undoes all the implications
def undoImplications(grid, impl):
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = EMPTY
    return


#This procedure fills in the missing squares of a Sudoku puzzle
#obeying the Sudoku rules by guessing when it has to and performing
#implications when it can
def solveSudokuOpt(grid, i = 0, j = 0):

    global backtracks

    #find the next empty cell to fill
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True

    for e in range(1, 10):
        #Try different values in i, j location
        if isValid(grid, i, j, e):

            impl = makeImplications(grid, i, j, e)
            
            if solveSudokuOpt(grid, i, j):
                return True
            #Undo the current cell for backtracking
            backtracks += 1
            undoImplications(grid, impl)

    return False

def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print (' ')
        print (row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1       
    return

input = [[5,1,7,6,0,0,0,3,4],
         [2,8,9,0,0,4,0,0,0],
         [3,4,6,2,0,5,0,9,0],
         [6,0,2,0,0,0,0,1,0],
         [0,3,8,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

inp2  = [[5,1,7,6,0,0,0,3,4],
         [0,8,9,0,0,4,0,0,0],
         [3,0,6,2,0,5,0,9,0],
         [6,0,0,0,0,0,0,1,0],
         [0,3,0,0,0,6,0,4,7],
         [0,0,0,0,0,0,0,0,0],
         [0,9,0,0,0,0,0,7,8],
         [7,0,3,4,0,0,5,6,0],
         [0,0,0,0,0,0,0,0,0]]

hard  = [[8,5,0,0,0,2,4,0,0],
         [7,2,0,0,0,0,0,0,9],
         [0,0,4,0,0,0,0,0,0],
         [0,0,0,1,0,7,0,0,2],
         [3,0,5,0,0,0,9,0,0],
         [0,4,0,0,0,0,0,0,0],
         [0,0,0,0,8,0,0,7,0],
         [0,1,7,0,0,0,0,0,0],
         [0,0,0,0,3,6,0,4,0]]

diff  = [[0,0,5,3,0,0,0,0,0],
         [8,0,0,0,0,0,0,2,0],
         [0,7,0,0,1,0,5,0,0],
         [4,0,0,0,0,5,3,0,0],
         [0,1,0,0,7,0,0,0,6],
         [0,0,3,2,0,0,0,8,0],
         [0,6,0,5,0,0,0,0,9],
         [0,0,4,0,0,0,0,3,0],
         [0,0,0,0,0,9,7,0,0]]


solveSudokuOpt(inp2)
printSudoku(inp2)
print ('Backtracks = ', backtracks)


# backtracks = 0
# print(solveSudokuOpt(hard))
# printSudoku(hard)
# print ('Backtracks = ', backtracks)

# backtracks = 0
# printSudoku(diff)
# print(solveSudokuOpt(diff))
# printSudoku(diff)
# print ('Backtracks = ', backtracks)

