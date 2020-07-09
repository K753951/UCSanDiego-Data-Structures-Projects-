import sys


class Node:
    def __init__(self, key, left_child, right_child, parent, lr):
        self.key = key
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent
        self.lr = lr


class BinaryTree:
    def __init__(self):
        self.tree = []

    def add_node(self, key, left_child, right_child):
        new_node = Node(key=key, left_child=left_child, right_child=right_child, parent=None, lr=None)
        self.tree.append(new_node)

    def build_tree(self, node_list):
        for entry in node_list:
            self.add_node(key=entry[0], left_child=entry[1], right_child=entry[2])


def post_order_traversal(tree, root_index, result):
    # Find indexes of left and right children of root.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If left child exists and has no children, append its key to result.
    if left_node is not -1 and tree[left_node].left_child is -1 and tree[left_node].right_child is -1:
        result.append(left_node)

    # If the left child exists but has children, recursively call function using left child as root node.
    elif left_node is not -1:
        post_order_traversal(tree, left_node, result)

    # If right child exists and has no children, append its key to result.
    if right_node is not -1 and tree[right_node].left_child is -1 and tree[right_node].right_child is -1:
        result.append(right_node)

    # If right child exists but has children, recursively call function using right child as root node.
    elif right_node is not -1:
        post_order_traversal(tree, right_node, result)

    # Add root to result.
    result.append(root_index)

    return


class Queue:
    def __init__(self):
        self.queue = []

    def insert(self, element):
        self.queue.append(element)

    def extract(self):
        if len(self.queue) == 0:
            raise Exception("Cannot remove element, empty frontier")
        else:
            element = self.queue[0]
            self.queue = self.queue[1:]
            return element


# Make an array to hold lists of tree data.
tree_data = []

# Open input file.
with open(sys.argv[1]) as in_file:

    # Obtain the number of vertices from the first line of input file. Cast to int.
    num_vertices = int(in_file.readline())

    # Check if num_vertices falls within acceptable parameters.
    if num_vertices < 0 or num_vertices > 100000:
        raise Exception("Invalid number of vertices")

    # Obtain nodes from subsequent lines of input file. Each line contains Node key, left child, and right child.
    for i in range(num_vertices):
        key_L_R = in_file.readline()

        first_space = key_L_R.find(" ")
        entry_key = int(key_L_R[0:first_space])

        # Check that key falls within acceptable parameters.
        if entry_key < -2147483648 or entry_key > 2147483648:
            raise Exception("Invalid key")

        second_space = key_L_R.find(" ", first_space + 1)
        entry_left = int(key_L_R[first_space + 1:second_space])

        backslashn = key_L_R.find("\n")
        entry_right = int(key_L_R[second_space + 1:backslashn])

        # Make a list of information for the new node.
        new = [entry_key, entry_left, entry_right]

        # Append new node information to tree_data list.
        tree_data.append(new)

if len(tree_data) is not 0:
    # Create an instance of the BinaryTree class.
    BT = BinaryTree()

    # Build the binary tree using data from the tree_data list.
    BT.build_tree(tree_data)

    # Add parents to binary tree.
    for i in range(len(BT.tree)):
        l_child = BT.tree[i].left_child
        r_child = BT.tree[i].right_child
        if l_child is not -1:
            BT.tree[l_child].parent = i
            BT.tree[l_child].lr = "left"
        if r_child is not -1:
            BT.tree[r_child].parent = i
            BT.tree[r_child].lr = "right"

    # Make a list of elements in order determined by post-order traversal.
    queue_list = []
    post_order_traversal(BT.tree, 0, queue_list)

    # Make an instance of the Queue class and populate with node indexes from queue_list.
    queue = Queue()

    for node in queue_list:
        queue.insert(node)

    # Remove elements from queue and check their validity.
    # First, make a variable, success, to indicate if tree is a valid binary search tree or not.
    success = True

    # Iterate through all elements in queue and check if they follow rules of binary search tree.
    while len(queue.queue) is not 0:

        # The success variable indicates whether or not binary search tree is valid.
        success = True

        # Get the index of the current node, the index of the node's parent, and whether the
        # node is a left or right child.
        node_index = queue.extract()
        parent_index = BT.tree[node_index].parent
        side = BT.tree[node_index].lr

        # Get the index of the parent of the closest node whose lr value is not equal to side.
        loop = True
        ancestor = parent_index
        while loop is True:
            if ancestor is not None:
                if BT.tree[ancestor].lr == side:
                    ancestor = BT.tree[ancestor].parent
                else:
                    loop = False
            else:
                break
        if loop is False:
            if ancestor is not None:
                ancestor = BT.tree[ancestor].parent
        else:
            ancestor = None

        # If node is a left child, check if it's key is less than the key of the parent.
        # Then check if node.key is greater than or equal to the parent of the closest ancestor
        # that is itself a right child.
        if side == "left":
            if BT.tree[node_index].key >= BT.tree[parent_index].key:
                success = False
                break
            if ancestor is not None and BT.tree[node_index].key < BT.tree[ancestor].key:
                success = False
                break

        if side == "right":
            if BT.tree[node_index].key < BT.tree[parent_index].key:
                success = False
                break
            if ancestor is not None and BT.tree[node_index].key >= BT.tree[ancestor].key:
                success = False
                break

    if success is True:
        print("CORRECT")
    if success is False:
        print("INCORRECT")

# If the binary tree is empty, it is valid.
elif len(tree_data) is 0:
    print("CORRECT")
