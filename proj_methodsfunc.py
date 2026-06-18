import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from json import loads

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
    print(settings)
    first_color = loads(settings[0])
    second_color = loads(settings[1])
    print(first_color)
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
            if (R + G + B) // 3 >=int(limit):
                new_pixels_array[x, y] = (first_color[0],first_color[1],first_color[2],A)
            else:
                new_pixels_array[x, y] = (second_color[0],second_color[1],second_color[2],A)
#(132,71,21)(59,20,6)
    image.next = create_image_list(new_image)
    label.current +=1


from PIL import Image


def pixelization_standard_method_sub_method(label, current_sub_method):
    settings = current_sub_method.object.settings
    block_x_size = int(settings[0])
    block_y_size = int(settings[1])
    compress = int(settings[2])
    image = get_image(label.head, label.current)
    pil_image = image.pil_image

    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')

    width, height = pil_image.size
    pixels = pil_image.load()


    if compress == 0:
        new_image = Image.new('RGBA', (width, height))
        new_pixels = new_image.load()
        for y in range(0, height, block_y_size):
            for x in range(0, width, block_x_size):

                x_end = min(x + block_x_size, width)
                y_end = min(y + block_y_size, height)

                r_sum = g_sum = b_sum = a_sum = 0
                pixel_count = 0

                for dy in range(y, y_end):
                    for dx in range(x, x_end):
                        r, g, b, a = pixels[dx, dy]
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        a_sum += a
                        pixel_count += 1

                r_avg = r_sum // pixel_count
                g_avg = g_sum // pixel_count
                b_avg = b_sum // pixel_count
                a_avg = a_sum // pixel_count

                for dy in range(y, y_end):
                    for dx in range(x, x_end):
                        new_pixels[dx, dy] = (r_avg, g_avg, b_avg, a_avg)

    elif compress == 1:
        new_width = width // block_x_size
        new_height = height // block_y_size

        new_image = Image.new('RGBA', (new_width, new_height))
        new_pixels = new_image.load()

        for y in range(0, height, block_y_size):
            for x in range(0, width, block_x_size):

                x_end = min(x + block_x_size, width)
                y_end = min(y + block_y_size, height)

                if x_end - x < block_x_size or y_end - y < block_y_size:
                    continue

                r_sum = g_sum = b_sum = a_sum = 0
                pixel_count = 0

                for dy in range(y, y_end):
                    for dx in range(x, x_end):
                        r, g, b, a = pixels[dx, dy]
                        r_sum += r
                        g_sum += g
                        b_sum += b
                        a_sum += a
                        pixel_count += 1

                r_avg = r_sum // pixel_count
                g_avg = g_sum // pixel_count
                b_avg = b_sum // pixel_count
                a_avg = a_sum // pixel_count

                new_x = x // block_x_size
                new_y = y // block_y_size

                if new_x < new_width and new_y < new_height:
                    new_pixels[new_x, new_y] = (r_avg, g_avg, b_avg, a_avg)

    image.next = create_image_list(new_image)
    label.current += 1
#pixelization
def pixelization_method(label,current_sub_method):
    if current_sub_method.tag == 'pixelization_standard':
        pixelization_standard_method_sub_method(label,current_sub_method)


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
    elif current_method == "Pixelization":
        pixelization_method(label, current_sub_method)