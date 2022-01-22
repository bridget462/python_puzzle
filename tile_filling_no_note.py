EMPTYPIECE = -1

def recurse_fill_tile(yard, size, row_start, col_start, row_miss, col_miss, next_tile_id):
    #quadrant of missing square: 0 (upper left), 1 (upper right),
    #                            2 (lower left), 3 (lower right)
    section_miss_id = 2*(row_miss >= size//2) + (col_miss >= size//2)
    
    #base case of 2x2 yard
    if size == 2: 
        tile_positions = [(0,0), (0,1), (1,0), (1,1)]
        tile_positions.pop(section_miss_id) # ignore already filled position
        for (row, col) in tile_positions:
            yard[row_start + row][col_start + col] = next_tile_id
        next_tile_id = next_tile_id + 1
        return next_tile_id 


    for section_id in range(4):
        #Each quadrant has a different origin
        #Quadrant 0 has origin (0, 0), Quadrant 1 has origin (0, size//2)
        #Quadrant 2 has origin (size//2, 0), Quadrant 3 has origin (size//2, size//2)
        row_offset = size//2 * (section_id >= 2)
        col_offset = size//2 * (section_id % 2 == 1)
		
        if section_id == section_miss_id:
            next_tile_id = recurse_fill_tile(yard, size//2, row_start + row_offset,\
                col_start + col_offset, row_miss - row_offset, col_miss - col_offset, next_tile_id)
        else:
            #The missing square is different for each of the other 3 quadrants
            section_row_miss = (size//2 - 1) * (section_id < 2)
            section_col_miss = (size//2 - 1) * (section_id % 2 == 0)
			# NOTE: ここではタイルを埋めていない? 先に埋めようとしたらid管理の順番がよくわからなくなってしまった. tileはbase caseだけで埋める?
            next_tile_id = recurse_fill_tile(yard, size//2, row_start + row_offset,\
                            col_start + col_offset, section_row_miss, section_col_miss, next_tile_id)


	# NOTE: 真ん中に作った新しい空白は, 各divided sectionを埋めた後に一度に埋める方法なら, idが各divide section callで変わっても大丈夫
	# 自分で書こうとしたときは 真ん中の空白をcall前に埋めようとしていた. でもcallするとidが変わる&一回ループしないと空白にする場所がわからないので二度手間になってしまっていた
    #place center tromino
	# NOTE: center_positionsは絶対的な座標
    center_positions = [(row + size//2 - 1, col + size//2 - 1)
                 for (row, col) in [(0,0), (0,1), (1,0), (1,1)]] 
    center_positions.pop(section_miss_id)
    for (row, col) in center_positions: # assign tile to 3 center squares
        yard[row_start + row][col_start + col] = next_tile_id
    next_tile_id = next_tile_id + 1

    return next_tile_id


#This procedure is a wrapper for recursiveTile that does all the work
def fill_tile_missing_yard(n, row_miss, col_miss):
    #Initialize yard, this is the only memory that will be modified!
    side_len = 2**n
    yard = [[EMPTYPIECE for i in range(side_len)]
            for j in range(side_len)] 
    recurse_fill_tile(yard, side_len, 0, 0, row_miss, col_miss, 0)
    return yard


#This procedure prints a given tiled yard using letters for tiles
def print_yard(yard):
    for i in range(len(yard)):
        row = ''
        for j in range(len(yard[0])):
            if yard[i][j] != EMPTYPIECE:
                row += chr((yard[i][j] % 26) + ord('A'))
            else:
                row += ' '
        print (row)


print_yard(fill_tile_missing_yard(3, 4, 6))
# printYard(tileMissingYard(4, 5, 7))