import matplotlib.pyplot as plt

def save_matrix_as_img(matrix, title, directory, img_format="png"):
	fig, ax = plt.subplots()
	im = ax.imshow(matrix)
	ax.set_xlabel(title)

	directory += "/" if directory[-1] != "/" else ""
	plt.savefig(f"{directory}{title}.{img_format}")
	print(f"matrix image saved as {directory}{title}.{img_format}")
	plt.close()


if __name__ == "__main__":
	# testing
	matrix = [[0 for col in range(10)] for row in range(10)]
	matrix[2][5] = 120
	save_matrix_as_img(matrix, "sample_fig", "visualizer/img")
