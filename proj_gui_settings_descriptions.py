from tkinter import *
from tkinter import scrolledtext
from proj_methodsfunc import get_method_name
from proj_custommethods import *

current_sub_method = None






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

    global settings_frame, settings_canvas
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


created_methods = {}


#устройство кастомизации: название, индекс, саб мктод, настройки
#когда создаём фрейм с выбором флажков проходимся по списку и создаём флажки
#когда создаём новый метод, добавляем новый флажок и создаём новый метод с именем сабметод+индекстег
#когда вызываем метод передаём в функцию наш обект


decoloration_standard_0 = create_custom_method('Standard', 0, 'decoloration_standard',
                                               [None, None])
decoloration_weighted_0 = create_custom_method('Weighted', 0, 'decoloration_weighted',
                                               [0.299, 0.587, 0.114])

color_mapping_standard_0 = create_custom_method('Two colors', 0, 'color_mapping_standard',
                                                [(132, 71, 21),(59, 20, 6), 150])

base_decoloration = {'decoloration_standard':{0:decoloration_standard_0},'decoloration_weighted':{0:decoloration_weighted_0}}
base_color_mapping = {'color_mapping_standard':{0:color_mapping_standard_0}}

# method_name rb_key
def create_settings(event, combo, frame):  # когда жмякаем на кобобокс создаётся нкжное окно с флажками
    global created_methods
    current_method = get_method_name(event, combo)
    if current_method == "Decoloration":
        if hasattr(frame, 'decoloration_sub_frame'):
            frame.current_sub_method = frame.decoloration_current_sub_method.get()
            get_current_sub_method(current_method, frame)
        else:
            frame.decoloration_current_sub_method = StringVar(value='decoloration_standard')
            decoloration_sub_frame = Frame(frame, bg="black")
            decoloration_sub_frame.grid(row=0, column=0, sticky="nsew")

            decoloration_sub_choosing_button = Button(decoloration_sub_frame,
                                                      textvariable=frame.decoloration_current_sub_method)
            decoloration_sub_choosing_button.grid(row=0, column=0, sticky="nsew")

            decoloration_sub_choosing_frame = Frame(decoloration_sub_frame, bg="black")
            decoloration_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
            decoloration_sub_choosing_frame.grid_rowconfigure(0, weight=1)
            decoloration_sub_choosing_frame.grid_columnconfigure(0, weight=1)
            decoloration_sub_settings_button = Button(decoloration_sub_frame)

            decoloration_sub_settings_button.grid(row=2, column=0, sticky="nsew")

            decoloration_sub_settings_frame = Frame(decoloration_sub_frame, bg="red", height=1000)

            decoloration_sub_settings_frame.grid(row=3, column=0, sticky="nsew")
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

            for i in range(3):
                decoloration_sub_frame.grid_rowconfigure(i, weight=1)
            decoloration_sub_frame.grid_columnconfigure(0, weight=1)

            frame.decoloration_sub_frame = decoloration_sub_frame
            frame.current_sub_method = 'decoloration_standard'
            created_methods.update({'Decoloration': frame.decoloration_sub_frame})
            decoloration_sub_methods = {'Standard': 'decoloration_standard', 'Weighted': 'decoloration_weighted',
                                        'Custom': 'decoloration_custom'}

            index = 0
            for sub_method in decoloration_sub_methods:
                current = Radiobutton(
                    decoloration_sub_choosing_frame,
                    text=sub_method,
                    variable=frame.decoloration_current_sub_method,
                    value=decoloration_sub_methods[sub_method],
                    bg="black",
                    fg="white",
                    selectcolor="gray",
                    activebackground="black",
                    anchor='w',  # слева
                    command=lambda current_method=current_method, frm=frame: get_current_sub_method(current_method, frm)
                )
                current.grid(row=index, column=0, sticky="ew")
                index += 1

            get_current_sub_method(current_method, frame)
    elif current_method == "Color Mapping":  # color_mapping
        if hasattr(frame, 'color_mapping_sub_frame'):
            frame.current_sub_method = frame.color_mapping_current_sub_method.get()
            get_current_sub_method(current_method, frame)
        else:
            frame.color_mapping_current_sub_method = StringVar(value='color_mapping_standard_0')  # флажок
            color_mapping_sub_frame = Frame(frame, bg="black")
            color_mapping_sub_frame.grid(row=0, column=0, sticky="nsew")

            color_mapping_sub_choosing_button = Button(color_mapping_sub_frame,
                                                       textvariable=frame.color_mapping_current_sub_method)
            color_mapping_sub_choosing_button.grid(row=0, column=0, sticky="nsew")

            color_mapping_sub_choosing_frame = Frame(color_mapping_sub_frame, bg="black")
            color_mapping_sub_choosing_frame.grid(row=1, column=0, sticky="nsew")
            color_mapping_sub_choosing_frame.grid_rowconfigure(0, weight=1)
            color_mapping_sub_choosing_frame.grid_columnconfigure(0, weight=1)
            color_mapping_sub_settings_button = Button(color_mapping_sub_frame)

            color_mapping_sub_settings_button.grid(row=2, column=0, sticky="nsew")

            color_mapping_sub_settings_frame = Frame(color_mapping_sub_frame, bg="red", height=1000)

            color_mapping_sub_settings_frame.grid(row=3, column=0, sticky="nsew")
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
            for i in range(3):
                color_mapping_sub_frame.grid_rowconfigure(i, weight=1)
            color_mapping_sub_frame.grid_columnconfigure(0, weight=1)

            frame.color_mapping_sub_frame = color_mapping_sub_frame
            created_methods.update({'Color Mapping': frame.color_mapping_sub_frame})
            color_mapping_sub_methods = {'Two colors': 'color_mapping_standard_0',
                                         'Weiwqeghted': 'color_mapping_weighted', 'Custom': 'color_mapping_custom'}
            color_mapping_sub_methods_settings = {'Two colors': 'color_mapping_standard',
                                                  'Weiwqeghted': 'color_mapping_weighted',
                                                  'Custom': 'color_mapping_custom'}
            index = 0
            for sub_method in color_mapping_sub_methods:
                current = Radiobutton(
                    color_mapping_sub_choosing_frame,
                    text=sub_method,
                    variable=frame.color_mapping_current_sub_method,
                    value=color_mapping_sub_methods[sub_method],
                    bg="black",
                    fg="white",
                    selectcolor="gray",
                    activebackground="black",
                    anchor='w',  # слева
                    command=lambda current_method=current_method, frm=frame: get_current_sub_method(current_method, frm)
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
        current_sub_method = frame.decoloration_current_sub_method.get()
    elif current_method == "Color Mapping":
        current_sub_method = frame.color_mapping_current_sub_method.get()


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
