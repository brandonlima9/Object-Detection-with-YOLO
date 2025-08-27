import os
import sys
import customtkinter as CTk
from pathlib import Path
from viz import get_data_def, draw_borders, colours
from tkinter import *
from PIL import Image

img_list_names = []

cur_index = 0

window = CTk.CTk()
window.geometry("1800x1000")

#   // PYTHON: COMB DELETER
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
# 
#   This program finds all of the images in the given directory and attempts to draw YOLO-type object-detection boundings around the detected object in a label.
#   This program allows the user to decide whether an image is "good", "suspicious", or "bad" and easily sorts them into a completed, suspicious directory (or deletes the image if it was bad).


# Finds the sibling directory of the current directory.
def get_other_path(path: str) -> str:
    spl_path = path.split('/')
    if (spl_path[len(spl_path) - 1] == 'labels'):
        spl_path[len(spl_path) - 1] = 'images'
    elif (spl_path[len(spl_path) - 1] == 'images'):
        spl_path[len(spl_path) - 1] = 'labels'
    return '/'.join(spl_path)

# Finds all Images in the given directory.
def find_images(directory: str):
    for filename in os.listdir(directory):
        img_list_names.append(filename)

# Creates a Custom Tkinter image object given the directory.
# Additionally overlays borders according to the object detection label corresponding to this image.
def create_display_image(directory: str):
    image_filename = img_list_names[cur_index]
    image = '/'.join([directory, image_filename])
    img = draw_borders(directory, image_filename, Image.open(image))
    
    height = img.height
    width = img.width
    if (img.height > 900 or img.width > 600):
        height = img.height - (img.height - 600)
        width = img.width - (img.width - 600)

    return CTk.CTkImage(img, size=(width, height))

# Updates the image frame on the menu with a new image.
def update_image_frame(info_label, picture_label, new_image):
    """ Function to change the images based on user input """

    picture_label.configure(image=new_image)
    picture_label.photo = new_image
    info_label.configure(text=f"Current Image: {img_list_names[cur_index]}\nImages Left: {len(img_list_names) - cur_index - 1}")

# Go to next image in the directory and save the current one as a "good" image.
def next_image(info_label, picture_label, directory: str):
    global cur_index

    image_filename = img_list_names[cur_index]
    old_image_path = '/'.join([directory, image_filename])
    new_image_path_arr = directory.split('/').copy()
    new_image_path_arr.insert(len(directory.split('/')) - 2, 'completed')
    new_image_path = '/'.join(['/'.join(new_image_path_arr), image_filename])
	
    label_filename = ''.join([image_filename[:-3], 'txt'])
    old_label_path = '/'.join([get_other_path(directory), label_filename])
    new_label_path_arr = get_other_path(directory).split('/').copy()
    new_label_path_arr.insert(len(get_other_path(directory).split('/')) - 2, 'completed')
    new_label_path = '/'.join(['/'.join(new_label_path_arr), label_filename])
	
    Path('/'.join(new_image_path_arr)).mkdir(parents=True, exist_ok=True)
    Path('/'.join(new_label_path_arr)).mkdir(parents=True, exist_ok=True)
    os.replace(old_image_path, new_image_path)
    os.replace(old_label_path, new_label_path)
    img_list_names.remove(image_filename)
	
    if (len(img_list_names) == 0):
        sys.exit()
    update_image_frame(info_label, picture_label, create_display_image(directory))

# Go to next image in the directory and save the current one as a "suspicious" image.
def mark_suspicious(info_label, picture_label, directory: str):
    global cur_index

    image_filename = img_list_names[cur_index]
    old_image_path = '/'.join([directory, image_filename])
    new_image_path_arr = directory.split('/').copy()
    new_image_path_arr.insert(len(directory.split('/')) - 2, 'suspicious')
    new_image_path = '/'.join(['/'.join(new_image_path_arr), image_filename])
	
    label_filename = ''.join([image_filename[:-3], 'txt'])
    old_label_path = '/'.join([get_other_path(directory), label_filename])
    new_label_path_arr = get_other_path(directory).split('/').copy()
    new_label_path_arr.insert(len(get_other_path(directory).split('/')) - 2, 'suspicious')
    new_label_path = '/'.join(['/'.join(new_label_path_arr), label_filename])
	
    Path('/'.join(new_image_path_arr)).mkdir(parents=True, exist_ok=True)
    Path('/'.join(new_label_path_arr)).mkdir(parents=True, exist_ok=True)
    os.replace(old_image_path, new_image_path)
    os.replace(old_label_path, new_label_path)
    img_list_names.remove(image_filename)
	
    if (len(img_list_names) == 0):
        sys.exit()
    update_image_frame(info_label, picture_label, create_display_image(directory))

