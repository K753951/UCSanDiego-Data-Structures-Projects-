import sys


class Table:
    """ Table objects store the number of rows in a table (rank) and an optional link to another table. """
    def __init__(self, rank, link, index):
        self.rank = rank
        self.link = link
        self.index = index


class DisjointSet:
    """ Data structure that can support creation of singleton sets, returning ID of set containing a
    certain element, an merging of two sets. """
    def __init__(self):
        self.sets = []

    def make_set(self, rank, link, index):
        new = Table(rank=rank, link=link, index=index)
        self.sets.append(new)

    def find(self, a, path_compression):
        # Add index a to list of elements to path-compress.
        path_compression.append(a)

        # If list head has been reached, set .link of all lists along the path to point at list head
        # (compress the path)
        if self.sets[a].link is None:
            for p in path_compression:

                # First must check that index of element to be compressed is not equal to list head itself.
                if a != p:
                    self.sets[p].link = a

            # Clear the path_compression buffer for next call to Find.
            path_compression.clear()

            # Return the zero-based index number of the list head.
            return a

        # If head of list not yet reached, update index a to index of parent and recursively call function.
        else:
            a = self.sets[a].link
            return self.find(a, path_compression)

    def merge(self, d, s):
        # If d and s point to the same list, return the length of that list.
        if d == s:
            return self.sets[d].rank

        # Otherwise, add the ranks of the lists to be merged and store total list length in destination.
        else:
            self.sets[d].rank = self.sets[d].rank + self.sets[s].rank
            self.sets[s].rank = 0
            self.sets[s].link = d
            return self.sets[d].rank


def convert_to_int(s):
    """ Converts a line of characters from a text file to a list of ints and returns this list. """

    # Make a temporary list to hold digits of input numbers.
    temp = []

    # Make a list to hold return values.
    return_list = []

    # Gather digits from input string.
    for i in range(len(s)):
        if '0' <= s[i] <= '9':
            temp.append(s[i])
        if s[i] == ' ' or i == len(s) - 1:
            return_list.append(int("".join(temp)))
            temp.clear()
    return return_list


# Read data from text file.
with open(sys.argv[1]) as infile:
    infile_mn = infile.readline()
    infile_rows = infile.readline()

    # Create lists to hold data from text file.
    global m_and_n
    global rows
    global merge
    merge = []

    # Convert first line of infile into ints m and n stored in list form.
    m_and_n = convert_to_int(infile_mn)

    # Parse m and n. Check if inputs valid.
    n = m_and_n[0]
    if n < 1 or n > 100000:
        raise Exception("Invalid number of tables in database.")

    m = m_and_n[1]
    if m < 1 or m > 100000:
        raise Exception("Invalid number of merge operations.")

    # Gather number of rows per table from infile.
    rows = convert_to_int(infile_rows)

    # Check that all inputs into the rows list are valid.
    for row in rows:
        if row < 0 or row > 10000:
            raise Exception("Invalid number of rows per table.")

    # Gather merge operation data.
    for i in range(m):
        infile_merge = infile.readline()
        merge.append(convert_to_int(infile_merge))

# Correct merge list data for zero-based indexing.
for i in range(m):
    merge[i][0] -= 1
    merge[i][1] -= 1

# Create a DisjointSet object to store all input tables.
master = DisjointSet()

# Add tables to master.
for i in range(len(rows)):
    master.make_set(rank=rows[i], link=None, index=i)

# Make a buffer to hold path_compression indexes for find function.
buffer = []

# Merge tables according to merge list. Find length of table resulting from the merge.
for action in merge:
    true_d = master.find(action[0], buffer)
    true_s = master.find(action[1], buffer)

    master.merge(true_d, true_s)

    maximum = []

    # Find maximum list length:
    for i in range(len(rows)):
        parent = master.find(i, buffer)
        maximum.append(master.sets[parent].rank)
    print(max(maximum))

    # Clear maximum for next iteration.
    maximum.clear()


