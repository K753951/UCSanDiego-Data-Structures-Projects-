import sys
from time import process_time


class Node:
    def __init__(self, key, character, left_child, right_child, parent):
        self.key = key
        self.character = character
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent


class SplayTree:
    def __init__(self):
        self.tree = []
        self.root = 0
        self.length = 0

    def find(self, key, root):
        """ Returns either the index of the node with the given key or the index of the node that should
        be the parent of the node with the given key. """
        # If the tree is empty, the new node belongs at index 0 and is the root.
        if self.length is 0:
            return 0

        # If key is found in the tree, splay that node then return the index of the node with this key.
        elif self.tree[root].key == key:
            self.splay(root)
            return root

        # If key is less than the key of the current subtree root, traverse the left subtree.
        elif self.tree[root].key > key:
            leftchild = self.tree[root].left_child
            if leftchild is not None and self.tree[leftchild].key is not None:
                return self.find(key, leftchild)

            # Splay the found node, then return it.
            self.splay(root)
            return root

        # If key is greater than the key of the current subtree root, traverse the right subtree.
        elif self.tree[root].key < key:
            rightchild = self.tree[root].right_child
            if rightchild is not None and self.tree[rightchild].key is not None:
                return self.find(key, rightchild)

            # Splay the found node, then return it.
            self.splay(root)
            return root

    def add_node(self, key, character):
        # If the AVL tree is empty, the new node becomes the root.
        if self.length == 0:
            root_node = Node(key=key, left_child=None, right_child=None, parent=None, character=character)
            self.tree.append(root_node)
            self.length += 1
            return

        # Find the position in the tree where the new node should be added
        # (or find the key in the tree if duplicate)
        index = self.find(key, self.root)

        # If AVL tree is not empty and the key of the node at the returned index does not match the
        # updated key to be added, add updated key as child of node at returned index.
        # If key of node at the returned index matches the key to be added, do nothing.
        if self.tree[index].key != key:

            # If updated key is less than the key at self.tree[index], add the new node as a left child.
            if self.tree[index].key > key:
                self.tree[index].left_child = len(self.tree)
                new_node = Node(key=key, left_child=None, right_child=None, parent=index, character=character)
                self.tree.append(new_node)

            # If updated key is greater than the key at self.tree[index], add the new node as a right child.
            if self.tree[index].key < key:
                self.tree[index].right_child = len(self.tree)
                new_node = Node(key=key, left_child=None, right_child=None, parent=index, character=character)
                self.tree.append(new_node)

            # Update the length of the tree.
            self.length += 1

            # Splay the added node.
            self.splay(key)
        return

    def great_grandparent(self, greatgp, element, grandparent):
        # If the grandparent is the root, update self.root.
        if greatgp is None:
            self.root = element
            self.tree[element].parent = None

        # Else, determine if grandparent is itself a left or right child. Change left or right child of great
        # grandparent to index of element. Change parent of element to greatgp.
        elif self.tree[greatgp].left_child == grandparent:
            self.tree[greatgp].left_child = element
            self.tree[element].parent = greatgp
        else:
            self.tree[greatgp].right_child = element
            self.tree[element].parent = greatgp
        return

    def zig_zig(self, element, parent, grandparent, l_or_r):
        """ Used to splay tree when element, parent, and grandparent are all on the same side. """
        # Find index of great grandparent.
        greatgp = self.tree[grandparent].parent

        # Take care of great grandparent's pointers.
        self.great_grandparent(greatgp, element, grandparent)

        # If the lineage is made up of left children, do the following.
        if l_or_r == 0: #left
            element_right = self.tree[element].right_child
            parent_right = self.tree[parent].right_child

            # Update the element's right child to point at the parent.
            self.tree[element].right_child = parent
            self.tree[parent].parent = element

            # The parent's left child points to the old right child of the element.
            self.tree[parent].left_child = element_right
            if element_right is not None:
                self.tree[element_right].parent = parent

            # The parent's right child is now the grandparent.
            self.tree[parent].right_child = grandparent
            self.tree[grandparent].parent = parent

            # The grandparent's left child is now the parent's old right child.
            self.tree[grandparent].left_child = parent_right
            if parent_right is not None:
                self.tree[parent_right].parent = grandparent

        # Else if the lineage is made up of right children
        else:
            element_left = self.tree[element].left_child
            parent_left = self.tree[parent].left_child

            # The element's left child is now the parent.
            self.tree[element].left_child = parent
            self.tree[parent].parent = element

            # The parent's right child is now the element's left child.
            self.tree[parent].right_child = element_left
            if element_left is not None:
                self.tree[element_left].parent = parent

            # The parent's left child is now the grandparent.
            self.tree[parent].left_child = grandparent
            self.tree[grandparent].parent = parent

            # The grandparent's right child is now the parent's old left child.
            self.tree[grandparent].right_child = parent_left
            if parent_left is not None:
                self.tree[parent_left].parent = grandparent
        return

    def zig_zag(self, element, parent, grandparent, l_or_r):
        """ Used to splay tree when element and grandparent are on opposite side as parent. """
        # Find index of great grandparent.
        greatgp = self.tree[grandparent].parent

        # Take care of great grandparent's pointers.
        self.great_grandparent(greatgp, element, grandparent)

        # Helpful variables for the conversions below.
        element_right = self.tree[element].right_child
        element_left = self.tree[element].left_child

        # If element and grandparent are on the right:
        if l_or_r == 1:

            # The left child of element is now parent.
            self.tree[element].left_child = parent
            self.tree[parent].parent = element

            # The right child of element is now grandparent.
            self.tree[element].right_child = grandparent
            self.tree[grandparent].parent = element

            # The right child of parent is now element_left.
            self.tree[parent].right_child = element_left
            if element_left is not None:
                self.tree[element_left].parent = parent

            # The left child of grandparent is now element_right.
            self.tree[grandparent].left_child = element_right
            if element_right is not None:
                self.tree[element_right].parent = grandparent

        # If element and grandparent are on left:
        else:

            # The left child of element is now grandparent.
            self.tree[element].left_child = grandparent
            self.tree[grandparent].parent = element

            # The right child of element is now parent.
            self.tree[element].right_child = parent
            self.tree[parent].parent = element

            # The right child of grandparent is now element_left.
            self.tree[grandparent].right_child = element_left
            if element_left is not None:
                self.tree[element_left].parent = grandparent

            # The left child of parent is now element_right.
            self.tree[parent].left_child = element_right
            if element_right is not None:
                self.tree[element_right].parent = parent
        return

    def zig(self, element, root):
        """ Used to splay tree when element is just below root. """

        # The root of the tree becomes the element.
        self.root = element
        self.tree[element].parent = None

        # Do the following if the element is the root's right child.
        if self.tree[root].right_child == element:
            element_left = self.tree[element].left_child

            # The element's left child is now the old root.
            self.tree[element].left_child = root
            self.tree[root].parent = element

            # The old root's right child is now the element's old left child.
            self.tree[root].right_child = element_left
            if element_left is not None:
                self.tree[element_left].parent = root

        # If the element is the root's left child, do this.
        else:
            element_right = self.tree[element].right_child

            # The element's right child is now the old root.
            self.tree[element].right_child = root
            self.tree[root].parent = element

            # The old root's left child is now the old right child of element.
            self.tree[root].left_child = element_right
            if element_right is not None:
                self.tree[element_right].parent = root

    def splay(self, element):
        # If element is already the root of the tree, return.
        if self.tree[element].parent is None:
            return

        # If there is more than one element in the tree, find the parent and grandparent.
        parent = self.tree[element].parent
        grandparent = self.tree[parent].parent

        # If grandparent is None, correct case is zig.
        if grandparent is None:
            self.zig(element, parent)

        # If grandparent exists, determine whether zig-zig or zig-zag is appropriate.
        else:
            if self.tree[parent].left_child == element:
                e_side = 0
            else:
                e_side = 1
            if self.tree[grandparent].left_child == parent:
                p_side = 0
            else:
                p_side = 1

            # If element and parent are on the same side, apply zig-zig.
            if e_side == 0 and p_side == 0:
                self.zig_zig(element, parent, grandparent, l_or_r=0)
            elif e_side == 1 and p_side == 1:
                self.zig_zig(element, parent, grandparent, l_or_r=1)

            # If element and parent are on opposite sides, apply zig-zag.
            elif e_side == 0 and p_side == 1:
                self.zig_zag(element, parent, grandparent, l_or_r=0)
            else:
                self.zig_zag(element, parent, grandparent, l_or_r=1)

        # If, after applying the appropriate function, the parent of element is not None, call function again.
        if self.tree[element].parent is not None:
            self.splay(element)
        else:
            return

    def split_right(self, key, root):
        """ Returns the indexes of two subtrees. Key is the index of the root of the right subtree. """
        # Find node with key = key in subtree with root = root. This automatically splays element to top.
        right_root = self.find(key, root)

        # Update parent of new root to None.
        self.tree[right_root].parent = None

        # Update parent of new root left child to None (it is now the root of its subtree).
        left_root = self.tree[right_root].left_child
        if left_root is not None:
            self.tree[left_root].parent = None

        # Update right_root left child to None
        self.tree[right_root].left_child = None

        # Add indexes of left and right roots to the result tuple.
        result = (left_root, right_root)

        # Return result.
        return result

    def split_left(self, key, root):
        """ Returns the indexes of two subtrees. Key is the index of the root of the left subtree. """
        # Find node with key = key in subtree with root = root. This automatically splays element to top.
        left_root = self.find(key, root)

        # Update parent of new root to None.
        self.tree[left_root].parent = None

        # Update parent of new root right child to None (it is now the root of its subtree). If no left child,
        # the left subtree is None.
        right_root = self.tree[left_root].right_child
        if right_root is not None:
            self.tree[right_root].parent = None

        # Update left_root right child to None
        self.tree[left_root].right_child = None

        # Add indexes of left and right roots to the result tuple.
        result = (left_root, right_root)

        # Return result.
        return result

    def find_largest(self, tree_root):
        while self.tree[tree_root].right_child is not None:
            tree_root = self.tree[tree_root].right_child
        self.splay(tree_root)
        return tree_root

    def merge(self, smaller_tree, larger_tree):
        # Find the largest element of the smallest tree and splay it to the top.
        largest_of_smaller = self.find_largest(smaller_tree)

        # Merge trees by adding the root of the larger tree as the right child of the newly-arranged smaller tree.
        self.tree[largest_of_smaller].right_child = larger_tree
        if larger_tree is not None:
            self.tree[larger_tree].parent = largest_of_smaller

        # Return the root of the new tree.
        return largest_of_smaller


