import sys


class PriorityQueue:
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


class Thread:
    def __init__(self, free, end_time):
        self.free = free
        self.end_time = end_time


# Create a list to hold values m and n. Create a second list to hold input values (job processing times).
mandn = []
input = []

# Open input file and read first and second lines into buffers.
with open(sys.argv[1]) as file:
    first_line = file.readline()
    second_line = file.readline()

    # Create a temp variable to hold individual digits of input numbers.
    temp = []

    # Convert m and n variables from strings to ints.
    for i in range(len(first_line)):
        if '0' <= first_line[i] <= '9':
            temp.append(first_line[i])
        if first_line[i] == ' ' or i == len(first_line) - 1:
            number = int("".join(temp))
            mandn.append(number)
            temp.clear()

    # Convert inputs (job processing times) from strings to ints.
    for i in range(len(second_line)):
        if '0' <= second_line[i] <= '9':
            temp.append(second_line[i])
        if second_line[i] == ' ' or i == len(second_line) - 1:
            number2 = int("".join(temp))
            input.append(number2)
            temp.clear()

# Parse m and n. Check if both are valid.
n = mandn[0]
if n < 1 or n > 100000:
    raise Exception("invalid number of threads")

m = mandn[1]
if m < 1 or m > 100000:
    raise Exception("invalid number of jobs")

# Check to see if any inputs invalid.
for num in input:
    if num < 0 or num > 1000000000:
        raise Exception("invalid processing time")

# Add elements from input list to a PriorityQueue.
PQ = PriorityQueue()
for num in input:
    PQ.insert(num)

# Make a list and populate with n thread objects.
threads = []
for i in range(n):
    new = Thread(free=True, end_time=0)
    threads.append(new)

# Make a timer and an array to hold output.
output = []
timer = 0

while len(PQ.queue) != 0:

    # Update thread status based on current timer.
    for thread in threads:
        if not thread.free:
            if timer == thread.end_time:
                thread.free = True

    # While there are some unoccupied threads, use free threads to process jobs from PQ.
    for i in range(len(threads)):
        if threads[i].free:
            job = PQ.extract()
            threads[i].free = False
            threads[i].end_time = timer + job
            out = [i, timer]
            output.append(out)

    timer += 1

# Print output in desired format.
for line in output:
    print(line[0], " ", line[1])