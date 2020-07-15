import sys


M = 1000000001


def pre_order_traversal(tree, root_index, lower_bound, result):
    # Add the key for the root.
    if tree[root_index].key < lower_bound:
        return
    result.append(tree[root_index].key)

    # Find indexes for left and right children of the root.
    left_node = tree[root_index].left_child
    right_node = tree[root_index].right_child

    # If left node has children, call pre_order_traversal on left child.
    if left_node is not None:
        pre_order_traversal(tree, left_node, lower_bound, result)

    # if right node has children, call pre_order_traversal on right child.
    if right_node is not None:
        pre_order_traversal(tree, right_node, lower_bound, result)

    return


class Node:
    def __init__(self, key, height, left_child, right_child, parent):
        self.key = key
        self.height = height
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent


class AVLTree:
    def __init__(self):
        self.tree = []
        self.root = 0
        self.length = 0

    def update_height(self, index):
        # Update the heights of all nodes along the path from a newly-added node to the tree root.
        while index is not None:
            node = self.tree[index]
            left_index = node.left_child
            right_index = node.right_child
            if left_index is None:
                left = 0
            else:
                left = self.tree[left_index].height
            if right_index is None:
                right = 0
            else:
                right = self.tree[right_index].height
            subtree_height = max(left, right)

            # If the addition of the new node doesn't change the height of the parent, return.
            if node.height == subtree_height + 1:
                return

            # Else, update the height of the parent and all other affected nodes.
            else:
                node.height = subtree_height + 1
                index = self.tree[index].parent
        return

    def calculate_height(self, node):
        # Find max of left and right subtrees of node. If max equals current node.height, return.
        # Else, call function again with node equal to the parent of the current node.
        if node.left_child is not None:
            left = self.tree[node.left_child].height
        else:
            left = 0
        if node.right_child is not None:
            right = self.tree[node.right_child].height
        else:
            right = 0
        height = max(left, right) + 1
        if height != node.height:
            node.height = height
            if node.parent is not None:
                self.calculate_height(self.tree[node.parent])
        return

    def rotate_right(self, index):
        # Index's left child takes the place of index, so update the parent of left to be the
        # parent of index, then update the parent's left or right child to point at left.
        left = self.tree[index].left_child
        parent = self.tree[index].parent

        if parent is not None:
            if self.tree[parent].left_child == index:
                self.tree[parent].left_child = left
            else:
                self.tree[parent].right_child = left

        # Index takes the place of right. Update left child of index to be the right child of left.
        # The parent of index is now left. The right child of left is now index. The parent of right becomes index.
        self.tree[index].parent = left
        self.tree[index].left_child = self.tree[left].right_child
        self.tree[left].parent = parent
        self.tree[left].right_child = index

        # Update tree.root if index equals root.
        if self.root == index:
            self.root = left

        self.calculate_height(self.tree[index])
        return

    def rotate_left(self, index):
        right = self.tree[index].right_child
        parent = self.tree[index].parent
        if parent is not None:
            if self.tree[parent].left_child == index:
                self.tree[parent].left_child = right
            else:
                self.tree[parent].right_child = right
        self.tree[right].parent = parent
        self.tree[index].parent = right
        self.tree[index].right_child = self.tree[right].left_child
        self.tree[right].left_child = index

        if index == self.root:
            self.root = right

        self.calculate_height(self.tree[index])
        return

    def rebalance_right(self, index):
        m = self.tree[index].left_child
        l = self.tree[m].left_child
        r = self.tree[m].right_child
        if l is not None:
            left_height = self.tree[l].height
        else:
            left_height = 0
        if r is not None:
            right_height = self.tree[r].height
        else:
            right_height = 0

        if right_height > left_height:
            self.rotate_left(m)
        self.rotate_right(index)
        return

    def rebalance_left(self, index):
        m = self.tree[index].right_child
        l = self.tree[m].left_child
        r = self.tree[m].right_child
        if l is not None:
            left_height = self.tree[l].height
        else:
            left_height = 0
        if r is not None:
            right_height = self.tree[r].height
        else:
            right_height = 0

        if left_height > right_height:
            self.rotate_right(m)
        self.rotate_left(index)
        return

    def rebalance(self, index):
        p = self.tree[index].parent
        left = self.tree[index].left_child
        right = self.tree[index].right_child
        if left is not None:
            left_height = self.tree[left].height
        else:
            left_height = 0
        if right is not None:
            right_height = self.tree[right].height
        else:
            right_height = 0

        if left_height > right_height + 1:
            self.rebalance_right(index)
        if right_height > left_height + 1:
            self.rebalance_left(index)

        if p is not None:
            self.rebalance(p)
        else:
            return

    def find(self, value, root, prior_sum):
        value = (value + prior_sum) % M

        # If the tree is empty, the new node belongs at index 0 and is the root.
        if self.length is 0:
            return 0

        # If value is found in the tree, return the index of the node with this key.
        elif self.tree[root].key == value:
            return root

        # If value is less than the key of the current subtree root, traverse the left subtree.
        elif self.tree[root].key > value:
            leftchild = self.tree[root].left_child
            if leftchild is not None and self.tree[leftchild].key is not None:
                return self.find(value, leftchild, prior_sum)
            return root

        # If value is greater than the key of the current subtree root, traverse the right subtree.
        elif self.tree[root].key < value:
            rightchild = self.tree[root].right_child
            if rightchild is not None and self.tree[rightchild].key is not None:
                return self.find(value, rightchild, prior_sum)
            return root

    def add_node(self, value, prior_sum):
        # Calculate the value to be added.
        updated_value = (value + prior_sum) % M

        # If the AVL tree is empty, the new node becomes the root.
        if self.length == 0:
            root_node = Node(key=updated_value, height=1, left_child=None, right_child=None, parent=None)
            self.tree.append(root_node)
            self.length += 1
            return

        # Find the position in the tree where the new node should be added
        # (or find the value in the tree if duplicate)
        index = self.find(value, self.root, prior_sum)

        # If AVL tree is not empty and the key of the node at the returned index does not match the
        # updated value to be added, add updated value as child of node at returned index.
        # If key of node at the returned index matches the value to be added, do nothing.
        if self.tree[index].key != updated_value:

            # If updated value is less than the key at self.tree[index], add the new node as a left child.
            if self.tree[index].key > updated_value:
                self.tree[index].left_child = len(self.tree)
                new_node = Node(key=updated_value, height=1, left_child=None, right_child=None, parent=index)
                self.tree.append(new_node)

                # Update heights of all nodes in lineage.
                self.update_height(index)

            # If updated value is greater than the key at self.tree[index], add the new node as a right child.
            if self.tree[index].key < updated_value:
                self.tree[index].right_child = len(self.tree)
                new_node = Node(key=updated_value, height=1, left_child=None, right_child=None, parent=index)
                self.tree.append(new_node)

                # Update heights of all nodes in lineage.
                self.update_height(index)
            self.length += 1

            # Rebalance the tree at the newly-added element.
            self.rebalance(len(self.tree) - 1)
        return

    def left_descendant(self, node_index):
        if self.tree[node_index].left_child is None:
            return node_index
        else:
            return self.left_descendant(self.tree[node_index].left_child)

    def right_ancestor(self, node_index):
        node_parent = self.tree[node_index].parent
        if self.tree[node_index].key < self.tree[node_parent].key:
            return node_parent
        else:
            return self.right_ancestor(node_parent)

    def next_node(self, node_index):
        if self.tree[node_index].right_child is not None:
            return self.left_descendant(self.tree[node_index].right_child)
        else:
            return self.right_ancestor(node_index)

    def delete_node(self, value, prior_sum):
        # If the tree is empty, return.
        if self.length == 0:
            return

        updated_value = (value + prior_sum) % M
        index = self.find(value, self.root, prior_sum)
        new_parent = self.tree[index].parent

        # If the value to be removed is not present in the tree, just return.
        if self.tree[index].key != updated_value:
            return

        # If there is only one node in the tree, just delete it.
        elif self.length == 1:
            self.tree.remove(self.tree[index])
            self.length -= 1
            return

        else:

            # If the node to be deleted has no right child, promote its left child.
            if self.tree[index].right_child is None:

                replacement = self.tree[index].left_child

                # If the node to be deleted has a left child but no right child, promote this left child by making
                # it the left or right child of the parent of the node to be deleted.
                if replacement is not None:

                    # Update the replacement node's parent to be the parent of the original node.
                    self.tree[replacement].parent = new_parent

                    # If the node to be deleted is itself a left child, promote the deleted node's left child to
                    # be the left child of the parent.
                    if new_parent is not None:
                        if self.tree[new_parent].left_child == index:
                            self.tree[new_parent].left_child = replacement

                            # Update the height of all nodes from the parent of the promoted node to the root.
                            self.calculate_height(self.tree[new_parent])

                        # If the node to be deleted is itself a right child, promote the deleted node's left child
                        # to be the right child of the parent.
                        else:
                            self.tree[new_parent].right_child = replacement

                            # update the height of all nodes from the parent of the promoted node to the root.
                            self.calculate_height(self.tree[new_parent])

                # If the node to be deleted doesn't have a left child or right child, update the new parent's
                # left or right pointer to none.
                elif new_parent is not None:
                    if self.tree[new_parent].left_child == index:
                        self.tree[new_parent].left_child = None
                    else:
                        self.tree[new_parent].right_child = None

                    # update the height of all nodes from the parent of the promoted node to the root.
                    self.calculate_height(self.tree[new_parent])

                # If the deleted node was the root, update tree.root.
                if index == self.root:
                    self.root = replacement

                # Rebalance the tree at index.
                self.rebalance(index)

            # If the node to be deleted has a right child (and the node may or may not have a left child)
            # promote the next largest element. Fix pointers relating to this next largest element.
            else:
                replace = self.next_node(index)
                replacement_parent = self.tree[replace].parent

                # Update the replacement node's parent to point to the parent of the deleted node.
                self.tree[replace].parent = self.tree[index].parent

                # If the replacement node has a right child (it will never have a left child), find the parent
                # of the replacement node and update its appropriate child to the right child of the replacement node.
                # Ensure the parent of the replacement node is not the node to be deleted!
                if replacement_parent != index:
                    if self.tree[replace].right_child is not None:
                        if self.tree[replacement_parent].left_child == replace:
                            self.tree[replacement_parent].left_child = self.tree[replace].right_child
                        elif self.tree[replacement_parent].right_child == replace:
                            self.tree[replacement_parent].right_child = self.tree[replace].right_child

                    # If the replacement node doesn't have a right child, update the appropriate child of the
                    # parent of the replacement node to None.
                    else:
                        if self.tree[replacement_parent].left_child == replace:
                            self.tree[replacement_parent].left_child = None
                        elif self.tree[replacement_parent].right_child == replace:
                            self.tree[replacement_parent].right_child = None

                # Now update the deleted node's parent to point at the replacement node and the replacement node to
                # point at the deleted node's right child (and left child if applicable).
                if new_parent is not None:
                    if self.tree[new_parent].left_child == index:
                        self.tree[new_parent].left_child = replace
                    else:
                        self.tree[new_parent].right_child = replace

                # If the right child of the deleted element is not the replacement element, set the right child of
                # the replacement element to equal the index of the right child of the deleted element.
                if self.tree[index].right_child != replace:
                    self.tree[replace].right_child = self.tree[index].right_child

                    # Set the parent of the right child of the deleted element to the index of the replacement element.
                    right = self.tree[index].right_child
                    self.tree[right].parent = replace

                # If the deleted element has a left child and that element is not the replacement element, set the
                # left child of the replacement element to equal the index of the left child of the deleted element.
                if self.tree[index].left_child is not None and self.tree[index].left_child != replace:
                    self.tree[replace].left_child = self.tree[index].left_child

                    # Set the parent of the left child of the deleted element to the index of the replacement element.
                    left = self.tree[index].left_child
                    self.tree[left].parent = replace

                else:
                    self.tree[replace].left_child = None

                # Update the heights of all nodes along the path from the replacement node to the root.
                if replacement_parent is not None:
                    self.calculate_height(self.tree[replace])

                # Rebalance the tree at replacement_parent.
                self.rebalance(replacement_parent)

            # If the deleted node was the root, update tree.root.
            if index == self.root:
                self.root = replace

            # Change all parameters of deleted node to None type.
            self.tree[index].parent = None
            self.tree[index].left_child = None
            self.tree[index].right_child = None
            self.tree[index].key = None
            self.tree[index].height = None

            # Update the length of the tree.
            self.length -= 1

    def range_sum(self, lower_bound, upper_bound, prior_sum):
        # If tree is empty, return 0.
        if self.length is 0:
            return 0

        # If the tree has only one element and that element falls within bounds, return that element. Else, return 0.
        if self.length is 1:
            indexofroot = self.root
            if lower_bound <= self.tree[indexofroot].key <= upper_bound:
                return self.tree[indexofroot].key
            else:
                return 0

        # Calculate the true upper and lower bounds for the range sum.
        updated_upper = (upper_bound + prior_sum) % M
        updated_lower = (lower_bound + prior_sum) % M

        # Find the index of either the node having key equal to updated_upper or the next largest element
        # if updated_upper is not in tree.
        upper = self.find(upper_bound, self.root, prior_sum)

        # Make a list to hold the results of the tree traversal.
        result_list = []

        # Check if updated upper bound has been found in tree. If so, add to result list.
        if updated_lower <= self.tree[upper].key <= updated_upper:
            result_list.append(updated_upper)

        # Get a list of all elements in left subtree of the upper bound.
        if self.tree[upper].left_child is not None:
            pre_order_traversal(self.tree, self.tree[upper].left_child, updated_lower, result_list)

        # Until the element is None, get a list of all elements in the left subtree of the element if the
        # parent.left_child is not the current element.
        original = upper
        upper = self.tree[upper].parent

        while upper is not None:
            if self.tree[upper].left_child != original and self.tree[upper].left_child is not None:
                pre_order_traversal(self.tree, self.tree[upper].left_child, updated_lower, result_list)
                if self.tree[upper].key >= updated_lower:
                    result_list.append(self.tree[upper].key)
            elif self.tree[upper].left_child != original:
                if self.tree[upper].key >= updated_lower:
                    result_list.append(self.tree[upper].key)
            original = upper
            upper = self.tree[upper].parent

        # Create a variable to hold the sum. Set to zero initially.
        summation = 0

        # Sum the values in result_list.
        for value in result_list:
            summation += value
        return summation


