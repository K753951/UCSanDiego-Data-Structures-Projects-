import sys


class Node:
    def __init__(self, key, left_child, right_child):
        self.key = key
        self.left_child = left_child
        self.right_child = right_child


class BinaryTree:
    def __init__(self):
        self.tree = []

    def add_node(self, key, left_child, right_child):
        new_node = Node(key=key, left_child=left_child, right_child=right_child)
        self.tree.append(new_node)

    def build_tree(self, node_list):
        for entry in node_list:
            self.add_node(key=entry[0], left_child=entry[1], right_child=entry[2])


def in_order_traversal(tree, root_index, result):
    # Find indexes for left and right children of root node.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If the root node has grandchildren in left subtree, keep recursively calling function on left subtree until a
    # terminal subtree is reached.
    if left_node is not -1 and (tree[left_node].left_child is not -1 or tree[left_node].right_child is not -1):
        in_order_traversal(tree, left_node, result)

        # If we have fully traversed the left subtree, append the root key to the result.
        result.append(tree[root_index].key)

    # If a terminal subtree (node has no grandchildren) reached, add first the left child then the root to result.
    elif left_node is not -1:
        result.append(tree[left_node].key)
        result.append(tree[root_index].key)

    # If root node has grandchildren on the right, then recursively call function on right subtree
    # until terminal subtree reached.
    if right_node is not -1 and (tree[right_node].left_child is not -1 or tree[right_node].right_child is not -1):
        in_order_traversal(tree, right_node, result)

    # If the right subtree has no children, append it's key.
    elif right_node is not -1:
        result.append(tree[right_node].key)
    return


def pre_order_traversal(tree, root_index, result):
    # Add the key for the root.
    result.append(tree[root_index].key)

    # Find indexes for left and right children of the root.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If left node has children, call pre_order_traversal on left child.
    if left_node is not -1:
        pre_order_traversal(tree, left_node, result)

    # if right node has children, call pre_order_traversal on right child.
    if right_node is not -1:
        pre_order_traversal(tree, right_node, result)

    return


def post_order_traversal(tree, root_index, result):
    # Find indexes of left and right children of root.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If left child exists and has no children, append its key to result.
    if left_node is not -1 and tree[left_node].left_child is -1 and tree[left_node].right_child is -1:
        result.append(tree[left_node].key)

    # If the left child exists but has children, recursively call function using left child as root node.
    elif left_node is not -1:
        post_order_traversal(tree, left_node, result)

    # If right child exists and has no children, append its key to result.
    if right_node is not -1 and tree[right_node].left_child is -1 and tree[right_node].right_child is -1:
        result.append(tree[right_node].key)

    # If right child exists but has children, recursively call function using right child as root node.
    elif right_node is not -1:
        post_order_traversal(tree, right_node, result)

    # Add root to result.
    result.append(tree[root_index].key)

    return


# Make an array to hold lists of tree data.
tree_data = []

# Open input file.
with open(sys.argv[1]) as in_file:

    # Obtain the number of vertices from the first line of input file. Cast to int.
    num_vertices = int(in_file.readline())

    # Check if num_vertices falls within acceptable parameters.
    if num_vertices < 1 or num_vertices > 100000:
        raise Exception("Invalid number of vertices")

    # Obtain nodes from subsequent lines of input file. Each line contains Node key, left child, and right child.
    for i in range(num_vertices):
        key_L_R = in_file.readline()

        first_space = key_L_R.find(" ")
        entry_key = int(key_L_R[0:first_space])

        # Check that key falls within acceptable parameters.
        if entry_key < 0 or entry_key > 1000000000:
            raise Exception("Invalid key")

        second_space = key_L_R.find(" ", first_space + 1)
        entry_left = int(key_L_R[first_space + 1:second_space])

        backslashn = key_L_R.find("\n")
        entry_right = int(key_L_R[second_space + 1:backslashn])

        # Make a list of information for the new node.
        new = [entry_key, entry_left, entry_right]

        # Append new node information to tree_data list.
        tree_data.append(new)

# Create an instance of the BinaryTree class.
BT = BinaryTree()

# Build the binary tree using data from the tree_data list.
BT.build_tree(tree_data)

# Make lists to hold results.
iot_result = []
preOT_result = []
postOT_result = []

# Call the in_order_traversal function.
in_order_traversal(BT.tree, 0, iot_result)

# Call the pre_order_traversal function.
pre_order_traversal(BT.tree, 0, preOT_result)

# Call the post_order_traversal function.
post_order_traversal(BT.tree, 0, postOT_result)

print(iot_result)
print(preOT_result)
print(postOT_result)