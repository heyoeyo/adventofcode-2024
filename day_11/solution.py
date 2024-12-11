# %% Load data

use_test = False
test_path = "test1.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()

# Convert sequence of string numbers to actual integers
puzzle_strs_list = [part for part in puzzle_txt.split()]


# %% Part 1

curr_sequence = [int(val_str) for val_str in puzzle_strs_list]
num_blinks = 25
for k in range(num_blinks):

    next_sequence = []
    for value_int in curr_sequence:

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

        # Update output sequence
        next_sequence.extend(replace_seq)

    # Update the current sequence (after N blinks)
    curr_sequence = next_sequence

print("Part 1:", len(curr_sequence))


# %% Part 2

print("Part 2:", None)
