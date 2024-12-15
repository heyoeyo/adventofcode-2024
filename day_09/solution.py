# %% Load data

use_test = False
test_path = "test1.txt"
data_path = test_path if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()

# The input alternates between 'number of blocks, number of spaces'
# -> Expecting even number of 'numbers', if we get an odd count, append a 0 (zero spaces) to the end!
in_text = lines[0] if len(lines[0]) % 2 == 0 else "".join((lines[0], "0"))

# Separate file blocks and spaces from input
num_blocks_list = [int(char) for char in in_text[0::2]]
num_spaces_list = [int(char) for char in in_text[1::2]]
total_space = sum(num_blocks_list) + sum(num_spaces_list)

# Make 'full' block list, with gaps as None
# -> '12345' becomes: [0,.,.,1,1,1,.,.,.,.,2,2,2,2,2] (using . instead of None for brevity)
start_of_blocks_idx = 0
block_idx_list, space_idx_list = [], []
block_start_idx_list, space_start_idx_list = [], []
raw_input_list = [None] * total_space
for file_idx, (num_blocks, num_space) in enumerate(zip(num_blocks_list, num_spaces_list)):

    # Record starting index for each block entry (used for part 2 specifically)
    block_start_idx_list.append(start_of_blocks_idx)

    # Write file indexing into raw input & record index sequence of file blocks
    start_of_spaces_idx = start_of_blocks_idx + num_blocks
    raw_input_list[start_of_blocks_idx:start_of_spaces_idx] = [file_idx] * num_blocks
    block_idx_list.extend(range(start_of_blocks_idx, start_of_spaces_idx))

    # Recording index sequence of spaces (don't need to write spaces in input, since it defaults to space everywhere!)
    start_of_blocks_idx = start_of_spaces_idx + num_space
    space_idx_list.extend(range(start_of_spaces_idx, start_of_blocks_idx))

    # Record starting index for each space entry
    space_start_idx_list.append(start_of_spaces_idx)


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

# Set up storage for keeping track of how much space is available and where
# -> This will be modified inside the loop!
space_available_list = num_spaces_list.copy()
available_start_idx_list = space_start_idx_list.copy()

# Set up reversed iterables (written out in full for easier debugging...)
rev_ids_list = list(reversed(range(len(num_blocks_list))))
rev_block_start_idx = list(reversed(block_start_idx_list))
rev_num_blocks = list(reversed(num_blocks_list))

part2_contiguous_blocks_list = raw_input_list.copy()
for block_id, block_start_idx, num_blocks in zip(rev_ids_list, rev_block_start_idx, rev_num_blocks):

    # Stop all searching if the block is after the first available space
    if available_start_idx_list[0] > block_start_idx:
        break

    # For each space available, check if we could fit the given block
    for avail_idx, space_available in enumerate(space_available_list):

        # Stop searching once the index of 'available space' exceeds the index of the block being considered
        # -> This doesn't mean we're done searching entirely though! Still need to consider other block ids
        space_start_idx = available_start_idx_list[avail_idx]
        if space_start_idx > block_start_idx:
            break

        # 'Move' block id to space, if possible
        is_space_fillable = num_blocks <= space_available
        if is_space_fillable:

            # 'Fill in' space with block id
            start_of_fill = space_start_idx
            end_of_fill = start_of_fill + num_blocks
            part2_contiguous_blocks_list[start_of_fill:end_of_fill] = [block_id] * num_blocks

            # 'Erase' block ID from the other end of the list (so it's as if we 'moved' it)
            start_of_removal = block_start_idx
            end_of_removal = start_of_removal + num_blocks
            part2_contiguous_blocks_list[start_of_removal:end_of_removal] = [None] * num_blocks

            # Update index of newly available space
            num_space_left = space_available - num_blocks
            space_available_list[avail_idx] = num_space_left
            available_start_idx_list[avail_idx] = end_of_fill

            # If we use up all the space, tag the entry for removal (not required, but speeds things up)
            # -> Avoid pop inside of the loop itself, for fear of angering the loop gods
            need_pop = num_space_left == 0

            break

    # If we've used up all the space of a given entry, knock it out of the listing
    if need_pop:
        space_available_list.pop(avail_idx)
        available_start_idx_list.pop(avail_idx)

    pass

checksum_list = [val * idx for idx, val in enumerate(part2_contiguous_blocks_list) if val is not None]
print("Part 2:", sum(checksum_list))
