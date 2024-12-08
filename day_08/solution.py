from collections import defaultdict

# %% Load data

use_test = False
test_path = "test1.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()

"""
Input looks like:
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


# Parse input to find all unique characters & their positions
char_rc_dict = defaultdict(list)
for row_idx, line in enumerate(lines):

    for col_idx, char in enumerate(line):

        is_antenna = char.isalnum()
        if is_antenna:
            char_row_col = (row_idx, col_idx)
            char_rc_dict[char].append(char_row_col)
    pass


# Get row/column boundaries for checking out-of-bounds indexing
min_row, min_col = 0, 0
max_row, max_col = len(lines) - 1, len(lines[0]) - 1
is_in_bounds = lambda rowcol: (min_row <= rowcol[0] <= max_row) and (min_col <= rowcol[1] <= max_col)


# %% Part 1

all_antinodes_list = []
for char, row_col_list in char_rc_dict.items():

    # For each row/col position, calculate distance to other entries to find antinodes
    num_ants = len(row_col_list)
    for ant_idx in range(max(num_ants - 1, 0)):
        root_row, root_col = row_col_list[ant_idx]
        rc_diffs = [(root_row - oth_row, root_col - oth_col) for oth_row, oth_col in row_col_list[(1 + ant_idx) :]]

        # Calculate both anti-nodes between each pair (root & other antenna)
        # -> Anti-node 1 is the one closest to the root antenna
        # -> Anti-node 2 is closest to other antenna (requires doubling diff to 'step past' other antenna!)
        antinodes_1 = [(root_row + r_diff, root_col + c_diff) for r_diff, c_diff in rc_diffs]
        antinodes_2 = [(root_row - 2 * r_diff, root_col - 2 * c_diff) for r_diff, c_diff in rc_diffs]

        # Add to total listing
        all_antinodes_list.extend(antinodes_1)
        all_antinodes_list.extend(antinodes_2)

    pass

# Remove anti-nodes that are out-of-bounds
inbounds_antinodes = [rowcol for rowcol in all_antinodes_list if is_in_bounds(rowcol)]
unique_inbounds_antinodes = set(inbounds_antinodes)

print("Part 1:", len(unique_inbounds_antinodes))


# %% Part 2

# Can't use approach from part 1, instead need to iteratively find antinode until we go out of bounds

part2_antinodes_list = []
for char, row_col_list in char_rc_dict.items():

    num_ants = len(row_col_list)
    for ant_idx in range(max(num_ants - 1, 0)):
        root_row, root_col = row_col_list[ant_idx]
        rc_diffs = [(root_row - oth_row, root_col - oth_col) for oth_row, oth_col in row_col_list[(1 + ant_idx) :]]

        # Find 'backwards' facing antinodes (i.e. closest to root antenna)
        antinodes_1 = []
        for r_diff, c_diff in rc_diffs:
            for step_idx in range(1, 1_000_000):
                next_r = root_row + r_diff * step_idx
                next_c = root_col + c_diff * step_idx
                if not is_in_bounds((next_r, next_c)):
                    break
                antinodes_1.append((next_r, next_c))

        # Find forwards-facing antinodes (i.e. closest to 'other' antenna)
        antinodes_2 = []
        for r_diff, c_diff in rc_diffs:
            oth_row = root_row - r_diff
            oth_col = root_col - c_diff
            for step_idx in range(1, 1_000_000):
                next_r = oth_row - r_diff * step_idx
                next_c = oth_col - c_diff * step_idx
                if not is_in_bounds((next_r, next_c)):
                    break
                antinodes_2.append((next_r, next_c))

        # Add to total listing
        part2_antinodes_list.extend(antinodes_1)
        part2_antinodes_list.extend(antinodes_2)

    # Add antenna position as antinodes, as long as there are at least 2 antennas
    antinodes_3 = []
    if num_ants > 1:
        antinodes_3 = row_col_list
    part2_antinodes_list.extend(antinodes_3)

# Exclude duplicates before counting!
part2_unique_antinodes = set(part2_antinodes_list)
print("Part 2:", len(part2_unique_antinodes))
