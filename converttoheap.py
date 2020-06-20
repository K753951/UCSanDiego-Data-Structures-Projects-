import sys


def left_child(i):
    """ Returns the index of the left child of the element at index i. """
    return 2 * i + 1


def right_child(i):
    """ Returns the index of the right child of the element at index i. """
    return (2 * i) + 2


def swap(initial_list, i, j):
    """ Swaps elements of initial_list found at indexes i and j. """
    temp = initial_list[i]
    initial_list[i] = initial_list[j]
    initial_list[j] = temp
    print(i, j)


def sift_down(initial_list, i):
    """ Moves the element found at index i of initial_list until heap properties satisfied. """
    min_index = i
    r = right_child(i)
    if r < len(initial_list) and initial_list[r] < initial_list[min_index]:
        min_index = r
    l = left_child(i)
    if l < len(initial_list) and initial_list[l] < initial_list[min_index]:
        min_index = l
    if i != min_index:
        swap(initial_list, i, min_index)
        sift_down(initial_list, min_index)


def build_heap(initial_list):
    """ Builds a heap from an array. """
    for i in range(len(initial_list) // 2, -1, -1):
        sift_down(initial_list, i)


# Open the input file as "file".
with open(sys.argv[1], "r") as file:
    n = int(file.readline())
    if n < 1 or n > 100000:
        raise Exception("Input size exceeds max capacity.")
    global num_array
    num_array = file.readline()

# Temp list holds digits of a single input number.
# Original list holds original input numbers in list form.
temp = []
original = []

# Iterate over second line of file (containing input numbers) and store in original list.
for i in range(len(num_array)):
    if "9" >= num_array[i] >= "0":
        temp.append(num_array[i])
    if num_array[i] == " " or i == len(num_array) - 1:
        number = int("".join(temp))
        if number > 1000000000 or number in original:
            raise Exception("Invalid Input")
        else:
            original.append(number)
        temp.clear()

# Build the heap.
build_heap(original)


