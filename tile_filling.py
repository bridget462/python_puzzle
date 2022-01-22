EMPTYPIECE = -1

def recurse_fill_tile(yard, size, row_start, col_start, row_miss, col_miss, next_tile_id):
    #quadrant of missing square: 0 (upper left), 1 (upper right),
    #                            2 (lower left), 3 (lower right)
    # section計算は相対座標でできる (row_miss, sizeはすべて相対値)
    section_miss_id = 2*(row_miss >= size//2) + (col_miss >= size//2)
    
    #base case of 2x2 yard
    if size == 2: 
      # NOTE: あらかじめ埋まっている場所をpopするのか!. 相対的な位置にすれば絶対的な位置とは違い, 常に計算できる?
      # タイルを埋めるのは絶対座標が必要 (row, col)は絶対座標
        tile_positions = [(0,0), (0,1), (1,0), (1,1)]
        tile_positions.pop(section_miss_id) # ignore already filled position
        for (row, col) in tile_positions:
            yard[row_start + row][col_start + col] = next_tile_id
        next_tile_id = next_tile_id + 1
        return next_tile_id # NOTE: tile_idを戻り地として返すことですべてのrecursive callで共有しているのか.

    #recurse on each quadrant
    for section_id in range(4):
        #Each quadrant has a different origin
        #Quadrant 0 has origin (0, 0), Quadrant 1 has origin (0, size//2)
        #Quadrant 2 has origin (size//2, 0), Quadrant 3 has origin (size//2, size//2)

        # row_section_origin_offset = size//2 * (section_id >= 2)
        # col_section_origin_offset = size//2 * (section_id % 2 == 1)
        # sectionの原点offsetは相対座標で求められる (相対sizeを使うだけ)
        row_section_origin_offset = 0 if section_id < 2 else size // 2
        col_section_origin_offset = 0 if section_id % 2 == 0 else size // 2

        # 原点座標の絶対座標はタイルを埋めるときに必要
        next_row_start = row_start + row_section_origin_offset
        next_col_start = col_start + col_section_origin_offset

        if section_id == section_miss_id:
            #Pass the new origin and the shifted rMiss and cMiss
			# NOTE: divided section row is relative coordinate?
			# たぶんr1, r2, c1, c2を渡すよりも少なくて済む? -> row_start, col_start, board_size
			# NOTE: ここでtile_idもupdateしている. 
            # 次のsectionの原点は絶対座標, missing cell postionは相対座標であることに注意
            next_tile_id = recurse_fill_tile(yard, size//2, next_row_start,\
                next_col_start, row_miss - row_section_origin_offset, col_miss - col_section_origin_offset, next_tile_id)

        else:
            #The missing square is different for each of the other 3 quadrants
            # NOTE: これはnext_row_start, next_col_startからみた相対的な座標!
            # QUESTION: なんで全部絶対的な座標で指定しないのかな?
            # このプログラムでは基本的に相対座標を優先して使っていると思う. 理由としてはrecursive callを行ったあとには, 分割前の座標を知る必要はコンセプト的には必要ないから?
            # でも原点だけは知らないとタイルを埋めることができないので渡している?
            # つまり絶対座標はタイルを埋めるときにしかつかっていない?
            section_row_miss = (size//2 - 1) * (section_id < 2)
            section_col_miss = (size//2 - 1) * (section_id % 2 == 0)
			# NOTE: ここではタイルを埋めていない? 先に埋めようとしたらid管理の順番がよくわからなくなってしまった. tileはbase caseだけで埋める?
            next_tile_id = recurse_fill_tile(yard, size//2, next_row_start,\
                            next_col_start, section_row_miss, section_col_miss, next_tile_id)


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