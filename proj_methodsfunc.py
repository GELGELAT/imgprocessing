import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image

from proj_image_nodes import *


#ф обесцвечивания
def decoloration_method(label,current_sub_method):
    if current_sub_method.tag == 'decoloration_standard':
        decoloration_method_sub_method_standard(label,current_sub_method)
    elif current_sub_method.tag == 'decoloration_weighted':
        decoloration_method_sub_method_weighted(label,current_sub_method)

def decoloration_method_sub_method_standard(label,current_sub_method):
    settings = current_sub_method.object.settings
    top_limit = settings[0]
    bottom_limit = settings[1]

    image = get_image(label.head, label.current)
    pil_image = image.pil_image
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    width, height = pil_image.size
    new_image = Image.new('RGBA',(width, height))
    pixels_array = pil_image.load()
    new_pixels_array = new_image.load()
    for x in range(width):
        for y in range(height):
            R, G, B, A = pixels_array[x, y]
            sum = (R + G + B) // 3
            if sum > top_limit:
                sum = 255
            elif sum < bottom_limit:
                sum = 0
            new_pixels_array[x, y] = (sum, sum, sum, A)
    image.next = create_image_list(new_image)
    label.current +=1

def decoloration_method_sub_method_weighted(label,current_sub_method):
    settings = current_sub_method.object.settings
    R_coefficient = settings[0]
    G_coefficient = settings[1]
    B_coefficient = settings[2]
    image = get_image(label.head, label.current)
    pil_image = image.pil_image
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    width, height = pil_image.size
    new_image = Image.new('RGBA', (width, height))
    pixels_array = pil_image.load()
    new_pixels_array = new_image.load()
    for x in range(width):
        for y in range(height):
            R, G, B, A = pixels_array[x, y]
            sum = int(R_coefficient * R + G_coefficient * G + B_coefficient * B)
            new_pixels_array[x, y] = (sum, sum, sum, A)
    image.next = create_image_list(new_image)
    label.current += 1

def color_mapping_method(label,current_sub_method):
    if current_sub_method.tag == 'color_mapping_two_colors':
        color_mapping_sub_method_two_colors(label,current_sub_method)
def color_mapping_sub_method_two_colors(label,current_sub_method):
    settings = current_sub_method.object.settings
    first_color = settings[0]
    second_color = settings[1]
    limit = settings[2]
    image = get_image(label.head, label.current)
    pil_image = image.pil_image
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    width, height = pil_image.size
    new_image = Image.new('RGBA', (width, height))
    pixels_array = pil_image.load()
    new_pixels_array = new_image.load()
    for x in range(width):
        for y in range(height):
            R, G, B, A = pixels_array[x, y]
            if (R + G + B) // 3 >=limit:
                new_pixels_array[x, y] = (first_color[0],first_color[1],first_color[2],A)
            else:
                new_pixels_array[x, y] = (second_color[0],second_color[1],second_color[2],A)
#(132,71,21)(59,20,6)
    image.next = create_image_list(new_image)
    label.current +=1


#получ метод
def get_method_name(event,combo):
    method = combo.get()
    current_method = method
    return current_method

#вызываем функцию
def use_method(event,current_method,label,current_sub_method):
    if current_method == "Decoloration":
        decoloration_method(label,current_sub_method)
    elif current_method == "Color Mapping":
        color_mapping_method(label,current_sub_method)