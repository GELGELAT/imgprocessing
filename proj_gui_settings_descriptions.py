from tkinter import *
from tkinter import scrolledtext,colorchooser
from proj_methodsfunc import get_method_name
from proj_custommethods import *
from json import loads
current_sub_method = create_current_sub_method(None, None)

FRAMES = {}



base_decoloration = {}
base_color_mapping = {}

created_methods = {}
created_sub_methods_settings = {}
base_methods = {
    'decoloration': {},
    'color_mapping': {}
}
settings_frames_store = {}


# справка насчёт канваса и отрисовки в нём фрейма. когда мы поместили фрейм в 00 в канвасе мы должны указать размеры канвасу этого фрейма поэтому
# нужна вызвать функцию которая обнавляет поле прокрутки, но если фрейм маленький то канвас не даёт выйти ему за свои пределы и пояляется ощущение
# что он начинает убегать в низ, но на самом деле мы просто не даём выйти нашему фрейму за канвас


def create_settings_frame(frame):  # ф для создания фрейма настроек, во фрейм передайм окно настроек и описаний
    # архитектура настроек
    # settings_frame(для выбора нужного фрейма настройки описание) <
    # < settings_canvas(для скролинга подстраивается под sub_settings_frame) <
    # < sub_settings_frame(создаются и отображаются сабы, подстраивается под sub_frames) <
    # < sub_frames <
    # < (1)choosing_sub_method_button, (2)sub method settings_button (когда жмём на (1) появляются флажки,(2) настройки выброного флажка

    global settings_frame, settings_canvas, sub_settings_frame
    settings_frame = Frame(frame, bg="black")
    settings_frame.grid(row=0, column=0, sticky="nsew")
    settings_frame.name = 'settings_frame'
    settings_frame.grid_rowconfigure(0, weight=1)
    settings_frame.grid_columnconfigure(0, weight=1)

    settings_canvas = Canvas(settings_frame, bg="black")
    settings_scrollbar = Scrollbar(settings_frame, orient="vertical",
                                   command=settings_canvas.yview)  # command=settings_canvas.yview управл канвосом
    settings_canvas.configure(yscrollcommand=settings_scrollbar.set)  # говорим скролбару о канвасе
    settings_canvas.grid(row=0, column=0, sticky="nsew")
    settings_scrollbar.grid(row=0, column=1, sticky="ns")

    sub_settings_frame = Frame(settings_canvas, bg="black")
    sub_settings_frame.grid_rowconfigure(0, weight=1)
    sub_settings_frame.grid_columnconfigure(0, weight=1)
    settings_canvas.create_window((0, 0), window=sub_settings_frame, anchor="nw")

    return settings_frame, sub_settings_frame, settings_canvas


def sub_choosing_button_on(frame_list):
    settings_canvas.yview("moveto", 0)  # сбрасываем прокрутку до нуля
    if frame_list[1] == 1:
        frame_list[0].grid_remove()
        frame_list[1] = 0

    else:
        frame_list[0].grid()
        frame_list[1] = 1


# устройство кастомизации: название, индекс, саб мктод, настройки
# когда создаём фрейм с выбором флажков проходимся по списку и создаём флажки
# когда создаём новый метод, добавляем новый флажок и создаём новый метод с именем сабметод+индекстег
# когда вызываем метод передаём в функцию наш обект


create_and_store_methods(base_decoloration, 'Standard', 0, 'decoloration_standard', [255, 0])
create_and_store_methods(base_decoloration, 'Standard1', 1, 'decoloration_standard', [128, 128])
create_and_store_methods(base_decoloration, 'Weighted', 0, 'decoloration_weighted', [0.299, 0.587, 0.114])

create_and_store_methods(base_color_mapping, 'Two colors', 0, 'color_mapping_two_colors',
                         [[132, 71, 21], [59, 20, 6], 150])


def show_current_sub_method_settings_frame():
    for page, method in created_sub_methods_settings.items():
        method.grid_remove()
    created_sub_methods_settings.get(current_sub_method.tag).grid()


