import sys
import numpy as np


def poly_hash(p, prime, x):
    h_value = 0
    for i in range(len(p)):
        h_value = h_value + ord(p[i]) * (x ** i)
    h_value = h_value % prime
    return h_value


def precompute_hashes(t, length_p, prime, x):
    # Get length of t.
    length_t = len(t)

    # Make an empty array to hold precomputed hashes.
    h = np.empty(length_t - length_p + 1, dtype=np.longlong)

    # Initialize S to last substring of t.
    s = t[length_t - length_p:length_t]

    # Hash S.
    h[length_t - length_p] = poly_hash(s, prime, x)

    # Compute x to the power of length_p modulo prime.
    y = x ** length_p

    # Use recurrence equation to precompute hashes.
    for i in range(length_t - length_p - 1, -1, -1):
        h[i] = int((x * h[i + 1] + ord(t[i])) - (y * ord(t[i + length_p]))) % prime

    # Return the list of precomputed hashes.
    return h


def rabin_karp(t, p):
    prime = 1000000007
    x = 263
    positions = []
    p_hash = poly_hash(p, prime, x)
    hashes = precompute_hashes(t, len(p), prime, x)
    for i in range(len(t) - len(p) + 1):
        if p_hash != hashes[i]:
            continue
        if t[i:i + len(p)] == p:
            positions.append(i)
    return positions


# Open input file and extract strings P and T.
with open(sys.argv[1]) as input_file:
    global P
    global T
    P = input_file.readline()
    T = input_file.readline()

    # Remove \n from both strings.
    P = P[:len(P) - 1]
    T = T[:len(T) - 1]

# Print output of rabin karp algorithm.
print(rabin_karp(T, P))
