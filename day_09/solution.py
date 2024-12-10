# %% Load data

use_test = False
test_path = "test1.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()
in_text = lines[0] if len(lines[0]) % 2 == 0 else "".join((lines[0], "0"))

# Separate file blocks and spaces from input
num_blocks_list = [int(char) for char in in_text[0::2]]
num_spaces_list = [int(char) for char in in_text[1::2]]
total_space = sum(num_blocks_list) + sum(num_spaces_list)

# Make 'full' block list, with gaps as None
# -> '12345' becomes: [0,.,.,1,1,1,.,.,.,.,2,2,2,2,2] (using . instead of None for brevity)
last_raw_idx = 0
block_idx_list, space_idx_list = [], []
raw_input_list = [None] * total_space
for file_idx, (num_blocks, num_space) in enumerate(zip(num_blocks_list, num_spaces_list)):

    # Write file indexing into raw input & record index sequence of file blocks
    next_raw_idx = last_raw_idx + num_blocks
    raw_input_list[last_raw_idx:next_raw_idx] = [file_idx] * num_blocks
    block_idx_list.extend(range(last_raw_idx, next_raw_idx))

    # Recording index sequence of spaces (don't need to write spaces in input, since it defaults to space everywhere!)
    last_raw_idx = next_raw_idx + num_space
    space_idx_list.extend(range(next_raw_idx, last_raw_idx))


# %% Part 1

total_blocks = len(raw_input_list)
contiguous_blocks_list = raw_input_list.copy()
for space_idx, rev_block_idx in zip(space_idx_list, reversed(block_idx_list)):

    if rev_block_idx > total_blocks - 1:
        break

    contiguous_blocks_list[space_idx] = raw_input_list[rev_block_idx]
    total_blocks -= 1

contiguous_blocks_list = contiguous_blocks_list[:total_blocks]
checksum_list = [val * idx for idx, val in enumerate(contiguous_blocks_list)]

print("Part 1:", sum(checksum_list))


# %% Part 2

print("Part 2:", None)
