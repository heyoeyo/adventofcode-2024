# %% Load data

use_test = False
test_path = "test2.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()


# %% Part 1

# Break text into pieces inbetween instances of 'mul('
mul_splits = puzzle_txt.split("mul(")[1:]

# For each text fragment after 'mul(' try to find corresponding 'x,y)'
x_list, y_list = [], []
for split in mul_splits:

    # Assume 'x' value is contained in text before the first instance of ','
    first_comma_idx = split.find(",")
    if first_comma_idx == -1:
        continue

    # Assume 'y' value is contained in text following ',' and before first instance of ')'
    subsplit = split[1 + first_comma_idx :]
    close_bracket_idx = subsplit.find(")")
    if close_bracket_idx == -1:
        continue

    # For clarity, index out x & y text
    x_val_str = split[0:first_comma_idx]
    y_val_str = subsplit[0:close_bracket_idx]

    # Try to parse x/y values, if they fail it's because they contain invalid characters (so ignore them)
    try:
        x_val = int(x_val_str)
        y_val = int(y_val_str)
        x_list.append(x_val)
        y_list.append(y_val)
    except ValueError:
        # Happens if x or y text is not a valid integer (we just ignore this case)
        pass

    pass

# Compute sum of all (x,y) pairs multiplied together
total = sum((x * y) for x, y in zip(x_list, y_list))
print("Part 1:", total)


# %% Part 2

# For simplicity, we'll go through the puzzle text and remove all "don't -> do" sections,
# so that we can then re-use the logic from part 1
parse_start = 0
do_txt_list = []
while True:

    # Look for next instance of "don't" so we can take block of do-able text
    dont_idx = puzzle_txt.find("don't", parse_start)

    # Store all text from parse starting point up to "don't" index
    parse_end = dont_idx if dont_idx != -1 else None
    new_txt_block = puzzle_txt[parse_start:parse_end]
    do_txt_list.append(new_txt_block)

    # We're done once we no longer find instances of "don't"
    if dont_idx == -1:
        break

    # Now jump parsing start index to the next "do" instance
    # -> Need to be careful parsing, because searching for "do" will match with "don't"
    found_next_do = False
    parse_start = dont_idx + 1
    while True:
        next_dont_idx = puzzle_txt.find("don't", parse_start)
        next_do_idx = puzzle_txt.find("do", parse_start)
        parse_start = next_do_idx + 1

        is_no_next_do = next_do_idx == -1
        found_next_do = next_do_idx != next_dont_idx
        if found_next_do or is_no_next_do:
            break

    # Stop if we can't find a 'next' starting point (we've reached the end of the text)
    if not found_next_do:
        break

    pass

# Do the exact same thing that we did in part 1, now using text with the 'dont' sections removed
part2_txt = "".join(do_txt_list)
mul_splits = part2_txt.split("mul(")[1:]
x_list, y_list = [], []
for split in mul_splits:

    first_comma_idx = split.find(",")
    if first_comma_idx == -1:
        continue

    subsplit = split[1 + first_comma_idx :]
    close_bracket_idx = subsplit.find(")")
    if close_bracket_idx == -1:
        continue

    x_val = split[0:first_comma_idx]
    y_val = subsplit[0:close_bracket_idx]
    try:
        x_val = int(x_val)
        y_val = int(y_val)
    except ValueError:
        continue
    x_list.append(x_val)
    y_list.append(y_val)

total = sum((x * y) for x, y in zip(x_list, y_list))

print("Part 2:", total)