def create_sub_method_buttons(current_method, parent_frame, frame):
    reset_button = Button(frame, text='Reset')
    reset_button.grid(row=0, column=0, sticky="nsew")

    save_button = Button(frame, text='Save')
    save_button.grid(row=0, column=1, sticky="nsew")

    apply_button = Button(frame, text='Apply')
    apply_button.grid(row=0, column=2, sticky="nsew")

    apply_button.bind("<Button-1>", lambda e: sub_method_settings_change())

    save_button.bind("<Button-1>",
                     lambda e, current_method=current_method, frame=parent_frame: save_sub_method_settings(
                         current_method, frame))

    reset_button.bind("<Button-1>",
                      lambda e, frm=frame, current_method=current_method: reset_sub_method_settings(current_method))


def get_var_from_sub_method_settings():
    result_settings = []

    for variables in variables_settings:
        result_settings.append(variables.get())

    return result_settings


def sub_method_settings_change():
    result_settings = get_var_from_sub_method_settings()


    if current_sub_method.tag == 'decoloration_standard':
        i = 0
        for result in result_settings:
            current_sub_method.object.settings[i] = int(result)
            i += 1
    elif current_sub_method.tag == 'decoloration_weighted':
        i = 0
        for result in result_settings:
            current_sub_method.object.settings[i] = float(result)
            i += 1
    elif current_sub_method.tag == 'color_mapping_two_colors':
        i = 0
        for result in result_settings:
            current_sub_method.object.settings[i] = result
            i += 1


def validate_input(var, *args):
    value = var.get()
    # Оставляем только цифры


    if current_sub_method.tag == 'decoloration_standard':
        filtered = ''.join(filter(str.isdigit, value))
        if value != filtered:
            var.set(filtered)
        '''if var.get() == '':
            var.set('1')
        if int(var.get()[0]) == 0:
            var.set('1')'''
        if 255 < int(var.get()):
            var.set('255')
        elif int(var.get()) < 0:
            var.set('0')
    elif current_sub_method.tag == 'decoloration_weighted':
        filtered = ''.join(i for i in value if i.isdigit() or i == '.')
        if filtered.count('.') > 1:
            filtered = value.replace('.', '', 1)

        if value != filtered:
            var.set(filtered)

def rgb_to_hex(lst):
    # Если пришла строка — парсим
    if isinstance(lst, str):
        lst = loads(lst)
    return f"#{lst[0]:02x}{lst[1]:02x}{lst[2]:02x}"
#[132, 71, 21], [59, 20, 6] variables_settings
def choose_color(index,lbl,lst):
    color = colorchooser.askcolor(title="Выберите цвет")
    if color:
        current_sub_method.object.settings[index] = list(color[0])
        lst[index] = StringVar(value=str(list(color[0])))
        lbl.config(bg=color[1])

def create_sub_method_settings(frame):
    global variables_settings
    variables_settings = []
    if current_sub_method.tag == 'decoloration_standard':
        i = 0
        for label_text, value in {'upper paint limit (max:255):': current_sub_method.object.settings[0],
                                  'lower paint border (min:0):': current_sub_method.object.settings[1]}.items():
            label = Label(frame, text=label_text, bg='black', fg='white')
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            var_settings = StringVar(value=value)
            var_settings.trace('w', lambda *args, v=var_settings: validate_input(v))
            variables_settings.append(var_settings)
            entry = Entry(frame, textvariable=var_settings)
            entry.grid(row=i, column=1, padx=10, pady=5)
            i += 1
    elif current_sub_method.tag == 'decoloration_weighted':
        i = 0
        for label_text, value in {'color channel R :': current_sub_method.object.settings[0],
                                  'color channel G:': current_sub_method.object.settings[1],
                                  'color channel B:': current_sub_method.object.settings[2]}.items():
            label = Label(frame, text=label_text, bg='black', fg='white')
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            var_settings = StringVar(value=value)
            var_settings.trace('w', lambda *args, v=var_settings: validate_input(v))
            variables_settings.append(var_settings)
            entry = Entry(frame, textvariable=var_settings)
            entry.grid(row=i, column=1, padx=10, pady=5)
            i += 1
    elif current_sub_method.tag == 'color_mapping_two_colors':
        first_color_display = Label(frame, bg=rgb_to_hex(current_sub_method.object.settings[0]), width=5, height=2, relief="sunken")
        first_color_display.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        second_color_display = Label(frame, bg=rgb_to_hex(current_sub_method.object.settings[1]), width=5, height=2, relief="sunken")
        second_color_display.grid(row=1, column=1, padx=10, pady=5, sticky="e")



        for label_text, value in {'first_color:': current_sub_method.object.settings[0],
                                  'second_color:': current_sub_method.object.settings[1]}.items():
            var_settings = StringVar(value=f'{value}')
            entry = Entry(frame, textvariable=var_settings)
            variables_settings.append(var_settings)

        first_color = Button(frame, text="Choose first color",
                             command=lambda lbl=first_color_display,lst=variables_settings: choose_color(0, lbl,lst))
        first_color.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        second_color = Button(frame, text="Choose second color",
                              command=lambda lbl=second_color_display,lst=variables_settings: choose_color(1, lbl,lst))
        second_color.grid(row=1, column=0, padx=10, pady=5, sticky="w")


        for label_text, value in {'Limit:': current_sub_method.object.settings[2]}.items():
            label = Label(frame, text=label_text, bg='black', fg='white')
            label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

            var_settings = StringVar(value=str(value))
            var_settings.trace('w', lambda *args, v=var_settings: validate_input(v))
            variables_settings.append(var_settings)
            entry = Entry(frame, textvariable=var_settings)
            entry.grid(row=2, column=1, padx=10, pady=5)