# Create an instance of the AVLTree class.
avl = AVLTree()

# Make a variable to hold the sum, which is increased with every call to range_sum.
current_sum = 0

for entry in avl.tree:
    print(entry.key, entry.left_child, entry.right_child, entry.parent, entry.height)


# Get input from infile.
with open(sys.argv[1]) as instructions:
    n = int(instructions.readline())

    for i in range(n):
        instruction = instructions.readline()
        first_space = instruction.find(" ")
        command = instruction[:first_space]
        backslashn = instruction.find("\n")

        if command is not "s":
            integer = int(instruction[first_space + 1:backslashn])

        if command == "+":
            avl.add_node(integer, current_sum)

        elif command == "-":
            avl.delete_node(integer, current_sum)

        elif command == "?":
            found = avl.find(integer, avl.root, current_sum)
            if len(avl.tree) != 0 and avl.tree[found].key == (integer + current_sum) % M:
                print("Found")
            else:
                print("Not found")

        elif command == "s":
            second_space = instruction.find(" ", first_space + 1)
            lower_int = int(instruction[first_space + 1:second_space])
            upper_int = int(instruction[second_space + 1:backslashn])

            new_sum = avl.range_sum(lower_int, upper_int, current_sum)
            print(new_sum)
            current_sum = new_sum