# Go to next image in the directory and delete the current one.
def delete_image(info_label, picture_label, directory: str):
    global cur_index
    if (len(img_list_names) == cur_index):
        pass
    else:
        image_filename = img_list_names[cur_index]
        image_path = '/'.join([directory, image_filename])
        label_filename = ''.join([image_filename[:-3], 'txt'])
        label_path = '/'.join([get_other_path(directory), label_filename])
        if (os.path.exists(image_path) and os.path.exists(label_path)):
            os.remove(image_path)
            os.remove(label_path)
            img_list_names.remove(image_filename)
            if (cur_index >= (len(img_list_names) - 1)):
                cur_index = len(img_list_names) - 1
        update_image_frame(info_label, picture_label, create_display_image(directory))

# Main Application Routine. 
def controller(directory: str):
    try:
        image_pane = CTk.CTkFrame(master=window, width=1600, height=900)
        image_pane.pack()
        image_pane.place(anchor='center', relx=0.5, rely=0.5)

        find_images(directory)
        current_image = create_display_image(directory)
        label = CTk.CTkLabel(master=image_pane, text='', image=current_image)
        label.pack()

        info_label = CTk.CTkLabel(master=window, text=f"Current Image: {img_list_names[cur_index]}\nImages Left: {len(img_list_names) - cur_index - 1}", font=('Helvetica', 24, 'bold'))
        info_label.place(anchor='center', relx=0.5, rely=0.1)

        good_button = CTk.CTkButton(master=window, text="Image Looks Good", text_color='black', font=('Helvetica', 18, 'bold'), fg_color='green', command=lambda:next_image(info_label, label, directory))
        good_button.place(anchor='w', relx=0.30, rely=0.9)
        
        sus_button = CTk.CTkButton(master=window, text="Image/Boundaries Look Suspicious", font=('Helvetica', 18, 'bold'), fg_color='orange', command=lambda:mark_suspicious(info_label, label, directory))
        sus_button.place(anchor='center', relx=0.50, rely=0.9)

        delete_button = CTk.CTkButton(master=window, text="Delete this Image", font=('Helvetica', 18, 'bold'), fg_color='red', command=lambda:delete_image(info_label, label, directory))
        delete_button.place(anchor='e', relx=0.70, rely=0.9)

        # Menu component to handle writing the object detection label names and colouring for the detection boxes
        counter = 0
        class_definitions = get_data_def(directory)
        colouring_info = CTk.CTkLabel(master=window, text='Segmentation Colours:', text_color='white', font=('Helvetica', 16, 'bold'))
        colouring_info.place(anchor='center', relx=0.85, rely=0.35)
        for clazz in class_definitions:
            colour = colours[min(len(colours) - 1, counter)]
            colouring_label = CTk.CTkLabel(master=window, text=f"{clazz}", text_color='#%02x%02x%02x' % colour, font=('Helvetica', 16, 'bold'))
            colouring_label.place(anchor='center', relx=0.85, rely=0.3 + 0.05 * (counter + 2))
            counter += 1
        window.mainloop()

    except IndexError as e:
        print(f"No images in directory found -> {e}")

controller('ENTER DIRECTORY HERE')

# Packages used for these scripts:
# pip install tkinter
# pip install customtkinter
# pip install pillow

# Packages maybe (not all) used for these scripts but they're generalist computer vision software so you should have them
# YOLO:
# pip install ultralytics
# pip install filterpy
# Open CV:
# pip install opencv-python