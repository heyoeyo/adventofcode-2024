# %% Load data

use_test = False
test_path = "test2.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()

# Find all starting points (i.e. coords of all 0's)
starting_row_cols = []
for row_idx, line in enumerate(lines):
    parse_start = 0
    num_zeros = line.count("0")
    for k in range(num_zeros):
        col_idx = line.index("0", parse_start)
        parse_start = col_idx + 1
        starting_row_cols.append((row_idx, col_idx))

# Convert lines to integers for easier comparisons
lines_int = [list(map(int, line)) for line in lines]
min_row_idx, max_row_idx = 0, len(lines_int) - 1
min_col_idx, max_col_idx = 0, len(lines_int[0]) - 1


# %% Part 1

end_points_per_start_point = {start_rc: [] for start_rc in starting_row_cols}
for row_start, col_start in starting_row_cols:

    # Initialize a (expected to grow) queue of 'all' known points to search
    prev_row_idx, next_col_idx = 0, 0
    all_search_rc_queue = [(row_start, col_start, prev_row_idx, next_col_idx)]

    while len(all_search_rc_queue) > 0:

        # For convenience, unpack current search point data
        search_row_idx, search_col_idx, prev_row_idx, prev_col_idx = all_search_rc_queue.pop()
        search_val = lines_int[search_row_idx][search_col_idx]

        # Get surrounding row/column indexing, with clamping to avoid out-of-bounds indexing
        u_row_idx, l_col_idx = max(search_row_idx - 1, min_row_idx), max(search_col_idx - 1, min_col_idx)
        d_row_idx, r_col_idx = min(search_row_idx + 1, max_row_idx), min(search_col_idx + 1, max_col_idx)

        # Form all possible neighbour row/column indices
        up_row_col = (u_row_idx, search_col_idx)
        down_row_col = (d_row_idx, search_col_idx)
        left_row_col = (search_row_idx, l_col_idx)
        right_row_col = (search_row_idx, r_col_idx)

        for next_row_idx, next_col_idx in (up_row_col, down_row_col, left_row_col, right_row_col):

            # Ignore previously visited locations
            is_prev_search_idx = (next_row_idx == prev_row_idx) and (next_col_idx == prev_col_idx)
            if is_prev_search_idx:
                continue

            # Decide what to do with the next step point
            next_val = lines_int[next_row_idx][next_col_idx]
            is_valid_step = (next_val - search_val) == 1
            if is_valid_step:

                # If we hit an end point, record it for the associated starting point
                if next_val == 9:
                    end_points_per_start_point[(row_start, col_start)].append((next_row_idx, next_col_idx))
                else:
                    # If we don't reach an end point, add new point (and prev point) to search queue
                    all_search_rc_queue.append((next_row_idx, next_col_idx, search_row_idx, search_col_idx))
            pass
        pass
    pass

# Each start point tends to have many pathes leading to the same end point, so only count unique start-end pairing!
unique_end_rc_per_start = {start_rc: set(end_rc_list) for start_rc, end_rc_list in end_points_per_start_point.items()}
scores_per_trailhead = {start_rc: len(end_rc_set) for start_rc, end_rc_set in unique_end_rc_per_start.items()}
print("Part 1:", sum(scores_per_trailhead.values()))


# %% Part 2

# Already have the solution from part 1! Just need to count it differently
print("Part 2:", sum(len(values) for values in end_points_per_start_point.values()))
