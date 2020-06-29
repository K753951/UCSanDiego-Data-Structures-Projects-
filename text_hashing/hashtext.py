import numpy as np
import sys


class HashTable:
    def __init__(self, m):
        self.table = np.empty(m, list)
        for i in range(m):
            self.table[i] = []

    def hash(self, word, m):
        h = 0
        for i in range(len(word)):
            h += ord(word[i]) * (263 ** i)
        h = h % 1000000007
        h = h % m
        return h

    def add(self, word, m):
        h = self.hash(word, m)
        if word in self.table[h]:
            return
        self.table[h].insert(0, word)

    def delete(self, word, m):
        h = self.hash(word, m)
        if word in self.table[h]:
            self.table[h].remove(word)

    def find(self, word, m):
        h = self.hash(word, m)
        if word in self.table[h]:
            return 'yes'
        return 'no'

    def check(self, i):
        if len(self.table[i]) is not 0:
            output = " ".join(self.table[i])
            return output
        return "\n"


def get_text(s):
    """ Returns the second word in a string of text """
    firstspace = s.find(' ')
    newline = s.find('\n')
    text = s[firstspace + 1:newline]
    for character in text:
        if character < 'A' or 'Z' < character < 'a' or character > 'z':
            if character != "\0":
                raise Exception("Invalid name")
    if len(text) > 15:
        raise Exception("Invalid text input")
    return text


# Make a list to hold query strings.
queries = []


# Open input file in read mode.
with open(sys.argv[1]) as infile:

    # Obtain number of buckets from first line.
    first_line = infile.readline()
    global M
    M = int(first_line)

    # Obtain number of queries from second line.
    second_line = infile.readline()
    global N
    N = int(second_line)

    # Check that N is within acceptable range.
    if N < 1 or N > 100000:
        raise Exception("Invalid number of queries")

    # Check that M is within acceptable range.
    if M < N/5 or M > N:
        raise Exception("Invalid number of buckets")

    # Now read the queries into an array of strings.
    for i in range(N):
        queries.append(infile.readline())

# Make an instance of the HashTable class.
HT = HashTable(M)

# For each input query, convert to instruction format, then implement that instruction.
# Begin by finding function name.
for query in queries:
    first_space = query.find(' ')
    function = query[:first_space]

    if function == "add":
        new_string = get_text(query)
        HT.add(new_string, M)

    if function == "del":
        new_string = get_text(query)
        HT.delete(new_string, M)

    if function == "find":
        new_string = get_text(query)
        print(HT.find(new_string, M))

    if function == "check":
        new_line = query.find('\n')
        index = int(query[first_space + 1:new_line])
        print(HT.check(index))
