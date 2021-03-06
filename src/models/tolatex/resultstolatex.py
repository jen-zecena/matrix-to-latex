"""
resultstolatex.py

takes in a filepath that goes to a file in YOLOv5 format and the symbol
classes list and returns the string LaTeX code corresponding to that file

TO USE: run 'resultstolatex(filepath, classes)'
"""


def to_array(results):
    """
    converts formatted YOLOv5 output and isolates brackets, while converting
    matrix to 2d array
    input: list with elements in the form:
        ['symbol class', [x_center, y_center]]
    output: list of the form:
        [['bracket', 'bracket'], [2D array representing matrix]]
    uses a + or - 12.5% margin of error for determining rows
    """
    margin_of_error = .125
    # remove brackets
    brackets = list(
        map(
            lambda x: x[0],
            list(
                filter(lambda x: x[0] in ['(', ')', '[', ']', '{', '}', '|'],
                       results))))

    results = list(
        filter(lambda x: x[0] not in ['(', ')', '[', ']', '{', '}', '|'],
               results))
    elements = []
    while len(results) > 0:
        # find object closest to the top of image
        y_coordinate = min(map(lambda x: [x[1][1], x], results))[0]
        # find all elements with center within margin of error
        row_elements = list(
            filter(lambda x: within_margin(x[1][1], y_coordinate,
                                           margin_of_error), results))
        for elem in row_elements:
            results.remove(elem)
        # sort by x-coordinates
        x_coord_elements = list(map(lambda x: [x[1][0], x[0]],
                                row_elements))
        x_coord_elements.sort()
        row = list(map(lambda x: x[1], x_coord_elements))
        elements += [row]
    return [brackets, elements]


def to_latex(brackets, elements):
    """
    takes brackets and 2d array of elements
    input:
        brackets: list of the opening and closing brackets of a matrix
        elements: 2d array of the elements and returns the latex code
        corresponding to that matrix
    output: string of LaTeX code
    """
    if brackets == [] and elements == []:
        # no symbols found, retur empty string
        return "No matrix detected."

    start = '$'
    if '(' in brackets or ')' in brackets:
        start += '\\begin{pmatrix} \n'
        end = '\n \\end{pmatrix}'
    elif '[' in brackets or ']' in brackets:
        start += '\\begin{bmatrix}\n'
        end = '\n\\end{bmatrix}'
    elif '{' in brackets or '}' in brackets:
        start += '\\begin{Bmatrix}\n'
        end = '\n\\end{Bmatrix}'
    elif '|' in brackets:
        start += '\\begin{vmatrix}\n'
        end = '\n\\end{vmatrix}'
    else:
        start += '\\begin{matrix}\n'
        end = '\n\\end{matrix}'
    end += '$'
    latex = start
    for row in elements:
        for element in row:
            latex += element
            if element != '-':
                # do not add space for negative sign
                latex += ' & '
        latex = latex[:-2]  # remove last '& '
        latex += '\\\\ \n'
    return latex[:-4] + end  # remove last '\\\\ \n'


def within_margin(testvalue, mainvalue, margin):
    """
        returns true if and only if
        testvalue is within margin of mainvalue
    """
    return mainvalue - margin <= testvalue <= mainvalue + margin


def read_file(filepath, classes):
    """
        reads in a file and YOLOv5 format,
        and returns that information formatted with index codes converted
        to symbol classes and the center information grouped
        input:
            filepath: path to a file in YOLOv5 format
            classes: the list of symbol classes for the model
        output:
            list, with each element corresponding to one bounding box
            each element is in the format
            'symbol class', [x_center, y_center]]
    """
    with open(filepath) as file:
        lines = file.readlines()
    # remove whitespace and split each line into 5 numbers
    lines = list(map(lambda line: line.strip().split(' '), lines))
    # convert from strings to numbers
    lines = list(map(lambda line: list(map(float, line)), lines))
    # change to nested list with 3 elements: symbol class, [x_center, y_center]
    converted = list(
        map(lambda line: [classes[int(line[0])], line[1:3]], lines))
    return converted


def results_to_latex(filepath, classes):
    """
        takes in a path to a YOLOv5 file and the symbol classes for the model
        and returns the matching LaTeX code
    """
    results = read_file(filepath, classes)
    [brackets, elements] = to_array(results)
    return to_latex(brackets, elements)