def reset_sub_method_settings(current_method):
    if current_sub_method.tag == 'decoloration_standard':
        sub_method = current_sub_method.object
        sub_method.settings = ['255', '0']
        create_sub_method_settings_frame(current_method, sub_settings_frame)
    elif current_sub_method.tag == 'decoloration_weighted':
        sub_method = current_sub_method.object
        sub_method.settings = ['0.299', '0.587', '0.114']
        create_sub_method_settings_frame(current_method, sub_settings_frame)


# decoloration_sub_frame.choosing_frame
def save_sub_method_settings(current_method, frame):
    if current_sub_method.tag == 'decoloration_standard' or current_sub_method.tag == 'decoloration_weighted':
        sub_method = current_sub_method.object

        result_settings = get_var_from_sub_method_settings()

        create_and_store_methods(base_decoloration, f'{sub_method.name}',
                                 find_smallest_index(base_decoloration, f'{sub_method.tag}'), f'{sub_method.tag}',
                                 result_settings)
        choosing_frame = decoloration_sub_frame.choosing_frame[0]
        choosing_frame.destroy()
        decoloration_sub_choosing_frame = Frame(decoloration_sub_frame, bg="black")
        decoloration_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
        decoloration_sub_choosing_frame.grid_rowconfigure(0, weight=1)
        decoloration_sub_choosing_frame.grid_columnconfigure(0, weight=1)

        index = 0
        for values in base_decoloration.values():
            for current_custom in values.values():
                decoloration_sub_choosing_frame.grid_rowconfigure(index, weight=1)

                current = Radiobutton(
                    decoloration_sub_choosing_frame,
                    text=current_custom.name,
                    variable=frame.decoloration_current_sub_method,
                    value=get_united_sub_method_name(current_custom.index, current_custom.tag),
                    bg="black",
                    fg="white",
                    selectcolor="gray",
                    activebackground="black",
                    anchor='w',  # слева
                    command=lambda current_method=current_method, frm=frame: get_current_sub_method(current_method,
                                                                                                    frm)
                )
                current.grid(row=index, column=0, sticky="ew")
                index += 1
        decoloration_sub_frame.choosing_frame[0] = decoloration_sub_choosing_frame
    elif current_sub_method.tag == 'color_mapping_two_colors':
        sub_method = current_sub_method.object

        result_settings = get_var_from_sub_method_settings()

        create_and_store_methods(base_color_mapping, f'{sub_method.name}',
                                 find_smallest_index(base_color_mapping, f'{sub_method.tag}'), f'{sub_method.tag}',
                                 result_settings)
        print(result_settings)

        choosing_frame = color_mapping_sub_frame.choosing_frame[0]
        choosing_frame.destroy()
        color_mapping_sub_choosing_frame = Frame(color_mapping_sub_frame, bg="black")
        color_mapping_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
        color_mapping_sub_choosing_frame.grid_rowconfigure(0, weight=1)
        color_mapping_sub_choosing_frame.grid_columnconfigure(0, weight=1)

        index = 0
        for values in base_color_mapping.values():
            for current_custom in values.values():
                color_mapping_sub_choosing_frame.grid_rowconfigure(index, weight=1)

                current = Radiobutton(
                    color_mapping_sub_choosing_frame,
                    text=current_custom.name,
                    variable=frame.color_mapping_current_sub_method,
                    value=get_united_sub_method_name(current_custom.index, current_custom.tag),
                    bg="black",
                    fg="white",
                    selectcolor="gray",
                    activebackground="black",
                    anchor='w',  # слева
                    command=lambda current_method=current_method, frm=frame: get_current_sub_method(current_method,
                                                                                                    frm)
                )
                current.grid(row=index, column=0, sticky="ew")
                index += 1
        color_mapping_sub_frame.choosing_frame[0] = color_mapping_sub_choosing_frame

