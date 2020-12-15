#! /usr/bin/python3

"""
    This program will solve nonogram puzzles for any x*x size with given starting conditions.
"""

from itertools import groupby

def find_options(length, filled):
    """ This function finds all possibilities for the starting condition of the rows or columns. """

    # TODO: Make a version of this function that takes a pattern to compare with (already filled out
    #       row) and skip any pattern that doesn't match.

    # TODO: Make a version of this for the empty hash as well.

    total_filled = sum(filled)
    total_empty = length - total_filled
    extra = total_empty - len(filled) + 1
    lines = []
    ones = filled[0]

    for pad in range(0, extra + 1):
        # Loop over each possible set of padding.

        line = ''
        blanks = len(filled)
        total_blanks = total_empty - pad

        # Set the first value of the sub-string.
        line += '0' * pad
        line += '1' * ones

        # Subtract from the number of dividers left.
        blanks -= 1

        if blanks > 0:
            # If there are still dividers, leave a blank for it.
            line += '0'

            # Subtract this divider from the total blanks left.
            total_blanks -= 1

        if len(filled) > 1:
            # If the string has not been fully built yet, then generate the next sub-string.
            subs = find_options(length - len(line), filled[1:])

            for sub in subs:
                # Append this section with the sub-sections found in the recursion.
                lines.append(line + sub)
        else:
            # There are no parts left so pad with the remaining blanks.
            line += '0' * total_blanks

            # Add the string to the possible values.
            lines.append(line)

    # Return the possible values.
    return lines

def find_overlap(length, patterns):
    """ This function finds the overlap between the current possibilities for a row or column. """

    # Set the initial maks to everything set.  This handles up to a 32x32 grid.
    overlap = 0xFFFFFFFF

    for pattern in patterns:
        # Convert each possibility to an integer based on the string bit pattern and generate
        # the overlap mask.
        overlap &= int(pattern, base=2)

    # Return the value as a bit pattern string.
    return "{0:b}".format(overlap).zfill(length)

def compare_existing(length, patterns, existing=''):
    """
        This function adds information from a partially user-solved row or column to the
        computer-generated row or column.
    """

    if existing == '':
        # Set the default to a completely unset bit pattern string.
        existing = '0' * length

    # Lookup the overlap value.
    pattern = int(find_overlap(length, patterns), base=2)

    # Merge the overlap value and the already existing value.
    pattern |= int(existing, base=2)

    # Return the value as a bit pattern string.
    return "{0:b}".format(pattern).zfill(length)

def update_existing(col_existing, row_existing):
    """
        This function updates the rows based on the columns and vice-versa.  It basically rotates
        one matrix in memory and compares it to the other one.
    """

    for row_index in range(0, len(col_existing)):
        for col_index in range(0, len(row_existing)):
            if col_existing[row_index][col_index] == '1':
                row_existing[col_index] \
                    = row_existing[col_index][:row_index] \
                    + '1' \
                    + row_existing[col_index][row_index+1:]

            if row_existing[row_index][col_index] == '1':
                col_existing[col_index] \
                    = col_existing[col_index][:row_index] \
                    + '1' \
                    + col_existing[col_index][row_index+1:]

    return row_existing, col_existing

def find_empty(grid, existing):
    """ This function is a stub to find the locations that cannot be set. """

    empty = []

    for row in range(0, len(grid)):
        empty.append('0' * len(grid))

    for index in range(0, len(existing)):
        runs = groupby(existing[index])
        result = [(label, sum(1 for _ in group)) for label, group in runs]

        total_filled = sum(grid[index])
        total_line = 0

        for key, value in result:
            if key == '1':
                total_line += value

        if total_filled == total_line:
            # #1 -- works
            # #2 -- needs to be tested
            for col in range(0, len(existing[index])):
                if existing[index][col] == '0':
                    empty[index] = empty[index][:col] + '1' + empty[index][col+1:]
                else:
                    empty[index] = empty[index][:col] + '0' + empty[index][col+1:]

        if total_filled >= total_line:
            # #3
            pass

        # #3 is going to be difficult

        # #4 is going to be very difficult

        print("%u of %u" % (total_line, total_filled))

    print("\n\nEMPTY")

    for row in empty:
        print("%s" % row)

    print("\n\n")

    # TODO #1: If only one value in grid, set all out-of-range values in empty.
    #          (really just a special case of #2)

    # TODO #2: If all 1s are accounted for, set all non-1s in existing to 1s in empty.

    # TODO #3: If some squares cannot be filled in, then mark them as empty (like 8 of 11 of 15)

    # TODO #4: If a complete value in existing, mark its borders in empty.


    return empty

def solve(length, horizontal_grid, vertical_grid):
    """
        This function will solve a nonogram given the length, horizontal_grid, and vertical_grid.
    """

    horizontal_existing = []
    vertical_existing = []

    horizontal_backup = []
    vertical_backup = []

    for row in horizontal_grid:
        patterns = find_options(length, row)

        horizontal_existing.append(find_overlap(length, patterns))

    for row in vertical_grid:
        patterns = find_options(length, row)

        vertical_existing.append(find_overlap(length, patterns))

    passes = 0
    done = 0

    while not done:
        horizontal_backup = horizontal_existing[:]
        vertical_backup = vertical_existing[:]

        vertical_existing, horizontal_existing \
            = update_existing(horizontal_existing, vertical_existing)

        if (horizontal_existing == horizontal_backup and vertical_existing == vertical_backup):
            done = 1

        passes += 1

    print("Passes: %u\n\n" % passes)

    find_empty(horizontal_grid, horizontal_existing)

    print("\n\n")

    return horizontal_existing

LENGTH = 15

HORIZONTAL_GRID = [
    [3,2],
    [1,4,1],
    [2],
    [1,2],
    [1,5],
    [2,7],
    [11],
    [5,2],
    [4,5],
    [3,2,1],
    [3,1,3],
    [2,3,3],
    [2,3,3],
    [1,2,2,2],
    [5,4]
]

VERTICAL_GRID = [
    [2,2],
    [1,1,3],
    [2,2,5,1],
    [1,1,9],
    [1,5,3,1],
    [1,5,1],
    [1,5,2],
    [3,2,3],
    [2,2],
    [2,6],
    [2,2,2],
    [1,1,1,],
    [3,5],
    [2,4],
    [5]
]

# TODO: Need to determine what cannot be filled in as well.

for solved in solve(LENGTH, HORIZONTAL_GRID, VERTICAL_GRID):
    print(solved)
