# Ian Battin: ibattin@calpoly.edu
# Derek Lance: dwlance@calpoly.edu

import sys, csv, time
from Node import Node
from operator import itemgetter
from csv import parse_small_dataset, parse_large_dataset

def find_node(nodes, label):
	for index, node in enumerate(nodes):
		if node.label == label:
			return index
	return -1

def football(rows):
	nodes = []
	for row in rows:
		index_left = find_node(nodes, row[0])
		index_right = find_node(nodes, row[2])
		if index_left == -1:
			nodes.append(Node(row[0]))
		if index_right == -1:
			nodes.append(Node(row[2]))
		if row[1] > row[3]:
			index_outgoing = find_node(nodes, row[2])
			index_incoming = find_node(nodes, row[0])
			nodes[index_outgoing].add_outgoing(row[0])
			nodes[index_incoming].add_incoming(row[2])
		else:
			index_outgoing = find_node(nodes, row[0])
			index_incoming = find_node(nodes, row[2])
			nodes[index_outgoing].add_outgoing(row[2])
			nodes[index_incoming].add_incoming(row[0])

	return nodes

def write(string):
	sys.stdout.write('\r' + str(string))
	sys.stdout.flush()

def gnutella(rows):
	nodes = []
	for index, row in enumerate(rows):
		#write(f'row {index + 1} / {len(rows)}')
		index_left = find_node(nodes, row[0])
		index_right = find_node(nodes, row[1])
		if index_left == -1:
			nodes.append(Node(row[0]))
			index_left = len(nodes) - 1
		if index_right == -1:
			nodes.append(Node(row[1]))
			index_right = len(nodes) - 1
		nodes[index_left].add_outgoing(row[1])
		nodes[index_right].add_incoming(row[0])
	return nodes

def lesmis(rows):
	nodes = []
	for row in rows:
		index_left = find_node(nodes, row[0])
		index_right = find_node(nodes, row[2])
		if index_left == -1:
			nodes.append(Node(row[0]))
			index_left = len(nodes) - 1
		if index_right == -1:
			nodes.append(Node(row[2]))
			index_right = len(nodes) - 1
		for i in range(row[1]):
			nodes[index_left].add_incoming(row[2])
			nodes[index_left].add_outgoing(row[2])
			nodes[index_right].add_incoming(row[0])
			nodes[index_right].add_outgoing(row[0])
		
	return nodes

def undirected(rows):
	nodes = []
	for row in rows:
		index_left = find_node(nodes, row[0])
		index_right = find_node(nodes, row[2])
		if index_left == -1:
			nodes.append(Node(row[0]))
			index_left = len(nodes) - 1
		if index_right == -1:
			nodes.append(Node(row[2]))
			index_right = len(nodes) - 1
		nodes[index_left].add_incoming(row[2])
		nodes[index_left].add_outgoing(row[2])
		nodes[index_right].add_incoming(row[0])
		nodes[index_right].add_outgoing(row[0])
	
	return nodes

def sum_page_ranks(page_ranks, index, nodes):
	total = 0

	for label in nodes[index].incoming:
		j = find_node(nodes, label)
		total += page_ranks[j] / len(nodes[j].outgoing)

	return total

def total_difference(v1, v2):
	return sum(abs(x - y) for x, y in zip(v1, v2))

def page_rank(nodes, d=0.85, epsilon=1.0e-8):
	N = len(nodes)
	page_ranks = [1 / N] * N

	i = 0
	while(True):
		i += 1

		new_ranks = [ (1 - d) / N + d * sum_page_ranks(page_ranks, i, nodes)
			for i in range(N) ]

		diff = total_difference(page_ranks, new_ranks)
		print(f"Convergence Progress (diff:epsilon): {diff}:{epsilon}")
		if diff < epsilon:
			break

		page_ranks = new_ranks

	print(f'Converged in {i} iterations')

	return list(zip(page_ranks, nodes))

def get_graph_parse_functions(arg):
	x = {
		'dolphin': (undirected, parse_small_dataset),
		'karate': (undirected, parse_small_dataset),
		'lesmis': (lesmis, parse_small_dataset),
		'football': (football, parse_small_dataset),
		'wiki': (gnutella, parse_large_dataset),
		'gnutella': (gnutella, parse_large_dataset),
		'livejournal': (gnutella, parse_large_dataset),
		'slashdot': (gnutella, parse_large_dataset),
		'amazon': (gnutella, parse_large_dataset)
	}
	return x.get(arg, (None, None))

def main():
	start = time.time()
	file_path = sys.argv[1]
	construct_graph, parse_file = get_graph_parse_functions(sys.argv[2])
	if construct_graph is None:
		raise ValueError(f'Invalid value \'{sys.argv[2]}\' for data type')
	lines = parse_file(file_path)
	nodes = construct_graph(lines)
	end = time.time()
	print(f'\nTime to read data and build graph: {round(end - start, 4)} seconds')

	start = time.time()
	page_ranks = page_rank(nodes)
	page_ranks.sort(key=itemgetter(0), reverse=True)
	for index, (rank, node) in enumerate(page_ranks):
		print(f'{index + 1} obj: {node.label} with pagerank: {rank}')

	end = time.time()
	print(f'Page rank processing time: {round(end - start, 4)} seconds')
	
if __name__ == '__main__':
	main()