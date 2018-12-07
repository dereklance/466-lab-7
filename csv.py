def parse_small_dataset(file_path):
	with open(file_path) as file:
		lines = []
		for line in file.read().strip().split('\n'):
			if line[0] != '#':
				row = []
				for index, column in enumerate(line.strip().split(',')):
					if index == 1 or index == 3:
						row.append(int(column.strip()))
					else:
						row.append(column.strip().strip('"'))
				lines.append(row)
		return lines
	
def parse_large_dataset(file_path):
	with open(file_path) as file:
		lines = []
		for line in file.read().strip().split('\n'):
			if line.strip()[0] != '#':
				lines.append(line.strip().split())
		return lines