def create_sub_method_settings_frame(current_method, frame):  # decoloration_weighted
    if current_sub_method.tag == 'decoloration_standard':
        if hasattr(frame.decoloration_sub_frame, 'main_decoloration_standard_setting_frame'):
            frame.decoloration_sub_frame.main_decoloration_standard_setting_frame.sub_decoloration_standard_setting_frame.decoloration_standard_setting_frame.destroy()
            decoloration_standard_setting_frame = Frame(
                frame.decoloration_sub_frame.main_decoloration_standard_setting_frame.sub_decoloration_standard_setting_frame,
                bg="black", height=100)
            decoloration_standard_setting_frame.grid(row=0, column=0, sticky="nsew")
            decoloration_standard_setting_frame.grid_columnconfigure(0, weight=1)

            frame.decoloration_sub_frame.main_decoloration_standard_setting_frame.decoloration_standard_setting_frame = decoloration_standard_setting_frame
            create_sub_method_settings(decoloration_standard_setting_frame)

            show_current_sub_method_settings_frame()
        else:
            main_decoloration_standard_setting_frame = Frame(decoloration_sub_settings_frame, bg='black')
            main_decoloration_standard_setting_frame.grid(row=0, column=0, sticky="nsew")
            main_decoloration_standard_setting_frame.grid_rowconfigure(1, weight=1)
            main_decoloration_standard_setting_frame.grid_columnconfigure(0, weight=1)
            main_decoloration_standard_setting_frame.grid_rowconfigure(0, weight=1)

            frame.decoloration_sub_frame.main_decoloration_standard_setting_frame = main_decoloration_standard_setting_frame
            created_sub_methods_settings.update(
                {'decoloration_standard': frame.decoloration_sub_frame.main_decoloration_standard_setting_frame})
            sub_decoloration_standard_setting_frame = Frame(main_decoloration_standard_setting_frame, bg="black")
            sub_decoloration_standard_setting_frame.grid(row=0, column=0, sticky="nsew")
            sub_decoloration_standard_setting_frame.grid_rowconfigure(0, weight=1)
            sub_decoloration_standard_setting_frame.grid_columnconfigure(0, weight=1)
            sub_decoloration_standard_setting_frame.grid_rowconfigure(1, weight=1)
            frame.decoloration_sub_frame.main_decoloration_standard_setting_frame.sub_decoloration_standard_setting_frame = sub_decoloration_standard_setting_frame
            decoloration_standard_setting_frame = Frame(sub_decoloration_standard_setting_frame, bg="black", height=100)
            decoloration_standard_setting_frame.grid(row=0, column=0, sticky="nsew")
            decoloration_standard_setting_frame.grid_columnconfigure(0, weight=1)

            decoloration_standard_setting_button_frame = Frame(sub_decoloration_standard_setting_frame, bg="black",
                                                               height=100)
            decoloration_standard_setting_button_frame.grid(row=1, column=0, sticky="nsew")
            decoloration_standard_setting_button_frame.grid_columnconfigure(0, weight=1)
            decoloration_standard_setting_button_frame.grid_columnconfigure(1, weight=1)
            decoloration_standard_setting_button_frame.grid_columnconfigure(2, weight=1)
            frame.decoloration_sub_frame.main_decoloration_standard_setting_frame.sub_decoloration_standard_setting_frame.decoloration_standard_setting_frame = decoloration_standard_setting_frame
            create_sub_method_settings(decoloration_standard_setting_frame)
            create_sub_method_buttons(current_method, frame, decoloration_standard_setting_button_frame)
            show_current_sub_method_settings_frame()
    elif current_sub_method.tag == 'decoloration_weighted':
        if current_sub_method.tag == 'decoloration_weighted':
            if hasattr(frame.decoloration_sub_frame, 'main_decoloration_weighted_setting_frame'):
                frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame.sub_decoloration_weighted_setting_frame.decoloration_weighted_setting_frame.destroy()
                decoloration_weighted_setting_frame = Frame(
                    frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame.sub_decoloration_weighted_setting_frame,
                    bg="black", height=100)
                decoloration_weighted_setting_frame.grid(row=0, column=0, sticky="nsew")
                decoloration_weighted_setting_frame.grid_columnconfigure(0, weight=1)

                frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame.decoloration_weighted_setting_frame = decoloration_weighted_setting_frame
                create_sub_method_settings(decoloration_weighted_setting_frame)

                show_current_sub_method_settings_frame()
            else:
                main_decoloration_weighted_setting_frame = Frame(decoloration_sub_settings_frame, bg='black')
                main_decoloration_weighted_setting_frame.grid(row=0, column=0, sticky="nsew")
                main_decoloration_weighted_setting_frame.grid_rowconfigure(1, weight=1)
                main_decoloration_weighted_setting_frame.grid_columnconfigure(0, weight=1)
                main_decoloration_weighted_setting_frame.grid_rowconfigure(0, weight=1)

                frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame = main_decoloration_weighted_setting_frame
                created_sub_methods_settings.update(
                    {'decoloration_weighted': frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame})
                sub_decoloration_weighted_setting_frame = Frame(main_decoloration_weighted_setting_frame, bg="black")
                sub_decoloration_weighted_setting_frame.grid(row=0, column=0, sticky="nsew")
                sub_decoloration_weighted_setting_frame.grid_rowconfigure(0, weight=1)
                sub_decoloration_weighted_setting_frame.grid_columnconfigure(0, weight=1)
                sub_decoloration_weighted_setting_frame.grid_rowconfigure(1, weight=1)
                frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame.sub_decoloration_weighted_setting_frame = sub_decoloration_weighted_setting_frame
                decoloration_weighted_setting_frame = Frame(sub_decoloration_weighted_setting_frame, bg="black",
                                                            height=100)
                decoloration_weighted_setting_frame.grid(row=0, column=0, sticky="nsew")
                decoloration_weighted_setting_frame.grid_columnconfigure(0, weight=1)

                decoloration_weighted_setting_button_frame = Frame(sub_decoloration_weighted_setting_frame, bg="black",
                                                                   height=100)
                decoloration_weighted_setting_button_frame.grid(row=1, column=0, sticky="nsew")
                decoloration_weighted_setting_button_frame.grid_columnconfigure(0, weight=1)
                decoloration_weighted_setting_button_frame.grid_columnconfigure(1, weight=1)
                decoloration_weighted_setting_button_frame.grid_columnconfigure(2, weight=1)
                frame.decoloration_sub_frame.main_decoloration_weighted_setting_frame.sub_decoloration_weighted_setting_frame.decoloration_weighted_setting_frame = decoloration_weighted_setting_frame
                create_sub_method_settings(decoloration_weighted_setting_frame)
                create_sub_method_buttons(current_method, frame, decoloration_weighted_setting_button_frame)
                show_current_sub_method_settings_frame()
    elif current_sub_method.tag == 'color_mapping_two_colors':
        if hasattr(frame.color_mapping_sub_frame, 'main_color_mapping_two_colors_setting_frame'):
            frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame.sub_color_mapping_two_colors_setting_frame.color_mapping_two_colors_setting_frame.destroy()
            color_mapping_two_colors_setting_frame = Frame(
                frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame.sub_color_mapping_two_colors_setting_frame,
                bg="black", height=100)
            color_mapping_two_colors_setting_frame.grid(row=0, column=0, sticky="nsew")
            color_mapping_two_colors_setting_frame.grid_columnconfigure(0, weight=1)

            frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame.color_mapping_two_colors_setting_frame = color_mapping_two_colors_setting_frame
            create_sub_method_settings(color_mapping_two_colors_setting_frame)

            show_current_sub_method_settings_frame()
        else:
            main_color_mapping_two_colors_setting_frame = Frame(color_mapping_sub_settings_frame, bg='black')
            main_color_mapping_two_colors_setting_frame.grid(row=0, column=0, sticky="nsew")
            main_color_mapping_two_colors_setting_frame.grid_rowconfigure(1, weight=1)
            main_color_mapping_two_colors_setting_frame.grid_columnconfigure(0, weight=1)
            main_color_mapping_two_colors_setting_frame.grid_rowconfigure(0, weight=1)

            frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame = main_color_mapping_two_colors_setting_frame
            created_sub_methods_settings.update(
                {'color_mapping_two_colors': frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame})
            sub_color_mapping_two_colors_setting_frame = Frame(main_color_mapping_two_colors_setting_frame, bg="black")
            sub_color_mapping_two_colors_setting_frame.grid(row=0, column=0, sticky="nsew")
            sub_color_mapping_two_colors_setting_frame.grid_rowconfigure(0, weight=1)
            sub_color_mapping_two_colors_setting_frame.grid_columnconfigure(0, weight=1)
            sub_color_mapping_two_colors_setting_frame.grid_rowconfigure(1, weight=1)
            frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame.sub_color_mapping_two_colors_setting_frame = sub_color_mapping_two_colors_setting_frame
            color_mapping_two_colors_setting_frame = Frame(sub_color_mapping_two_colors_setting_frame, bg="black",
                                                        height=100)
            color_mapping_two_colors_setting_frame.grid(row=0, column=0, sticky="nsew")
            color_mapping_two_colors_setting_frame.grid_columnconfigure(0, weight=1)

            color_mapping_two_colors_setting_button_frame = Frame(sub_color_mapping_two_colors_setting_frame, bg="black",
                                                               height=100)
            color_mapping_two_colors_setting_button_frame.grid(row=1, column=0, sticky="nsew")
            color_mapping_two_colors_setting_button_frame.grid_columnconfigure(0, weight=1)
            color_mapping_two_colors_setting_button_frame.grid_columnconfigure(1, weight=1)
            color_mapping_two_colors_setting_button_frame.grid_columnconfigure(2, weight=1)
            frame.color_mapping_sub_frame.main_color_mapping_two_colors_setting_frame.sub_color_mapping_two_colors_setting_frame.color_mapping_two_colors_setting_frame = color_mapping_two_colors_setting_frame
            create_sub_method_settings(color_mapping_two_colors_setting_frame)
            create_sub_method_buttons(current_method, frame, color_mapping_two_colors_setting_button_frame)
            show_current_sub_method_settings_frame()


