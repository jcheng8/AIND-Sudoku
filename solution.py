assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# two diagonals: (I) [A1, B2, ..., I9], (II)[A9, B8,..., I1]. Each works as a unit as other units
diag_units = ([[s+t for (s,t) in list(zip(rows, cols))]] +
    [[s+t for (s,t) in list(zip(rows, reversed(cols)))]])
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    twins = []
    for unit in unitlist:
        # twins condition : len(box1) == len(box2) == 2, values[box1] == values[box2]
        # use s < t to avoid duplication (box1, box2) and (box2, box1)
        unit_twins = [(s,t, unit) for s in unit for t in unit if s < t and len(values[s]) == 2 and values[s] == values[t]]
        twins = twins + unit_twins

    # Eliminate the naked twins as possibilities for their peers
    for twin in twins:
        # apply elimination within each unit
        s1, s2, boxes = twin
        digits = values[s1]
        for peer in boxes:
            # only apply to unresolved boxes
            if len(values[peer]) > 1 and values[peer] != digits:
                for digit in digits:
                    assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    known_boxes = [k for k, v in values.items() if len(v) == 1]
    for box in known_boxes:
        eliminator = values[box]
        for p in peers[box]:
            assign_value(values, p, values[p].replace(eliminator, ''))
    return values

def only_choice(values):
    new_values = values.copy()  # note: do not modify original values

    for unit in unitlist:
        for digit in '123456789':
            containing_boxes = [box for box in unit if digit in values[box]]
            if len(containing_boxes) == 1:
                assign_value(values, containing_boxes[0], digit)
    return new_values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            #print("empty for {0}".format([box for box in values.keys() if len(values[box]) == 0]))
            return False
    return values

def search(values):
    # First, reduce the puzzle using the previous function
    result = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if not result:
        return False
    if all([len(v) == 1 for k, v in values.items()]):
        return values

    unresolved = [(len(v), k) for k, v in values.items() if len(v) > 1]
    n, box = min(unresolved)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    choices = values[box]
    for digit in choices:
        copy = values.copy()
        copy[box] = digit
        result = search(copy)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
