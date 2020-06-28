import numpy as np
import sys


class Entry:
    def __init__(self, name, number):
        self.name = name
        self.number = number


class HashTable:
    def __init__(self):
        self.hash_table = np.empty(1000, list)

    def hash(self, number):
        h = (((365 * number) + 15) % 1949) % 1000
        return h

    def add(self, number, name):
        person = Entry(name=name, number=number)
        h = self.hash(number)
        if self.hash_table[h] is None:
            self.hash_table[h] = []
            self.hash_table[h].append(person)
            return
        elif self.hash_table[h] is not None:
            for entry in self.hash_table[h]:
                if entry.number == number:
                    entry.name = name
                    return
            self.hash_table[h].append(person)
            return

    def delete(self, number):
        h = self.hash(number)
        if self.hash_table[h] is not None:
            for entry in self.hash_table[h]:
                if entry.number == number:
                    self.hash_table[h].remove(entry)

    def find(self, number):
        h = self.hash(number)
        if self.hash_table[h] is not None:
            for entry in self.hash_table[h]:
                if entry.number == number:
                    return entry.name
        return "not found"


# Make a list to hold query strings.
queries = []

# Make an instance of the HashTable class.
HT = HashTable()

# Make a list to hold output.
output = []

# Open input file in read mode.
with open(sys.argv[1]) as infile:

    # Obtain number of queries from first line.
    first_line = infile.readline()
    global N
    N = int(first_line)

    # Check that N follows acceptable parameters.
    if N < 1 or N > 100000:
        raise Exception("Invalid number of queries")

    # Now read the queries into an array of strings.
    for i in range(N):
        queries.append(infile.readline())

# For each input query, convert to instruction format.
# Begin by finding function name.
for query in queries:
    first_space = query.find(' ')
    function = query[:first_space]

    if function == "add":
        second_space = query.find(' ', first_space + 1)
        Number = int(query[first_space + 1:second_space])
        if Number > 10000000:
            raise Exception("Invalid phone number")
        newline = query.find('\n')
        Name = query[second_space + 1:newline]
        for character in Name:
            if character < 'A' or 'Z' < character < 'a' or character > 'z':
                if character != "\0":
                    raise Exception("Invalid name")
        if len(Name) > 15:
            raise Exception("Invalid name")
        HT.add(Number, Name)

    if function == "del":
        Number = int(query[first_space + 1:])
        if Number > 10000000:
            raise Exception("Invalid phone number")
        HT.delete(Number)

    if function == "find":
        Number = int(query[first_space + 1:])
        if Number > 10000000:
            raise Exception("Invalid phone number")
        output.append(HT.find(Number))

for x in output:
    print(x)
