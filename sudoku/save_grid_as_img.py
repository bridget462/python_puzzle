import matplotlib.pyplot as plt
# for visualizing
def save_grid_as_img(grid, title, path="sudoku/img"):
    # NOTE for graph background
    zero_grids = [[0 for col in range(len(grid[0]))] for row in range(len(grid))]

    fig, ax = plt.subplots()
    im = ax.imshow(zero_grids, cmap="binary")

    # text anotation on each cell
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # NOTE: row, colの順番に注意!
            ax.text(col, row, grid[row][col], 
                    color="black", ha="center", va="center")
    plt.xlabel(title)
    path += "/" if path[-1] != "/" else ""
    plt.savefig(f"{path}{title}.png")
    print(f"sudoku grid saved {path}{title}.png")
    plt.close()

# testing
if __name__ == "__main__":
  from input import example_girds
  save_grid_as_img(example_girds["normal1"], "sample_fig")