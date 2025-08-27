import os

to_replace = [80, 81]
to_replace_with = [0, 1]

#   // PYTHON: REPLACER
#
#   This program is meant to be used on an images directory where there are labels/images directories under a common parent directory.
#   For example (note that you should use the full path for any of the directories labelled with [*] below):
#   ./main_directory
#       |> train
#           |> images
#           |> labels [*]
#       |> val
#           |> images
#           |> labels [*]
#       |> test
#           |> images 
#           |> labels [*]
#
#   A YOLO label: [CLASS ID] [CENTER X OF DETECTION BOUNDING BOX] [CENTER Y OF DETECTION BOUNDING BOX] [HEIGHT OF DETECTION BOUNDING BOX] [WIDTH OF DETECTION BOUNDING BOX]:
#   -> For example: 1 0.50703125 0.58125 0.9453125 0.71875
#
#   This program finds all of the labels in the given directory and swaps the classification IDs from ${to_replace} to ${to_replace_with}. There are two operating modes:
#   1. If the array length of both ${to_replace} and ${to_replace_with} are the same:
#       -> Each index will be mapped directly to each other. 
#           -> For example to_replace = [78, 79] and to_replace_with = [0, 1]. Any class ID instance of 78 would be turned into 0 and any class ID instance of 79 would be turned into 1.
#   2. If the array length of both ${to_replace} and ${to_replace_with} are not the same:
#       -> Each value in ${to_replace} will be to the value at the first index in ${to_replace_with}. 
#           -> For example to_replace = [78, 79] and to_replace_with = [0]. Any class ID instance of 78 or 79 would be turned into 0.

# Swaps the label's class IDs around
def process_line_item(x):
    first_number = x[1].split(' ')[0]
    if (int(first_number) in to_replace):
        replacement_index = 0
        if (len(to_replace) == len(to_replace_with)):
            replacement_index = to_replace.index(int(first_number))
        new_first_value = [str(to_replace_with[replacement_index])]
        return ' '.join(new_first_value + x[1].split(' ')[1:])
    return ' '.join(x[1].split(' ')[0:])

# Processes all label files in the directory.
def entire_directory(directory: str):   
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file: # open in readonly mode
            data = file.read()
            new_data = '\n'.join(list(map(process_line_item, enumerate(data.split('\n')))))

            with open(os.path.join(directory, filename), 'w') as rep_file:
                rep_file.write(new_data)

# Processes all label files in the directory.           
def single_file(filename: str, replacement_filename: str):
    data = None
    with open(filename, 'r') as file:
        data = file.read()
    new_data = '\n'.join(list(map(process_line_item, enumerate(data.split('\n')))))

    with open(replacement_filename, 'w') as file:
        file.write(new_data)

entire_directory("ENTER DIRECTORY HERE")