# method_name rb_key
def create_settings(event, combo, frame):  # когда жмякаем на кобобокс создаётся нкжное окно с флажками
    global created_methods, decoloration_sub_settings_frame, color_mapping_sub_settings_frame, decoloration_sub_frame,color_mapping_sub_frame
    current_method = get_method_name(event, combo)
    if current_method == "Decoloration":
        if hasattr(frame, 'decoloration_sub_frame'):
            frame.current_sub_method = frame.decoloration_current_sub_method.get()
            get_current_sub_method(current_method, frame)
        else:
            quantity_sub_methods = get_quantity_sub_methods(base_decoloration)
            frame.decoloration_current_sub_method = StringVar(value='decoloration_standard_0')
            decoloration_sub_frame = Frame(frame, bg="black")
            decoloration_sub_frame.grid(row=0, column=0, sticky="nsew")

            decoloration_sub_choosing_button = Button(decoloration_sub_frame,
                                                      textvariable=frame.decoloration_current_sub_method)
            decoloration_sub_choosing_button.grid(row=0, column=0, sticky="nsew")

            decoloration_sub_choosing_frame = Frame(decoloration_sub_frame, bg="black")
            decoloration_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
            decoloration_sub_choosing_frame.grid_rowconfigure(0, weight=1)
            decoloration_sub_choosing_frame.grid_columnconfigure(0, weight=1)
            decoloration_sub_settings_button = Button(decoloration_sub_frame, text='Settings')

            decoloration_sub_settings_button.grid(row=2, column=0, sticky="nsew")

            decoloration_sub_settings_frame = Frame(decoloration_sub_frame, bg="dark red")

            decoloration_sub_settings_frame.grid(row=3, column=0, sticky="nsew")
            decoloration_sub_settings_frame.grid_rowconfigure(0, weight=1)
            decoloration_sub_settings_frame.grid_columnconfigure(0, weight=1)
            decoloration_sub_settings_frame.grid_remove()

            decoloration_sub_frame.choosing_frame = [decoloration_sub_choosing_frame, 1]
            decoloration_sub_frame.settings_frame = [decoloration_sub_settings_frame, 0]
            decoloration_sub_choosing_button.bind("<Button-1>",
                                                  lambda e,
                                                         lst=decoloration_sub_frame.choosing_frame: sub_choosing_button_on(
                                                      lst))
            decoloration_sub_settings_button.bind("<Button-1>",
                                                  lambda e,
                                                         lst=decoloration_sub_frame.settings_frame: sub_choosing_button_on(
                                                      lst))

            for i in range(quantity_sub_methods):
                decoloration_sub_frame.grid_rowconfigure(i, weight=1)
            decoloration_sub_frame.grid_columnconfigure(0, weight=1)

            frame.decoloration_sub_frame = decoloration_sub_frame
            frame.current_sub_method = 'decoloration_standard'
            created_methods.update({'Decoloration': frame.decoloration_sub_frame})

            index = 0
            for values in base_decoloration.values():
                for current_custom in values.values():
                    current = Radiobutton(
                        decoloration_sub_choosing_frame,
                        text=current_custom.name,
                        variable=frame.decoloration_current_sub_method,
                        value=get_united_sub_method_name(current_custom.index, current_custom.tag),
                        bg="black",
                        fg="white",
                        selectcolor="gray",
                        activebackground="black",
                        anchor='w',  # слева
                        command=lambda current_method=current_method, frm=frame: get_current_sub_method(current_method,
                                                                                                        frm)
                    )
                    current.grid(row=index, column=0, sticky="ew")
                    index += 1

            get_current_sub_method(current_method, frame)
    elif current_method == "Color Mapping":  # color_mapping
        if current_method == "Color Mapping":
            if hasattr(frame, 'color_mapping_sub_frame'):
                frame.current_sub_method = frame.color_mapping_current_sub_method.get()
                get_current_sub_method(current_method, frame)
            else:
                quantity_sub_methods = get_quantity_sub_methods(base_color_mapping)
                frame.color_mapping_current_sub_method = StringVar(value='color_mapping_two_colors_0')
                color_mapping_sub_frame = Frame(frame, bg="black")
                color_mapping_sub_frame.grid(row=0, column=0, sticky="nsew")

                color_mapping_sub_choosing_button = Button(color_mapping_sub_frame,
                                                          textvariable=frame.color_mapping_current_sub_method)
                color_mapping_sub_choosing_button.grid(row=0, column=0, sticky="nsew")

                color_mapping_sub_choosing_frame = Frame(color_mapping_sub_frame, bg="black")
                color_mapping_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
                color_mapping_sub_choosing_frame.grid_rowconfigure(0, weight=1)
                color_mapping_sub_choosing_frame.grid_columnconfigure(0, weight=1)
                color_mapping_sub_settings_button = Button(color_mapping_sub_frame, text='Settings')

                color_mapping_sub_settings_button.grid(row=2, column=0, sticky="nsew")

                color_mapping_sub_settings_frame = Frame(color_mapping_sub_frame, bg="dark red")

                color_mapping_sub_settings_frame.grid(row=3, column=0, sticky="nsew")
                color_mapping_sub_settings_frame.grid_rowconfigure(0, weight=1)
                color_mapping_sub_settings_frame.grid_columnconfigure(0, weight=1)
                color_mapping_sub_settings_frame.grid_remove()

                color_mapping_sub_frame.choosing_frame = [color_mapping_sub_choosing_frame, 1]
                color_mapping_sub_frame.settings_frame = [color_mapping_sub_settings_frame, 0]
                color_mapping_sub_choosing_button.bind("<Button-1>",
                                                      lambda e,
                                                             lst=color_mapping_sub_frame.choosing_frame: sub_choosing_button_on(
                                                          lst))
                color_mapping_sub_settings_button.bind("<Button-1>",
                                                      lambda e,
                                                             lst=color_mapping_sub_frame.settings_frame: sub_choosing_button_on(
                                                          lst))

                for i in range(quantity_sub_methods):
                    color_mapping_sub_frame.grid_rowconfigure(i, weight=1)
                color_mapping_sub_frame.grid_columnconfigure(0, weight=1)

                frame.color_mapping_sub_frame = color_mapping_sub_frame
                frame.current_sub_method = 'color_mapping_two_colors'
                created_methods.update({'Color Mapping': frame.color_mapping_sub_frame})

                index = 0
                for values in base_color_mapping.values():
                    for current_custom in values.values():
                        current = Radiobutton(
                            color_mapping_sub_choosing_frame,
                            text=current_custom.name,
                            variable=frame.color_mapping_current_sub_method,
                            value=get_united_sub_method_name(current_custom.index, current_custom.tag),
                            bg="black",
                            fg="white",
                            selectcolor="gray",
                            activebackground="black",
                            anchor='w',  # слева
                            command=lambda current_method=current_method, frm=frame: get_current_sub_method(
                                current_method,
                                frm)
                        )
                        current.grid(row=index, column=0, sticky="ew")
                        index += 1

                get_current_sub_method(current_method, frame)


