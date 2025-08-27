import os

to_keep = [0, 1]
max_vals_per_line=5

#   // PYTHON: REMOVER
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
#   Example 2, a yolo label ([CLASS ID] [CENTER X OF DETECTION BOUNDING BOX] [CENTER Y OF DETECTION BOUNDING BOX] [HEIGHT OF DETECTION BOUNDING BOX] [WIDTH OF DETECTION BOUNDING BOX]):
#   1 0.50703125 0.58125 0.9453125 0.71875
# 
#   This program finds all of the labels in the given directory and deletes all labels, label files, and corresponding images given a set of criteria.
#   1. If a label has any class ID other than the ones listed in ${to_keep}, delete the label.
#   2. If a label has a parameter count not identical to ${max_vals_per_line}, delete the label.
#   3. If a label file no longer has any labels in it (either never had any to start with or they were deleted given the previous criteria), delete the label file its corresponding image.

# Determine which labels should be kept according to criteria.
def process_file_item(data: str) -> str:
    data_lines = data.split('\n')
    clone_data_lines = data_lines.copy()
    for line in clone_data_lines:
        if (line == '' or line == ' '):
            data_lines.remove(line)
        else:
            val = int(line.split(' ')[0])
            number_of_values = len(line.split(' '))
            if (val not in to_keep or number_of_values != max_vals_per_line):
                data_lines.remove(line)
    if (len(data_lines) == 0):
        return None
    return '\n'.join(data_lines)

# Processes all label files in the directory.
def get_other_path(path: str) -> str:
    spl_path = path.split('/')
    if (spl_path[len(spl_path) - 1] == 'labels'):
        spl_path[len(spl_path) - 1] = 'images'
    elif (spl_path[len(spl_path) - 1] == 'images'):
        spl_path[len(spl_path) - 1] = 'labels'
    return '/'.join(spl_path)

# Processes all label files in the directory.
def entire_directory(directory: str):   
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file: # open in readonly mode
            data = file.read()
            new_data = process_file_item(data)
            file.close()
            if (new_data == None):
                other_filename = ''.join([filename[:-3], 'jpg'])
                if (os.path.exists('/'.join([directory, filename])) and os.path.exists('/'.join([get_other_path(directory), other_filename]))):
                    os.remove('/'.join([directory, filename]))
                    os.remove('/'.join([get_other_path(directory), other_filename]))
            else:
                with open(os.path.join(directory, filename), 'w') as file:
                    file.write(new_data)

# Processes a single label file.           
def single_file(filename: str):
    data = None
    with open(filename, 'r') as file:
        data = file.read()
    new_data = process_file_item(data)
    if (new_data == None):
        if (os.path.exists(filename)):
            os.remove(filename)
    else:
        with open(filename, 'w') as file:
            file.write(new_data)
    
entire_directory("ENTER DIRECTORY HERE")