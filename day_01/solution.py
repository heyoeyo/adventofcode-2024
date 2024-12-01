# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()


# %% Part 1

# Separate left/right strings, interpretted as integers
left_lines, right_lines = zip(*[map(int, l.split("   ")) for l in lines])

# Calculate per-row differences as given by question
left_sorted = sorted(left_lines)
right_sorted = sorted(right_lines)
diffs = [abs(left - right) for left, right in zip(left_sorted, right_sorted)]

print("Part 1:", sum(diffs))


# %% Part 2

from collections import Counter

# Python has built-in object for exactly handling part 2...
left_counts = Counter(left_lines)
right_counts = Counter(right_lines)
similarities = [l_id * right_counts[l_id] * l_count for l_id, l_count in left_counts.items()]

print("Part 2:", sum(similarities))
