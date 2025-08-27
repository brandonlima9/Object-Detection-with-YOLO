import os

vals_per_line=5

#   // PYTHON: LINE VALUE COUNTER
#
#   This program is meant to be used on an labels directory where there are text files filled with YOLO-type object detection labels.
#   Note that you should use the full path for your directory.
#
#   A YOLO label: [CLASS ID] [CENTER X OF DETECTION BOUNDING BOX] [CENTER Y OF DETECTION BOUNDING BOX] [HEIGHT OF DETECTION BOUNDING BOX] [WIDTH OF DETECTION BOUNDING BOX]:
#   -> For example: 1 0.50703125 0.58125 0.9453125 0.71875
# 
#   This program counts the number of times any label doesn't have ${vals_per_line} parameters. 

# Determine which labels should be kept according to criteria.
def process_file_item(data: str) -> str:
    data_lines = data.split('\n')
    clone_data_lines = data_lines.copy()
    for line in clone_data_lines:
        if (line == '' or line == ' '):
            data_lines.remove(line)
        else:
            number_of_values = len(line.split(' '))
            if (number_of_values != vals_per_line):
                data_lines.remove(line)
    if (len(data_lines) == 0):
        return None
    return '\n'.join(data_lines)

# Processes all label files in the directory.
def entire_directory(directory: str) -> int:   
    counter = 0
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file: # open in readonly mode
            data = file.read()
            new_data = process_file_item(data)
            if (new_data == None):
                counter += 1
                print(filename)
            file.close()
    return counter

print(entire_directory("ENTER DIRECTORY HERE"))