from collections import defaultdict

# %% Load data

use_test = False
test_path = "test1.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()

# Convert sequence of string numbers to actual integers
puzzle_strs_list = [part for part in puzzle_txt.split()]


def apply_rules(value_int):
    """
    Helper function which takes a single integer and produces
    a list of 'split' results according to problem rules
    """

    # For convenience
    value_str = str(value_int)
    value_len = len(value_str)

    # Figure out the replacement value for each sequence item
    replace_seq = None
    if value_int == 0:
        # Handle 'value is 0' case
        replace_seq = [1]

    elif (value_len % 2) == 0:
        # Handle 'value has even number of digits' case
        mid_str_idx = value_len // 2
        first_val_str = value_str[:mid_str_idx]
        second_val_str = value_str[mid_str_idx:]
        replace_seq = [int(first_val_str), int(second_val_str)]

    else:
        # No other rules apply, so multiply by 2024
        replace_seq = [2024 * value_int]

    return replace_seq


# %% Part 1

curr_sequence = [int(val_str) for val_str in puzzle_strs_list]
num_blinks = 25
for k in range(num_blinks):

    next_sequence = []
    for value_int in curr_sequence:
        replace_seq = apply_rules(value_int)
        next_sequence.extend(replace_seq)

    # Update the current sequence (after N blinks)
    curr_sequence = next_sequence

print("Part 1:", len(curr_sequence))


# %% Part 2

# Can't repeat part 1 solution, because it's too slow
# -> List splitting grows exponentially!
# -> However, lots of numbers keep repeating... Can avoid exponential growth by caching results as we go...
# Idea is to ignore ordering (doesn't actually matter) and instead count 'set' of numbers on each line
# -> We 'count' each new number based on the number of times the value it was split from was previously seen (counted)

# Set up initial count for number of times each value appears
parent_counts_per_value = defaultdict(int)
for value_int in [int(val_str) for val_str in puzzle_strs_list]:
    parent_counts_per_value[value_int] += 1

num_blinks = 75
for k in range(num_blinks):

    # Initialize (zeroed) counts for the results of 'blinking' the parent values
    child_counts_per_value = defaultdict(int)

    # Apply update rule to each previously seen value to get new sequence
    for prev_value, prev_count in parent_counts_per_value.items():
        replace_seq = apply_rules(prev_value)

        # For each value in new sequence, 'count' it according to the number of times it's parent has been counted
        # -> This is where our speed-up comes from. We only consider each parent value once, but account for
        #    multiple 'sightings' of the value from previous iterations!
        # -> This has a multiplicative effect for values appearing multiple times in the new sequence
        # -> ex: if the parent value was 77, then it will split to [7, 7] , so 7 is counted twice by this loop!
        # -> If the value 77 had been seen 4 times previously, then we would 'count' 7 a total of (4 + 4) times!
        for replace_value in replace_seq:
            child_counts_per_value[replace_value] += prev_count

    # Consider child values as the parent values for the next iteration
    parent_counts_per_value = child_counts_per_value

print("Part 2:", sum(parent_counts_per_value.values()))
