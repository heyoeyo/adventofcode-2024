# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()


# %% Part 1

# Convert each line of text into list of integers
levels_list = [list(map(int, l.split(" "))) for l in lines]

# Compute consecutive differences (e.g. for [1,3,5,2] we get: [2, 2, -3])
# -> Note, the differences are always 1 element shorted than the original list!!!
diffs = []
for l in levels_list:
    level_diff = [a - b for a, b in zip(l[1:], l[:-1])]
    diffs.append(level_diff)

# Check conditions for part 1 question
safe_levels_part_1 = []
for level_diff in diffs:

    is_ascending = all(d > 0 for d in level_diff)
    is_descending = all(d < 0 for d in level_diff)
    is_slow = all(abs(d) <= 3 for d in level_diff)

    is_safe = (is_ascending or is_descending) and is_slow
    safe_levels_part_1.append(is_safe)

print("Part 1:", sum(safe_levels_part_1))


# %% Part 2

# For each level, flag all entries that might be problematic
# -> Problem if not matching ascending/descending pattern or changing too fast
is_unfixable_list = []
problem_idxs_list = []
for level, level_diff in zip(levels_list, diffs):

    # Assume all level entries are not problematic
    is_problem_value = [False for _ in level]
    bad_idx = []

    # Check for cases where the level is definitely no good
    num_ascending = sum(d > 0 for d in level_diff)
    num_descending = sum(d < 0 for d in level_diff)
    num_fast = sum(abs(d) > 3 for d in level_diff)

    # Flag as unsafe and skip further checks
    max_allowed = len(level_diff) - 1
    is_unsafe = (num_ascending < max_allowed and num_descending < max_allowed) or num_fast > 1
    is_unfixable_list.append(is_unsafe)
    if is_unsafe:
        problem_idxs_list.append(None)
        continue

    # Check for entries that are not matching ascending/descending pattern
    if num_ascending == len(level_diff) - 1:
        bad_idx = [idx for idx, d in enumerate(level_diff) if d <= 0]

    elif num_descending == len(level_diff) - 1:
        bad_idx = [idx for idx, d in enumerate(level_diff) if d >= 0]

    # Check for entries that are 'too fast'
    is_too_fast = [idx for idx, d in enumerate(level_diff) if abs(d) > 3]
    bad_idx.extend(is_too_fast)

    # Flag bad entries (based on ascend/descend requirements)
    # -> Need to flag 'left & right' values, since removing either might help!
    problem_idx_per_level = set()
    for idx in bad_idx:
        problem_idx_per_level.add(idx)
        problem_idx_per_level.add(idx + 1)
    problem_idxs_list.append(problem_idx_per_level)

# For each level, try removing each problematic entry (one-by-one) and see if level becomes safe
safe_levels_part_2 = []
for level, problem_idx_per_level, is_unfixable in zip(levels_list, problem_idxs_list, is_unfixable_list):

    # Skip checks on bad levels
    if is_unfixable:
        safe_levels_part_2.append(False)
        continue

    # For levels with problems, see if removing 1 entry fixes things
    is_safe = True
    for bad_idx in problem_idx_per_level:
        mod_level = [val for idx, val in enumerate(level) if idx != bad_idx]
        mod_diff = [a - b for a, b in zip(mod_level[1:], mod_level[:-1])]
        is_ascending = all(d > 0 for d in mod_diff)
        is_descending = all(d < 0 for d in mod_diff)
        is_slow = all(abs(d) <= 3 for d in mod_diff)

        is_safe = (is_ascending or is_descending) and is_slow
        if is_safe:
            break
        pass

    safe_levels_part_2.append(is_safe)

print("Part 2:", sum(safe_levels_part_2))