def in_order_traversal(tree, root_index, result):
    # Find indexes for left and right children of root node.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If the tree has only one node, just append it's index and return.
    if left_node is None and right_node is None:
        result.append(root_index)
        return

    # If the root node has grandchildren in left subtree, keep recursively calling function on left subtree until a
    # terminal subtree is reached.
    if left_node is not None and (tree[left_node].left_child is not None or tree[left_node].right_child is not None):
        in_order_traversal(tree, left_node, result)

        # If we have fully traversed the left subtree, append the root key to the result.
        result.append(root_index)

    # If a terminal subtree (node has no grandchildren) reached, add first the left child then the root to result.
    elif left_node is not None:
        result.append(left_node)
        result.append(root_index)

    # If node has no left ancestors, add root to result list.
    else:
        result.append(root_index)

    # If root node has grandchildren on the right, then recursively call function on right subtree
    # until terminal subtree reached.
    if right_node is not None and (tree[right_node].left_child is not None or tree[right_node].right_child is not None):
        in_order_traversal(tree, right_node, result)

    # If the right subtree has no children, append it's key.
    elif right_node is not None:
        result.append(right_node)
    return


def get_characters(tree, root_index, result):
    # Find indexes for left and right children of root node.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If the tree has only one node, just append it's character and return.
    if left_node is None and right_node is None:
        result.append(tree[root_index].character)
        return

    # If the root node has grandchildren in left subtree, keep recursively calling function on left subtree until a
    # terminal subtree is reached.
    if left_node is not None and (tree[left_node].left_child is not None or tree[left_node].right_child is not None):
        get_characters(tree, left_node, result)

        # If we have fully traversed the left subtree, append the root key to the result.
        result.append(tree[root_index].character)

    # If a terminal subtree (node has no grandchildren) reached, add first the left child then the root to result.
    elif left_node is not None:
        result.append(tree[left_node].character)
        result.append(tree[root_index].character)

    # If node has no left ancestors, add root to result list.
    else:
        result.append(tree[root_index].character)

    # If root node has grandchildren on the right, then recursively call function on right subtree
    # until terminal subtree reached.
    if right_node is not None and (tree[right_node].left_child is not None or tree[right_node].right_child is not None):
        get_characters(tree, right_node, result)

    # If the right subtree has no children, append it's key.
    elif right_node is not None:
        result.append(tree[right_node].character)
    return


