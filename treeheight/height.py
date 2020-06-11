import sys
import numpy as np


class Node:
    def __init__(self, parent, key):
        self.parent = parent
        self.child = []
        self.key = key

    def add_child(self, new_child):
        self.child.append(new_child)

class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, next_node):
        self.frontier.extend(next_node)

    def remove(self):
        if len(self.frontier) == 0:
            raise Exception("cannot remove node, empty frontier")
        else:
            removed_node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return removed_node


# First, open the text file in read mode.
file1 = open(sys.argv[1], "r")

# Obtain the number of nodes from line one of the text file.
node_number = int(file1.readline())

if node_number < 1 or node_number > 100000:
    raise Exception("Incorrect tree size")

# Read the tree data into string 'data'.
data = file1.readline()

file1.close()

# Convert tree data into a list.
tree_data = []
neg_number = 0
for number in data:
    if number == '-':
        neg_number = 1
    elif number != '-' and neg_number == 1:
        tree_data.append((int(number)) * -1)
        neg_number = 0
    else:
        tree_data.append(int(number))

# Create an array of nodes.
nodes = np.empty(node_number, dtype=Node)

# Initialize each node to have key i and parent None
for i in range(node_number):
    nodes[i] = Node(key=i, parent=None)

for i in range(node_number):
    if tree_data[i] != -1:
        nodes[i].parent = nodes[tree_data[i]]

# Add children to nodes.
for i in range(node_number):
    Parent = tree_data[i]
    if Parent != -1:
        nodes[Parent].add_child(nodes[i])

# Create a queue frontier.
Frontier = QueueFrontier()

# Find root of tree.
root = Node(parent=None, key=None)
for node in nodes:
    if node.parent is None:
        root = node

# First, add children of root to the frontier.
Frontier.add(root.child)

# Depth-first search to find longest path
height = 1
while True:
    if len(Frontier.frontier) == 0:
        raise Exception('Something went wrong, frontier empty.')
    else:
        check_node = Frontier.remove()
        if len(Frontier.frontier) == 0 and len(check_node.child) == 0:
            while check_node.parent is not None:
                height += 1
                check_node = check_node.parent
            print(height)
            exit()
        else:
            Frontier.add(check_node.child)


