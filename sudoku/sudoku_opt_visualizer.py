# global variables
backtracks = 0 # to count how many backtrack call has been made
EMPTY = 0 # empty cell value
# x varies from entry1 to entry2 - 1, y varies from entry3 to entry4 - 1 
sectors = [ [0, 3, 0, 3], [3, 6, 0, 3], [6, 9, 0, 3],
            [0, 3, 3, 6], [3, 6, 3, 6], [6, 9, 3, 6],
            [0, 3, 6, 9], [3, 6, 6, 9], [6, 9, 6, 9] ]

from save_sudoku_grid_as_img import save_sudoku_grid_as_img

# fill numbers to grid if its valid sudoku puzzle and return True else return False
def solve_sudoku(grid, row = 0, col = 0):
    global backtracks # for performance counting
    #find the next empty cell to fill
    row, col = find_first_empty_cell(grid)

    # EDGE CASE: grid already filled
    if (row, col) == (-1, -1):
        return True

    for num in range(1, 10):
        if not will_cell_be_valid(grid, row, col, num):
            continue

        # NOTE: do_implications modify grid
        save_sudoku_grid_as_img(grid, f"#backtrack {backtracks} solve_sudoku {row, col, num}", row, col)
        impl = do_implications(grid, row, col, num) 
        save_sudoku_grid_as_img(grid, f"#backtrack {backtracks} solve_sudoku {row, col, num} impl", row, col, impl)
        if solve_sudoku(grid, row, col):
            return True
        backtracks += 1
        undo_implications(grid, impl)
        save_sudoku_grid_as_img(grid, f"#backtrack {backtracks} solve_sudoku {row, col, num} impl undo", row, col, impl, True)

    return False


# return first empty cell (row, col) or (-1, -1) if every cell is filled
def find_first_empty_cell(grid):
    #Look for an unfilled grid location
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == EMPTY:
                return row, col
    return -1, -1


# check filling (row, col) as num will create valid grid
def will_cell_be_valid(grid, row, col, num_to_fill):
    # row validation
    is_row_valid = all([num_to_fill != grid[row][other_col] for other_col in range(9)])
    if not is_row_valid:
        return False

    # col validation
    is_col_valid = all([num_to_fill != grid[other_row][col] for other_row in range(9)])
    if not is_col_valid:
        return False

    # section validation
    section_row_start, section_col_start = 3 * (row//3), 3 * (col//3)
    for other_row in range(section_row_start, section_row_start+3):
        for other_col in range(section_col_start, section_col_start+3):
            if grid[other_row][other_col] == num_to_fill:
                return False
    return True


# mutate grid based on implication and return created implications to undo it later if necessary
# return list of implication as (row, col, num)
def do_implications(grid, row, col, num):
    global sectors

    grid[row][col] = num
    impl = [(row, col, num)]

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
                num = left.pop()
                if will_cell_be_valid(grid, sin[0], sin[1], num):
                    grid[sin[0]][sin[1]] = num
                    impl.append((sin[0], sin[1], num))
    return impl


#This procedure undoes all the implications
def undo_implications(grid, impl):
    for i in range(len(impl)):
        grid[impl[i][0]][impl[i][1]] = EMPTY
    return


def print_sudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print (' ')
        print (row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1       
    return



if __name__ == "__main__":
    # example input
    from input import example_girds
    from output import example_filled_grid

    grid = example_girds["normal2"]
    filled_grid = example_filled_grid["normal2"]

    solve_sudoku(grid)
    print_sudoku(grid)
    print ('Backtracks = ', backtracks)

    # for testing
    print(grid == filled_grid)
