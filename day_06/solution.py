from collections import defaultdict

# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()


# %% Pre-processing

# Find starting point & direction
start_rc_dir = (0, 0)
start_rc = (None, None)
for row_idx, l in enumerate(lines):
    if "v" in l:
        start_rc_dir = (1, 0)
        start_rc = (row_idx, l.index("v"))
        break
    if "^" in l:
        start_rc_dir = (-1, 0)
        start_rc = (row_idx, l.index("^"))
        break
    if ">" in l:
        start_rc_dir = (0, 1)
        start_rc = (row_idx, l.index(">"))
        break
    if "<" in l:
        start_rc_dir = (-1, 0)
        start_rc = (row_idx, l.index("<"))
        break
    pass


# Find locations of blockers on every row/column
blockers_col_idx_per_row_dict = {}
blockers_row_idx_per_col_dict = defaultdict(list)
for row_idx, l in enumerate(lines):

    # Skip rows without blockers
    if "#" not in l:
        continue

    # Get column index of every '#' on the row (and record row index for corresponding column!)
    col_idx_on_row_list = []
    parse_start = 0
    while "#" in l[parse_start:]:
        col_idx = l.find("#", parse_start)
        col_idx_on_row_list.append(col_idx)
        blockers_row_idx_per_col_dict[col_idx].append(row_idx)
        parse_start = col_idx + 1

    # Store all col indices for the given row
    blockers_col_idx_per_row_dict[row_idx] = col_idx_on_row_list

# Record largest row/column index (for out-of-bounds indexing), assuming rectangular area
max_row = len(lines[0]) - 1
max_col = len(lines) - 1


# %% Part 1

# Helper used to rotate direction 90deg clockwise
rot_dir_90cw = lambda rdir, cdir: (cdir, -rdir)

curr_rdir, curr_cdir = start_rc_dir
curr_row, curr_col = start_rc
visited_row_cols = [start_rc]
while True:

    is_moving_vertically = curr_rdir != 0
    if is_moving_vertically:
        blocker_idxs = blockers_row_idx_per_col_dict[curr_col]
        inserted_idx_list = sorted([*blocker_idxs, curr_row])
        target_blocker_list_idx = inserted_idx_list.index(curr_row) + curr_rdir

        # If we can't get a blocker index, we've walked off the map
        if target_blocker_list_idx < 0:
            last_row = 0
            last_col = curr_col
            visited_row_cols.append((last_row, last_col))
            break
        elif target_blocker_list_idx > len(inserted_idx_list) - 1:
            last_row = max_row
            last_col = curr_col
            visited_row_cols.append((last_row, last_col))
            break

        new_row_idx = inserted_idx_list[target_blocker_list_idx] - curr_rdir
        new_col_idx = curr_col

    else:
        blocker_idxs = blockers_col_idx_per_row_dict[curr_row]
        inserted_idx_list = sorted([*blocker_idxs, curr_col])
        target_blocker_list_idx = inserted_idx_list.index(curr_col) + curr_cdir

        # If we can't get a blocker index, we've walked off the map
        if target_blocker_list_idx < 0:
            last_row = curr_row
            last_col = 0
            visited_row_cols.append((last_row, last_col))
            break
        elif target_blocker_list_idx > len(inserted_idx_list) - 1:
            last_row = curr_row
            last_col = max_col
            visited_row_cols.append((last_row, last_col))
            break

        new_row_idx = curr_row
        new_col_idx = inserted_idx_list[target_blocker_list_idx] - curr_cdir

    curr_row, curr_col = (new_row_idx, new_col_idx)
    curr_rdir, curr_cdir = rot_dir_90cw(curr_rdir, curr_cdir)

    visited_row_cols.append((curr_row, curr_col))

# We have all stopping/turning points, now need to 'connect' them to find all visited points
binary_grid = []
for _ in range(max_row + 1):
    new_row = [0 for _ in range(max_col + 1)]
    binary_grid.append(new_row)
for (row_a, col_a), (row_b, col_b) in zip(visited_row_cols[:-1], visited_row_cols[1:]):

    row_dir = 1 if row_b + 1 > row_a else -1
    col_dir = 1 if col_b + 1 > col_a else -1
    for row_idx in range(row_a, row_b + row_dir, row_dir):
        for col_idx in range(col_a, col_b + col_dir, col_dir):
            binary_grid[row_idx][col_idx] = 1

    pass

print("Part 1:", sum(sum(row) for row in binary_grid))


# %% Part 2

print("Part 2:", None)