def correct_keys(tree, root_index, correction_factor):
    # Find indexes for left and right children of root node.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If the tree has only one node, just append it's index and return.
    if left_node is None and right_node is None:
        tree[root_index].key += correction_factor
        return

    # If the root node has grandchildren in left subtree, keep recursively calling function on left subtree until a
    # terminal subtree is reached.
    if left_node is not None and (tree[left_node].left_child is not None or tree[left_node].right_child is not None):
        correct_keys(tree, left_node, correction_factor)

        # If we have fully traversed the left subtree, append the root key to the result.
        tree[root_index].key += correction_factor

    # If a terminal subtree (node has no grandchildren) reached, add first the left child then the root to result.
    elif left_node is not None:
        tree[left_node].key += correction_factor
        tree[root_index].key += correction_factor

    # If node has no left ancestors, add root to result list.
    else:
        tree[root_index].key += correction_factor

    # If root node has grandchildren on the right, then recursively call function on right subtree
    # until terminal subtree reached.
    if right_node is not None and (tree[right_node].left_child is not None or tree[right_node].right_child is not None):
        correct_keys(tree, right_node, correction_factor)

    # If the right subtree has no children, append it's key.
    elif right_node is not None:
        tree[right_node].key += correction_factor
    return


start_time = process_time()