def create_description_frame(frame):  # ф создаёт фрейм с описанием в котором лежит скролтекст
    width, height = frame.winfo_width(), frame.winfo_height()
    global description_frame
    description_frame = Frame(frame, bg="black")
    description_frame.grid(row=0, column=0, sticky="nsew")
    description_frame.grid_propagate(False)
    description_frame.grid_rowconfigure(0, weight=1)
    description_frame.grid_columnconfigure(0, weight=1)
    description_frame.name = 'description_frame'
    description_text_area = scrolledtext.ScrolledText(description_frame, width=width, height=height, wrap=WORD,
                                                      bg="black")
    description_text_area.grid(row=0, column=0, sticky="nsew")
    description_text_area.insert(END, "Выберити метод обработки")
    description_text_area.config(state=DISABLED)
    description_frame.text = description_text_area
    return description_frame


def on_frame_from_canvas_width_resize(event, canvas):
    canvas.itemconfig(1, width=event.width)  # event.width новая ширина cansvs


def on_frame_from_canvas_height_resize(event, canvas):
    canvas.itemconfig(1, width=event.width)  # event.width новая ширина cansvs


def update_scroll(event, canvas):
    canvas.configure(
        scrollregion=canvas.bbox("all"))  # устанавливаем размеры прокручивания all возращает размеры фрейма в канвасе


