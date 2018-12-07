class Node:
	def __init__(self, label):
		self.incoming = []
		self.outgoing = []
		self.label = label

	def add_connection(self, connection):
		self.connections.append(connection)
	
	def add_incoming(self, incoming):
		self.incoming.append(incoming)

	def add_outgoing(self, outgoing):
		self.outgoing.append(outgoing)

if __name__ == '__main__':
	node = Node('test node')
	print(node.label)
	node.add_connection(1)
	print(node.connections)
