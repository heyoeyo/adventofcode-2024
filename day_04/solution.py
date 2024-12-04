# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()

"""
Input looks like:
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
"""


# %% Part 1

# Helper functions
down_right_shift_and_pad = lambda line, offset: line[offset:].ljust(len(line))
down_left_shift_and_pad = lambda line, offset: line[0 : (len(line) - offset)].rjust(len(line))
transpose_strings = lambda lines: ["".join(char) for char in zip(*lines)]
count_xmas_in_str = lambda one_line: one_line.count("XMAS") + one_line.count("SAMX")

# Count XMAS along rows
num_xmas_per_row = [count_xmas_in_str(l) for l in lines]

# Count XMAS along columns
lines_transposed = transpose_strings(lines)

# Count XMAS along diagonals
num_xmas_dr_diag, num_xmas_dl_diag = [], []
num_four_row_blocks = len(lines) - 3
four_row_slices = [slice(k, k + 4) for k in range(num_four_row_blocks)]
all_4row_lines = [lines[four_row_slice] for four_row_slice in four_row_slices]
for l_4rows in all_4row_lines:

    # Create modified shifted & transposed version of 4-rows of characters
    # -> Shifting 'undoes' the diagonal ordering
    # -> Transpose let's us search for 'XMAS' pattern directly in the string (easier to use built-in counting!)
    l_dr = transpose_strings([down_right_shift_and_pad(line, offset) for offset, line in enumerate(l_4rows)])
    l_dl = transpose_strings([down_left_shift_and_pad(line, offset) for offset, line in enumerate(l_4rows)])
    num_xmas_dr_diag.append(sum(count_xmas_in_str(l) for l in l_dr))
    num_xmas_dl_diag.append(sum(count_xmas_in_str(l) for l in l_dl))
num_xmas_per_column = [count_xmas_in_str(l) for l in lines_transposed]

total_xmas_count = sum(num_xmas_per_row) + sum(num_xmas_per_column) + sum(num_xmas_dr_diag) + sum(num_xmas_dl_diag)
print("Part 1:", total_xmas_count)


# %% Part 2

# Could re-use part 1 solution somewhat, but taking a different approach here
# -> Will look for every instance of 'A' and search diagonal neighbours for target 'MAS' patterns
# -> Don't need to check first/last row or first/last column, since cross pattern can't fit there!

# Loop over every character of every line, looking for 'A', then searching for MAS/SAM diagonals
xmas_row_col_coords = []
for row_idx, row_line in enumerate(lines[1:-1], start=1):
    prev_line, next_line = lines[row_idx - 1], lines[row_idx + 1]
    for col_idx, col_char in enumerate(row_line[1:-1], start=1):
        prev_c_idx, next_c_idx = col_idx - 1, col_idx + 1

        # If we find an 'A' character, search diagonals for MAS/SAM pattern
        if col_char == "A":
            dr_diag_is_mas = prev_line[prev_c_idx] == "M" and next_line[next_c_idx] == "S"
            dr_diag_is_sam = prev_line[prev_c_idx] == "S" and next_line[next_c_idx] == "M"
            dl_diag_is_mas = prev_line[next_c_idx] == "M" and next_line[prev_c_idx] == "S"
            dl_diag_is_sam = prev_line[next_c_idx] == "S" and next_line[prev_c_idx] == "M"
            is_dr_mas = dr_diag_is_mas or dr_diag_is_sam
            is_dl_mas = dl_diag_is_mas or dl_diag_is_sam
            is_xmas = is_dr_mas and is_dl_mas
            if is_xmas:
                xmas_row_col_coords.append((row_idx, col_idx))

print("Part 2:", len(xmas_row_col_coords))