# Make a splay tree to hold input.
ST = SplayTree()

# Open the input file and read the data.
with open(sys.argv[1]) as infile:
    input_string = infile.readline()
    n = len(input_string)

    # Check that input_string has a valid length.
    if n > 300000 or n < 1:
        raise Exception("Invalid input string")

    # Add nodes to splay tree.
    for i in range(n - 1):
        ST.add_node(i, input_string[i])

    # Splay the tree to get a more even distribution.
    for i in range(n - 2, 0, -50):
        ST.splay(i)

    # Get number of instructions.
    q = int(infile.readline())

    # Check that number of instructions is valid.
    if q < 1 or q > 100000:
        raise Exception("Invalid number of queries")

    # Get instructions.
    for x in range(q):
        instruction = infile.readline()

        first_space = instruction.find(" ")
        i = int(instruction[:first_space])

        second_space = instruction.find(" ", first_space + 1)
        j = int(instruction[first_space + 1:second_space])

        backslashn = instruction.find("\n", second_space + 1)
        k = int(instruction[second_space + 1:backslashn])

        # Check that input is valid.
        if i < 0 or i > j or j > n - 1 or k < 0 or k > n - (j - i + 1):
            raise Exception("Invalid instruction")

        # The following code should be executed if the spliced characters are moving forward in the string.
        if k > j:
            # Split the tree such that j and i are both in the same subtree
            first_split = ST.split_left(j, ST.root)

            # Split the left subtree of first_split to isolate only i through j in the resulting right subtree.
            second_split = ST.split_right(first_split[0], i)

            # Update keys of elements i through j.
            correct_keys(ST.tree, second_split[1], k - j)

            # Find all elements between j + 1 and k inclusive. To do this, split the right subtree of first_split
            # (holding all elements larger than j) at k. Use split_left to include k.
            third_split = ST.split_left(k, first_split[1])

            # Update the keys of all nodes in the interval between j + 1 and k inclusive.
            correct_keys(ST.tree, third_split[0], i - j - 1)

            # Merge interval left and right subtrees back together.
            if third_split[1] is not None:
                merge1 = ST.merge(second_split[1], third_split[1])
            else:
                merge1 = second_split[1]

            # Merge j_pointer back with rest of tree. Interval[0] always exists because it includes k.
            merge2 = ST.merge(third_split[0], merge1)

            # Merge new_leftroot back with tree.
            if second_split[0] is not None:
                merge3 = ST.merge(second_split[0], merge2)
            else:
                merge3 = merge2

            # Update self.root.
            ST.root = merge3

        # The following code should be executed if the spliced characters are moving backward in the string.
        elif k < i:

            # Split the tree at i. The right subtree contains both j and i, while the left contains k.
            first_split = ST.split_right(i, ST.root)

            # Split the right subtree of first_split at j. The left subtree contains only i and j.
            # The right subtree contains all nodes greater than j.
            second_split = ST.split_left(j, first_split[1])

            # Correct keys for i-j.
            correct_keys(ST.tree, second_split[0], k - i + 1)

            # Split the left subtree of first_split at k. Intervening nodes (those > k but < i) are found in the
            # right subtree. All nodes <= k are found in the left subtree.
            third_split = ST.split_left(k, first_split[0])

            # Correct keys for intervening nodes.
            correct_keys(ST.tree, third_split[1], j - i + 1)

            # Merge all nodes > j with intervening nodes.
            if third_split[1] is not None and second_split[1] is not None:
                merge1 = ST.merge(third_split[1], second_split[1])
            elif third_split[1] is None and second_split[1] is not None:
                merge1 = second_split[1]
            elif third_split[1] is not None and second_split[1] is None:
                merge1 = third_split[1]
            else:
                merge1 = None

            # Merge all nodes i-j with merge1.
            if merge1 is not None:
                merge2 = ST.merge(second_split[0], merge1)
            else:
                merge2 = second_split[0]

            # Merge all nodes <= k with merge2.
            merge3 = ST.merge(third_split[0], merge2)

            # Update root of main tree.
            ST.root = merge3

# Print the results.
new_string = []
get_characters(ST.tree, ST.root, new_string)
for character in new_string:
    print(character, end="")
print("\n")

stop_time = process_time()
print("time: ", stop_time - start_time)