def on_mousewheel(event, canvas):
    bbox = canvas.bbox("all")

    content_height = bbox[3] - bbox[1]  # высота содержимого
    canvas_height = canvas.winfo_height()
    if content_height <= canvas_height:
        return
    canvas.yview("scroll", int(-1 * (event.delta / 120)), "units")  # event.delta величина прокрутки колесика мыши


def get_current_sub_method(current_method, frame):  # полуаем текущий саб метод
    global current_sub_method
    if current_method == 'Decoloration':
        current_sub_method.tag = get_split_sub_method_name(frame.decoloration_current_sub_method.get())[0]
        current_sub_method.object = find_current_sub_method(base_decoloration,
                                                            frame.decoloration_current_sub_method.get())
    elif current_method == "Color Mapping":
        current_sub_method.tag = get_split_sub_method_name(frame.color_mapping_current_sub_method.get())[0]
        current_sub_method.object = find_current_sub_method(base_color_mapping,
                                                            frame.color_mapping_current_sub_method.get())
    create_sub_method_settings_frame(current_method, frame)


def show_current_settings(event, combo, canvas):  # для отображения нжного окна настроек
    canvas.yview("moveto", 0)  # сбрасываем прокрутку до нуля
    current_method = get_method_name(event, combo)
    for page, method in created_methods.items():
        method.grid_remove()
    created_methods.get(current_method).grid()


def show_current_descriptions_text(event, combo, frame):  # для нужного текста
    current_method = get_method_name(event, combo)
    frame.text.config(state=NORMAL)
    frame.text.delete(1.0, END)
    if current_method == "Decoloration":
        frame.text.insert(END,
                          """Standard: Функция выполняет обесцвечивание изображения: преобразует цветную картинку в оттенки серого (чёрно-белый формат) с сохранением яркостной структуры исходного кадра.
                          Weighted: Функция выполняет обесцвечивание изображения на основе взвешенного суммирования цветовых каналов: каждый пиксель преобразуется в оттенки серого по формуле яркости L = 0.299*R + 0.587*G + 0.114*B, где коэффициенты подобраны с учётом физиологического восприятия яркости человеческим глазом, что позволяет сохранить естественный контраст и тональный баланс исходного кадра.
                          """)


def show_settings_descriptions(event, frame):  # для нужного фрейма настроек или описания
    for page in [settings_frame, description_frame]:
        page.lower()
    if frame.name == 'settings_frame':
        settings_frame.lift()
    elif frame.name == 'description_frame':
        description_frame.lift()
