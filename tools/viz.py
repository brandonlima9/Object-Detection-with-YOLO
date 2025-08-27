import cv2
import numpy
from PIL import Image

#   // PYTHON: VIZ HELPER
#
#   This program is meant to be used on an images directory where there are labels/images directories under a common parent directory and a yaml data definition file above the common parent directory.
#   For example (note that you should use the full path for any of the directories labelled with [*] below):
#   ./main_directory
#       |> train
#           |> images [*]
#           |> labels
#       |> val
#           |> images [*]
#           |> labels
#       |> test
#           |> images [*]
#           |> labels
#       |> data.yaml

# Colouring for bounding boxes.
colours = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

# Gets the data.yaml file corresponding to a labels/images directory.
def get_data_def(path: str) -> str:
    spl_path = path.split('/')
    out = []
    if (spl_path[len(spl_path) - 1] == 'labels' or spl_path[len(spl_path) - 1] == 'images'):
        del spl_path[len(spl_path) - 1]
        spl_path[len(spl_path) - 1] = 'data.yaml'
        data_path = '/'.join(spl_path)
        with open(data_path, 'r') as file:
            # get file data
            data = file.read()
            spl_data = data.split('\n')
            for line in spl_data:
                # split each of the lines in the data and read them
                spl_line = line.split(' ')
                for col in spl_line:
                    # if the first word/number is 'names', then it's the line that has all of the class names
                    if (col == "names:"):
                        definitions = line.split("'")
                        for definition in definitions:
                            # cleanup the class names
                            defin = definition.replace('names:', '').replace('[', '').replace(']', '').replace(', ', '').replace(' ,', '')
                            if (defin != '' and defin != ' '):
                                out.append(defin)
                        
    return out

# Finds the sibling directory of the current directory.
def get_other_path(path: str) -> str:
    spl_path = path.split('/')
    if (spl_path[len(spl_path) - 1] == 'labels'):
        spl_path[len(spl_path) - 1] = 'images'
    elif (spl_path[len(spl_path) - 1] == 'images'):
        spl_path[len(spl_path) - 1] = 'labels'
    return '/'.join(spl_path)

# Get the labels
def get_labels(directory: str, image_name:str):
    label_dir = get_other_path(directory)
    label_name = ''.join([image_name[:-3], 'txt'])
    label_path = '/'.join([label_dir, label_name])
    
    data = []
    with open(label_path, 'r') as file:
        data = file.read()

    return data.split('\n')

# Convert a cv2 image to a pil image
def cv2_to_image(img: numpy.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Convert a pil image to a cv2 image
def image_to_cv2(img: Image) -> numpy.ndarray:
    pil_data = img.convert('RGB')
    image = numpy.array(pil_data)[:, :, ::-1].copy()
    return image

# Draw borders on a pil image given the bounding boxes corresponding to that image.
def draw_borders(directory: str, image_name:str, pil_img:Image, thickness=2):
    img = image_to_cv2(pil_img)
    for label in get_labels(directory, image_name):
        label_info = label.split(' ')
        if (len(label_info) == 5): 
            colour = colours[min(len(colours) - 1, int(label_info[0]))]
            bgr_colour = (colour[2], colour[1], colour[0])
            image_height = pil_img.height
            image_width = pil_img.width
            x, y, w, h = map(float, label_info[1:])
            x_min = int((x - (w / 2)) * image_width)
            y_min = int((y - (h / 2)) * image_height)
            x_max = int((x + (w / 2)) * image_width)
            y_max = int((y + (h / 2)) * image_height)

            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), bgr_colour, thickness)
    return cv2_to_image(img)