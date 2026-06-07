class CustomMethod:
    pass


class CurrentSubMethod:
    pass


def create_current_sub_method(tag, object):
    current_sub_method = CurrentSubMethod()
    current_sub_method.tag = tag
    current_sub_method.object = object
    return current_sub_method


def create_custom_method(name, index, tag, settings):
    custom_method = CustomMethod()
    custom_method.name = name
    custom_method.index = index
    custom_method.tag = tag
    custom_method.settings = settings
    return custom_method


def get_quantity_sub_methods(dictionary):
    quantity = 0
    for item in dictionary:
        quantity += len(item)
    return quantity


def get_split_sub_method_name(text):
    parts = text.rsplit("_", 1)  # разделить по _ максимум 1 раз начиная справа
    return parts[0], parts[1]


def get_united_sub_method_name(index, tag):
    return f"{tag}_{index}"


def find_current_sub_method(dictionary, text):
    sub_methods, index = get_split_sub_method_name(text)
    for values in dictionary.items():
        if values[0] == sub_methods:
            for sub_values in values[1].items():
                if str(sub_values[0]) == index:
                    return sub_values[1]

def create_and_store_methods(base_dict, name, index, tag, settings):
    obj = create_custom_method(name, index, tag, settings)
    if tag not in base_dict:
        base_dict[tag] = {}
    base_dict[tag][index] = obj