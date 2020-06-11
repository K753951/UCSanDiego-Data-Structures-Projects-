import sys
import copy
import numpy as np


class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def push(self, next_package):
        self.frontier.append(next_package)

    def pop(self):
        if len(self.frontier) == 0:
            raise Exception("cannot remove package, empty frontier")
        else:
            removed_package = self.frontier[0]
            self.frontier = self.frontier[1:]
            return removed_package


def check_arrival(time, pkg_list):
    """ Returns a list of indexes for packages that arrived at a given time """
    return_list = []
    for i in range(len(pkg_list)):
        if pkg_list[i][0] == time:
            return_list.append(i)
    return return_list


def packages_missed(time, pkg_list):
    """ Returns the number of packages missed while processing the most recent package """
    for i in range(len(pkg_list)):
        if pkg_list[i][0] >= time: #TODO: fix this line
            return i
    return 0


# Check for proper usage.
if len(sys.argv) != 2:
    raise Exception("Usage error: python simulation.py filename")

# Open the list of incoming packets in read mode.
incoming = open(sys.argv[1], "r")

# Read first line of text file into a string.
stats = incoming.readline()

index = stats.find(" ")
S = int(stats[0:index])
n = int(stats[index:])

# Check if constraints have been met.
if S < 1 or S > 100000:
    raise Exception('Invalid buffer size')
if n < 0 or n > 100000:
    raise Exception('Invalid number of packages')

# Close file.
incoming.close()

# Make a 2D array to hold packages.
packages = []

# Create new file pointer to read incoming packets.
with open(sys.argv[1], "r") as incoming2:

    # Skip the first line.
    incoming2.readline()

    # Read file line by line into the packages 2D array.
    valid_set = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\n'}
    for i in range(n):
        line = incoming2.readline()
        temp = []
        for num in line:
            if num not in valid_set:
                raise Exception("Invalid numerical input")
        x = line.find(' ')
        A = int(line[0:x])
        if A < 0 or A > 1000000:
            raise Exception("Invalid input A")
        P = int(line[x:])
        if P < 0 or P > 1000:
            raise Exception("Invalid input P")
        temp.append(A)
        temp.append(P)
        packages.append(copy.deepcopy(temp))
        temp.clear()

# Make a buffer to hold incoming packets and a timer to keep track of time.
buffer = QueueFrontier()
timer = 0

# Make a one-dimensional array to hold output and initialize all entries to -1.
output = np.full(n, -1)

# Make a QueueFrontier to hold packages.
queue = QueueFrontier()

# Initially, append an index number to all packages and add all package entries to Queue.
for i in range(len(packages)):
    packages[i].append(i)
    queue.push(packages[i])

while len(queue.frontier) is not 0 or len(buffer.frontier) is not 0:

    # Make a counter to hold number of packages to be popped from queue.
    pop_counter = 0

    # Check for incoming packages in queue.
    packages_in = check_arrival(timer, queue.frontier)
    pop_counter += len(packages_in)

    # Add incoming packages to buffer if buffer is not full.
    packages_left = len(packages_in)
    for i in range(len(packages_in)):
        if len(buffer.frontier) is not S and packages_left is not 0:
            buffer.push(copy.deepcopy(queue.frontier[i]))
            packages_left -= 1

    # Check for missed incoming packages.
    missed = packages_missed(timer, queue.frontier)
    pop_counter += missed

    # Remove packages added to buffer, packages that overflowed buffer, and missed packages from queue.
    for i in range(pop_counter):
        queue.pop()

    # Process oldest package in buffer if buffer contains packages.
    if len(buffer.frontier) is not 0:
        in_process = buffer.pop()
        output[in_process[2]] = timer

        # Increment timer
        timer = timer + in_process[1]

    # If buffer is empty, increment timer by one.
    else:
        timer += 1

for line in output:
    print(line)




