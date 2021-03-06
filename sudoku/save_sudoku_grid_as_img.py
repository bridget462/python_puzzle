import matplotlib.pyplot as plt
# for visualizing
def save_sudoku_grid_as_img(grid, title, current_row=-1, current_col=-1, implications=None, is_undo=False, path="sudoku/img"):
    # NOTE for graph background
    zero_grids = [[255 for col in range(len(grid[0]))] for row in range(len(grid))]
    if (current_row, current_col) != (-1, -1):
        zero_grids[current_row][current_col] = 220

    fig, ax = plt.subplots()
    im = ax.imshow(zero_grids, cmap='gray', vmin=0, vmax=255)

    # text anotation on each cell
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # NOTE: row, colの順番に注意!
            ax.text(col, row, grid[row][col], 
                    color="black", ha="center", va="center")

    # highlight implication
    if implications:
        highlight_implication_anotation(ax, implications, is_undo)

    ax.set_xlabel(title, loc='left')
    path += "/" if path[-1] != "/" else ""
    plt.savefig(f"{path}{title}.png")
    print(f"sudoku grid saved {path}{title}.png")
    plt.close()


def highlight_implication_anotation(ax, implications, is_undo):
    for (row, col, num) in implications:
        if not is_undo:
            ax.text(col, row, num, color="blue", ha="center", va="center")
        else:
            ax.text(col, row, 0, color="red", ha="center", va="center")


# testing
if __name__ == "__main__":
  from input import example_girds
  save_sudoku_grid_as_img(example_girds["normal1"], "sample_fig", 4, 4)