import tkinter
from math import cos
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
from proj_image_nodes import *
from proj_methodsfunc import *
from math import sin, cos, radians

is_started = False
current_index = -1

#перекрас png картынки в один цвет
def change_color_png_image(pil_image,RGB):
    width, height = pil_image.size
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    pixels_array = pil_image.load()
    for x in range(width):
        for y in range(height):
            if pixels_array[x, y][3] > 0:
                pixels_array[x,y] = (RGB[0],RGB[1],RGB[2],pixels_array[x,y][3])
    return pil_image

# ф подгона под размер окна при растягивании
def preview_image_resize_redo(event, frame, label):
    if label.image:
        frame_size = (frame.winfo_width() - 5, frame.winfo_height() - 5)
        main_image = get_image(label.head, label.current)
        pil_main_image = main_image.pil_image
        pil_image_resize = pil_main_image.resize(frame_size)
        tk_image_resize = ImageTk.PhotoImage(pil_image_resize)  # ресайзнутый тк файл
        label.config(image=tk_image_resize)
        label.image = tk_image_resize
# ф обработок кнопак
# ф начала обработки
def processing(event, combo, label, image_frame, image_label):
    current_method = get_method_name(event, combo)
    if label.image and current_method:
        from proj_gui_settings_descriptions import current_sub_method
        global is_started
        is_started = True
        use_method(event, current_method, label,current_sub_method)
        preview_image_resize_redo(event, image_frame, image_label)
        is_started = False
def start_button_on(event, canvas, button, text):  # навелись
    if not is_started:
        canvas.itemconfig(button, fill="white")
        canvas.itemconfig(text, fill="black")
def start_button_leave(event, canvas, button, text):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="black")
        canvas.itemconfig(text, fill="white")
def settings_button_on(event, canvas, button):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="white")
def settings_button_leave(event, canvas, button):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="black")
def description_button_on(event, canvas, button):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="white")
def description_button_leave(event, canvas, button):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="black")
def left_button_on(event, canvas, button,image):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="white")
        canvas.itemconfig(image, image=canvas.left_arrow_black)
def left_button_leave(event, canvas, button,image):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="black")
        canvas.itemconfig(image, image=canvas.left_arrow_white)
def right_button_on(event, canvas, button,image):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="white")
        canvas.itemconfig(image, image=canvas.right_arrow_black)
def right_button_leave(event, canvas, button,image):  # увелись
    if not is_started:
        canvas.itemconfig(button, fill="black")
        canvas.itemconfig(image, image=canvas.right_arrow_white)
# ф перемотки use_method
def left_image(event, frame, label):
    if label.image:
        if label.current > 0:
            label.current -= 1
            preview_image_resize_redo(event, frame, label)
def right_image(event, frame, label):
    if label.image:
        if label.current < length_image(label.head) - 1:
            label.current += 1
            preview_image_resize_redo(event, frame, label)
# ф создания menu
def create_menu(menu, list):
    for i in list:
        if "label" in i and "items" in i:
            submenu = tkinter.Menu(menu, tearoff=0)  # tearoff убераем линию
            menu.add_cascade(label=i["label"], menu=submenu)
            create_menu(submenu, i["items"])
        else:
            menu.add_command(label=i["label"], command=i["command"])
# ф создания кнопок
def create_top_left_button(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    points = [15, height // 2, 5, height // 2, 5, 5, width // 2 - 3, 5, width // 2 - 3, height // 4 - 5]
    """x = x₀ + a·cos(t)
       y = y₀ + b·sin(t)"""
    x_0 = width // 2 - 5
    y_0 = height // 2 - 5
    major_axis = (5 + width // 2) - 25
    minor_axis = -(height // 4)
    for i in range(90):
        i += 90
        points.append(x_0 + major_axis * cos(radians(i)))
        points.append(y_0 + minor_axis * sin(radians(i)))

    return points
def create_top_right_button(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    points = [width // 2 + 3, height // 4 - 5, width // 2 + 3, 5, width - 5, 5, width - 5, height // 2, width - 15,
              height // 2]
    """x = x₀ + a·cos(t)
       y = y₀ + b·sin(t)"""
    x_0 = width // 2 + 5
    y_0 = height // 2 - 5
    major_axis = (5 + width // 2) - 25
    minor_axis = -(height // 4)

    for i in range(90):
        points.append(x_0 + major_axis * cos(radians(i)))
        points.append(y_0 + minor_axis * sin(radians(i)))

    return points
def create_bottom_left_button(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    points = [width // 2 - 3, height*3 // 4 + 5, width // 2 - 3, height -5, 5, height-5, 5, height // 2+6, 15, height // 2+6]
    """x = x₀ + a·cos(t)
       y = y₀ + b·sin(t)"""
    x_0 = width // 2 - 5
    y_0 = height // 2 + 6
    major_axis = (5 + width // 2) - 25
    minor_axis = -(height // 4)

    for i in range(90):
        i +=180
        points.append(x_0 + major_axis * cos(radians(i)))
        points.append(y_0 + minor_axis * sin(radians(i)))
    return points
def create_bottom_right_button(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    points = [width-15, height // 2 + 6, width-5, height // 2 + 6, width-5, height - 5, width // 2 + 3, height - 5, width // 2 + 3, height * 3 // 4 + 5]
    """x = x₀ + a·cos(t)
       y = y₀ + b·sin(t)"""
    x_0 = width // 2 + 5
    y_0 = height // 2 + 6
    major_axis = (5 + width // 2) - 25
    minor_axis = -(height // 4)

    for i in range(90):
        i += 270
        points.append(x_0 + major_axis * cos(radians(i)))
        points.append(y_0 + minor_axis * sin(radians(i)))
    return points
# откр новый файл
def open_image_menu(frame, label):
    image_path = filedialog.askopenfilename(title="Выберите изображение",
                                            filetypes=[("Изображения", "*.jpg *.jpeg *.png")])
    if image_path:
        try:
            with Image.open(
                    image_path) as pil_main_image:  # основной файл через with чтоб обраб ошибку + закрыть файл авто
                frame_size = (frame.winfo_width() - 5, frame.winfo_height() - 5)
                main_image_resize = pil_main_image.resize(frame_size)
                tk_main_image_resize = ImageTk.PhotoImage(main_image_resize)  # ресайзнутый тк файл

                label.config(image=tk_main_image_resize)
                label.image = tk_main_image_resize
                label.head = create_image_list(pil_main_image)  # создаём для имг лист
                label.current = 0

        except:
            messagebox.showinfo("Ошибка", "Ошибка.")
    else:
        messagebox.showinfo("Ошибка", "Путь не выбран.")
def save_image_menu():
    pass
def guide_menu():
    pass
def about_menu():
    pass
def exit_menu(root):
    if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()
def ZZZZ():
    pass
