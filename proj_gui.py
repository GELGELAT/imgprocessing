import tkinter as tk
from proj_rootfunc import *
from proj_methodsfunc import *
from proj_gui_settings_descriptions import *
from tkinter import ttk
from PIL import *
from PIL import ImageTk, Image
import os


def RUN():
    root = tk.Tk()
    # настройка root
    root.title("Тиша нубус")

    screen_wight, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    k = round(screen_wight / screen_height, 2)

    # центровка + 0.8 от размера экрана
    root_wight, root_height = int(screen_wight * 0.8), int(screen_height * 0.8)
    x_centering, y_centering = (screen_wight // 2) - (root_wight // 2), (screen_height // 2) - (root_height // 2 + 30)
    root.geometry(f"{root_wight}x{root_height}+{x_centering}+{y_centering}")

    menu = tk.Menu(root)
    root.config(menu=menu)

    # основной main frame
    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(expand=True, fill="both")  # expand чтоб всё место занимало fill во все стороны

    # настройка весов для main
    main_frame.grid_rowconfigure(0, weight=1)  # верхний растяг по x и y
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=0)  # верхний растяг по x и y
    # создание верхнего frame
    top_frame = tk.Frame(main_frame, bg="white")
    top_frame.grid(row=0, column=0, sticky="nsew", padx=(2, 2), pady=(2, 2))
    top_frame.grid_propagate(False)  # игнорирует размеры дочерних виджетов combo

    # настройка весов для top
    top_frame.grid_columnconfigure(0, weight=1)  # левый растяг по x
    top_frame.grid_columnconfigure(1, weight=0)  # правый не растяг по x
    top_frame.grid_rowconfigure(0, weight=1)  # по y
    root.update()  # иначе размер фрейма одын
    # место для изображения и настроек

    image_frame = tk.Frame(top_frame, bg="black")
    image_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 2))
    image_frame.grid_propagate(False)  # игнорирует размеры дочерних виджетов
    # отображ картинки
    image_label = Label(image_frame)
    image_label.image = None
    image_label.grid(row=0, column=0)

    basic_frame = tk.Frame(top_frame, bg="white", width=int(top_frame.winfo_width() * 0.3))
    basic_frame.grid(row=0, column=1, sticky="nsew")
    basic_frame.grid_propagate(False)  # игнорирует размеры дочерних виджетов

    # настройка весов для basic
    basic_frame.grid_rowconfigure(0, weight=1)  # 1 растяг по y
    basic_frame.grid_rowconfigure(1, weight=0)  # 2 не растяг по y
    basic_frame.grid_columnconfigure(0, weight=1)  # растяг по x

    # место для выбораметода описания, старта, отмотки
    # выбораметода описания
    method_frame = tk.Frame(basic_frame, bg="white")
    method_frame.grid(row=0, column=0, sticky="nsew")
    method_frame.grid_propagate(False)  # игнорирует размеры дочерних виджетов

    # настройка весов для method
    method_frame.grid_rowconfigure(0, weight=0)
    method_frame.grid_rowconfigure(1, weight=1)
    method_frame.grid_rowconfigure(2, weight=0)
    method_frame.grid_columnconfigure(0, weight=1)

    # меню
    menu_frame = tk.Frame(method_frame, bg="black")
    menu_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 2))
    menu_frame.grid_propagate(False)  # игнорирует размеры дочерних виджетов
    menu_frame.grid_rowconfigure(0, weight=1)
    menu_frame.grid_columnconfigure(0, weight=1)
    # создаём через функции фреймы описания и нстроек
    description_frame = create_description_frame(menu_frame)
    settings_frame, sub_settings_frame, settings_canvas = create_settings_frame(menu_frame)

    sub_settings_frame.bind("<Configure>", lambda e, cnv=settings_canvas: update_scroll(e, cnv))
    settings_canvas.bind_all("<MouseWheel>", lambda e, cnv=settings_canvas: on_mousewheel(e, cnv))

    settings_canvas.bind("<Configure>", lambda e, cnv=settings_canvas: on_frame_from_canvas_width_resize(e,
                                                                                        cnv))  # изменяем размер субнастроечного фрейма

    # выбор метода
    combo = ttk.Combobox(method_frame, values=["Decoloration", "Color Mapping", "Pixelization"], state="readonly")
    combo.grid(row=0, column=0, sticky="nsew")
    combo.bind("<<ComboboxSelected>>", lambda e, com=combo, frm=description_frame: show_current_descriptions_text(e,
                                                                                                                  com,
                                                                                                                  frm),
               # отображ нужного описания
               add='+')
    combo.bind("<<ComboboxSelected>>", lambda e, com=combo, frm=sub_settings_frame: create_settings(e, com, frm),
               add='+')  # создание настроек
    combo.bind("<<ComboboxSelected>>", lambda e, com=combo,cnv=settings_canvas: show_current_settings(e, com,cnv),
               add='+')  # отображ нужных настроек


    # 1настройка

    # 2описание

    # canvas
    buttons_canvas = Canvas(basic_frame, bg="black", height=int(screen_height * 0.2))
    buttons_canvas.grid(row=1, column=0, sticky="nsew")
    buttons_canvas.grid_propagate(False)
    root.update()
    width = buttons_canvas.winfo_width()
    height = buttons_canvas.winfo_height()
    # создаём кастомные кнопки
    settings_button = buttons_canvas.create_polygon(create_top_left_button(buttons_canvas), width=2, outline="white",
                                                    fill="black")
    description_button = buttons_canvas.create_polygon(create_top_right_button(buttons_canvas), width=2,
                                                       outline="white",
                                                       fill="black")
    left_button = buttons_canvas.create_polygon(create_bottom_left_button(buttons_canvas), width=2, outline="white",
                                                fill="black")
    right_button = buttons_canvas.create_polygon(create_bottom_right_button(buttons_canvas), width=2, outline="white",
                                                 fill="black")

    # создаём стрелки
    script_dir = os.path.dirname(os.path.abspath(__file__))  # бсолютный путь до дериктория текущего файла
    image_path = os.path.join(script_dir, 'arrows.png')  # збор полного пути
    with Image.open(image_path) as pil_arrow_image:
        arrow_size = (width * 2 // 5, height * 2 // 5)
        arrow_image_resize = pil_arrow_image.resize(arrow_size)
        arrow_image_resize_left = arrow_image_resize.rotate(145)
        arrow_image_resize_right = arrow_image_resize.transpose(Image.FLIP_LEFT_RIGHT).rotate(-145)
        tk_arrow_image_resize_left_black = ImageTk.PhotoImage(arrow_image_resize_left)
        tk_arrow_image_resize_right_black = ImageTk.PhotoImage(arrow_image_resize_right)
        tk_arrow_image_resize_left_white = ImageTk.PhotoImage(
            change_color_png_image(arrow_image_resize_left, (255, 255, 255)))
        tk_arrow_image_resize_right_white = ImageTk.PhotoImage(
            change_color_png_image(arrow_image_resize_right, (255, 255, 255)))
        buttons_canvas.left_arrow_white = tk_arrow_image_resize_left_white
        buttons_canvas.left_arrow_black = tk_arrow_image_resize_left_black
        buttons_canvas.right_arrow_white = tk_arrow_image_resize_right_white
        buttons_canvas.right_arrow_black = tk_arrow_image_resize_right_black

    left_arrow = buttons_canvas.create_image(width // 4.5, height * 13 // 16, image=buttons_canvas.left_arrow_white)
    right_arrow = buttons_canvas.create_image(width // 1.28, height * 13 // 16, image=buttons_canvas.right_arrow_white)
    # настройка кнопок настроек описания
    settings_description_button_config = {
        settings_button: {
            "<Button-1>": lambda e, frm=settings_frame: show_settings_descriptions(e, frm),  # показ настроек
            "<Enter>": lambda e, cnv=buttons_canvas, btn=settings_button: settings_button_on(e, cnv, btn),  # покрас на
            "<Leave>": lambda e, cnv=buttons_canvas, btn=settings_button: settings_button_leave(e, cnv, btn)
            # покрас от
        },
        description_button: {
            "<Button-1>": lambda e, frm=description_frame: show_settings_descriptions(e, frm),  # показ описания
            "<Enter>": lambda e, cnv=buttons_canvas, btn=description_button: description_button_on(e, cnv, btn),
            "<Leave>": lambda e, cnv=buttons_canvas, btn=description_button: description_button_leave(e, cnv, btn)
        }}
    for item, events in settings_description_button_config.items():
        for event_name, handler in events.items():
            buttons_canvas.tag_bind(item, event_name, handler)
    # настройка кнопок отмотки и стрелок
    left_right_button_config = {
        left_arrow: {
            "<Button-1>": lambda e, frm=image_frame, lab=image_label: left_image(e, frm, lab),
            "<Enter>": lambda e, cnv=buttons_canvas, btn=left_button, img=left_arrow: left_button_on(e, cnv, btn, img),
            "<Leave>": lambda e, cnv=buttons_canvas, btn=left_button, img=left_arrow: left_button_leave(e, cnv, btn,
                                                                                                        img)
        },
        left_button: {
            "<Button-1>": lambda e, frm=image_frame, lab=image_label: left_image(e, frm, lab),
            "<Enter>": lambda e, cnv=buttons_canvas, btn=left_button, img=left_arrow: left_button_on(e, cnv, btn, img),
            "<Leave>": lambda e, cnv=buttons_canvas, btn=left_button, img=left_arrow: left_button_leave(e, cnv, btn,
                                                                                                        img)
        },
        right_button: {
            "<Button-1>": lambda e, frm=image_frame, lab=image_label: right_image(e, frm, lab),
            "<Enter>": lambda e, cnv=buttons_canvas, btn=right_button, img=right_arrow: right_button_on(e, cnv, btn,
                                                                                                        img),
            "<Leave>": lambda e, cnv=buttons_canvas, btn=right_button, img=right_arrow: right_button_leave(e, cnv, btn,
                                                                                                           img)
        }
        ,
        right_arrow: {
            "<Button-1>": lambda e, frm=image_frame, lab=image_label: right_image(e, frm, lab),
            "<Enter>": lambda e, cnv=buttons_canvas, btn=right_button, img=right_arrow: right_button_on(e, cnv, btn,
                                                                                                        img),
            "<Leave>": lambda e, cnv=buttons_canvas, btn=right_button, img=right_arrow: right_button_leave(e, cnv, btn,
                                                                                                           img)
        }
    }
    for item, events in left_right_button_config.items():
        for event_name, handler in events.items():
            buttons_canvas.tag_bind(item, event_name, handler)

    # кнопка старта + центровка
    start_button = buttons_canvas.create_oval(20, buttons_canvas.winfo_height() // 4, buttons_canvas.winfo_width() - 20,
                                              buttons_canvas.winfo_height() * 3 // 4, width=2,
                                              outline="white")
    text_start_btn = buttons_canvas.create_text(int(buttons_canvas.winfo_width() / 2),
                                                int(buttons_canvas.winfo_height() / 2), text="СТАРТ", fill="white",
                                                font=("Arial", int(k * 22)))
    # настройка старта
    for item in [start_button, text_start_btn]:
        buttons_canvas.tag_bind(item, "<Button-1>",
                                lambda e, com=combo,
                                       lab=image_label, ifrm=image_frame, ilab=image_label: processing(e,
                                                                                                       combo,
                                                                                                       lab,
                                                                                                       ifrm,
                                                                                                       ilab))

        buttons_canvas.tag_bind(item, "<Enter>",
                                lambda e, cnv=buttons_canvas, btn=start_button, txt=text_start_btn: start_button_on(e,
                                                                                                                    cnv,
                                                                                                                    btn,
                                                                                                                    txt))
        buttons_canvas.tag_bind(item, "<Leave>",
                                lambda e, cnv=buttons_canvas, btn=start_button, txt=text_start_btn: start_button_leave(
                                    e,
                                    cnv,
                                    btn,
                                    txt))

    # создание нижнего фрейма
    bottom_frame = tk.Frame(main_frame, bg="black", height=int(screen_height * 0.05))
    bottom_frame.grid(row=2, column=0, sticky="nsew", padx=(2, 2), pady=(0, 2))
    bottom_frame.grid_propagate(False)

    # добавляем menu
    # Файл: Открыть сохранить выход, О программе
    menu_list = [{"label": "Файл",
                  "items": [
                      {"label": "Открыть",
                       "command": lambda frm=image_frame, lab=image_label: open_image_menu(frm, lab)},
                      {"label": "Сохранить", "command": save_image_menu},
                      {"label": "Выход", "command": lambda: exit_menu(root)}]},
                 {"label": "Справка", "items": [{"label": "Как пользоваться", "command": guide_menu},
                                                {"label": "О программе", "command": about_menu}]}]
    create_menu(menu, menu_list)
    # когда меняем размер окна
    root.bind("<Configure>", lambda e, frm=image_frame, lab=image_label: preview_image_resize_redo(e, frm, lab))

    root.mainloop()
