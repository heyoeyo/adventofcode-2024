# %% Load data

use_test = False
data_path = "test.txt" if use_test else "input.txt"
with open(data_path, "r") as infile:
    puzzle_txt = infile.read()
lines = puzzle_txt.splitlines()

# Split input into 'test' and 'operator' values
test_values_list = []
op_values_list = []
for l in lines:
    str_test, str_op = l.split(": ")
    test_values_list.append(int(str_test))
    str_op_vals = str_op.split(" ")
    op_values_list.append([int(val) for val in str_op_vals])


# %% Define helper functions used across part 1 & 2


def create_operator_sequence(num_operator_values, num_options=2):
    """
    Creates all possible operator sequences for a given number of operator values & operator options
    For example, for 2 values (e.g. [1,2]), there is only one operator (e.g. 1 ? 2). If there are
    3 operator options, then this function returns all of them as indices:
        [(0,), (1,), (2,)]
    For 3 values (e.g. [1,2,3]) and 2 operator options (e.g. 0 or 1), we get:
        [(0,0), (1,0), (0,1), (1,1)]
    """

    num_operators = num_operator_values - 1
    num_sequences = num_options**num_operators

    all_digit_sequences_list = []
    for k in range(num_operators):
        digit_seq = [x // (num_options**k) % num_options for x in range(num_sequences)]
        all_digit_sequences_list.append(digit_seq)

    return list(zip(*all_digit_sequences_list))


def evaluate_operation(values, operator_sequence, enable_print_debug=False):
    """
    Takes a list of values, e.g. [1,2,3,4] and a single operator sequence,
    given as a list of operator indexing: [1,0,2]
    Operator indexing means:
        0 - add values
        1 - multiply
        2 - || concatenate

    So the given example would be interpretted as:
        1 * 2 + 3 || 4 = 54
    """

    result = values[0]
    if enable_print_debug:
        print(result)

    for idx, op in enumerate(operator_sequence):

        next_val = values[1 + idx]
        if op == 0:
            result = result + next_val
        elif op == 1:
            result = result * next_val
        elif op == 2:
            result = int(f"{result}{next_val}")

        if enable_print_debug:
            op_str = "+" if op == 0 else ("*" if op == 1 else "||")
            print(result, op_str, next_val)

    return result


# %% Part 1

num_op_options = 2
true_test_values_list_part_1 = []
for test_val, op_vals in zip(test_values_list, op_values_list):

    # Produce all possible operator sequences for given op values
    num_op_vals = len(op_vals)
    op_sequences_list = create_operator_sequence(num_op_vals, num_op_options)

    # Try computing result from all possible operator sequences and look for a result matching the test value
    for op_seq in op_sequences_list:
        result = evaluate_operation(op_vals, op_seq)
        if result == test_val:
            true_test_values_list_part_1.append(result)
            break

    pass

print("Part 1:", sum(true_test_values_list_part_1))


# %% Part 2

# Same as part 1, except now we use all 3 operators
num_op_options = 3
true_test_values_list_part_2 = []
for test_val, op_vals in zip(test_values_list, op_values_list):
    num_op_vals = len(op_vals)
    op_sequences_list = create_operator_sequence(num_op_vals, num_op_options)
    for op_seq in op_sequences_list:
        result = evaluate_operation(op_vals, op_seq)
        if result == test_val:
            true_test_values_list_part_2.append(result)
            break
    pass

print("Part 2:", sum(true_test_values_list_part_2))
