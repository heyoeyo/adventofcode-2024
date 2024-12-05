from collections import defaultdict

# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()

# Split raw input into 'page order' & 'updates' sections for separate parsing
txt_page_order, txt_updates = puzzle_txt.split("\n\n")
lines_page_order = txt_page_order.splitlines()
lines_updates = txt_updates.splitlines()

# Form dictionary of L: set(R1, R2, R3, ...)
# For encoding the L|R 'page ordering rules'
page_order_lut = defaultdict(set)
for each_order_line in lines_page_order:
    left_number, right_number = [int(value) for value in each_order_line.split("|")]
    page_order_lut[left_number].add(right_number)


# %% Part 1

# For each update, iterate backwards over each value one-by-one
# and check the 'set intersection' between all values prior
# to the current value and the page order set for that value
# -> Page order lists all values that must come *after* the target value
# -> Any intersection with values *before* implies a bad ordering
good_updates_list, bad_updates_list = [], []
for each_update_line in lines_updates:
    update_ints = [int(value) for value in each_update_line.split(",")]
    num_update_values = len(update_ints)

    # Iterate over update listing in reverse, looking for order vs. prior intersections
    is_order_mismatch = False
    for idx in range(1, num_update_values):

        # Get 'last-most' target value & set of values prior to the target
        target_val = update_ints[-idx]
        prior_to_target_set = set(update_ints[0:-idx])

        # Check if any numbers prior to target are part of targets 'after' ordering set
        target_order_set: set = page_order_lut[target_val]
        is_order_mismatch = not target_order_set.isdisjoint(prior_to_target_set)
        if is_order_mismatch:
            break

    # Store 'good' and 'bad' updates separately (need good ones for part 1, bad ones for part 2)
    if is_order_mismatch:
        bad_updates_list.append(update_ints)
    else:
        good_updates_list.append(update_ints)

    pass

# Find middle numbers of good updates
middle_values_list = []
for good_update in good_updates_list:
    middle_update_value = good_update[len(good_update) // 2]
    middle_values_list.append(middle_update_value)

print("Part 1:", sum(middle_values_list))


# %% Part 2

# To get corrected ordering, we can do something similar to part 1. Idea is:
# 1. Find last-most value in the update that we haven't already checked
# 2. Get intersection of page ordering for last-most value and prior values in update list
# 3. From the intersection values, find the one earliest in the update list
# 4. Move the last-most value from the 'end' of the update list to an index before the earliest intersection point
# 5. Mark the value as 'already checked'
# 6. Repeat steps 1-5 until we've checked all values. This should force the correct sorting order!

corrected_updates_list = []
for bad_update in bad_updates_list:

    # Perform sorting loop
    num_values = len(bad_update)
    values_already_checked = set()
    sorted_values = bad_update.copy()
    while len(values_already_checked) < num_values:

        # Get last-most value that we haven't already checked and all values before it
        target_idx, lastmost_value, prior_values_list = None, None, []
        for idx in range(1, num_values + 1):
            lastmost_value = sorted_values[-idx]
            prior_values_list = sorted_values[0:-idx]
            if lastmost_value not in values_already_checked:
                target_idx = num_values - idx
                break
        values_already_checked.add(lastmost_value)

        # Find first-most mismatched value (if one exists) so we can sort last-most value before it
        mismatched_values = page_order_lut[lastmost_value].intersection(prior_values_list)
        if len(mismatched_values) > 0:
            earliest_mismatch_idx = min([sorted_values.index(value) for value in mismatched_values])

            # Sanity check
            assert target_idx > earliest_mismatch_idx, f"Bad 'early' mismatch! {target_idx} vs. {earliest_mismatch_idx}"

            # Update sorting
            sorted_values.pop(target_idx)
            sorted_values.insert(earliest_mismatch_idx, lastmost_value)

    # After loop, we should have sorted the 'bad' listing!
    corrected_updates_list.append(sorted_values)


# Find middle numbers of corrected updates
corrected_middles_list = []
for corrected_update in corrected_updates_list:
    corrected_mid_val = corrected_update[len(corrected_update) // 2]
    corrected_middles_list.append(corrected_mid_val)

print("Part 2:", sum(corrected_middles_list))
