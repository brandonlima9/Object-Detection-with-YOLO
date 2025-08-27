import os

#   // PYTHON: UNIQUE NUMS
#
#   This program is meant to be used on an labels directory where there are text files filled with YOLO-type object detection labels.
#   Note that you should use the full path for your directory.
#
#   A YOLO label: [CLASS ID] [CENTER X OF DETECTION BOUNDING BOX] [CENTER Y OF DETECTION BOUNDING BOX] [HEIGHT OF DETECTION BOUNDING BOX] [WIDTH OF DETECTION BOUNDING BOX]:
#   -> For example: 1 0.50703125 0.58125 0.9453125 0.71875
#
#   This program counts the number of times a class ID appears in a given file or directory. 

#   Gets the class ID for a label.
def process_line_item(x):
    val = None
    try:
        val = int(x[1].split(' ')[0])
    except ValueError:
        val = None
    return val

# Processes all label files in the directory.
def unique_nums(directory: str):
    numbers = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file: # open in readonly mode
            data = file.read()
            numbers = numbers + list(map(process_line_item, enumerate(data.split('\n'))))
    print(list(set(numbers)))
    for integer in list(set(numbers)):
        print(f"Number of {integer}'s: {numbers.count(integer)}")

# Processes all label files in the directory.       
def unique_nums_file(file_name: str):
    data = None
    with open(file_name, 'r') as file:
        data = file.read()
    numbers = list(map(process_line_item, enumerate(data.split('\n'))))
    print(list(set(numbers)))
    for integer in list(set(numbers)):
        print(f"Number of {integer}'s: {numbers.count(integer)}")

unique_nums("ENTER DIRECTORY HERE")
