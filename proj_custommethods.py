class CustomMethod:
    pass


def create_custom_method(name, index_tag, sub_method_tag, settings):
    custom_method = CustomMethod()
    custom_method.name = name
    custom_method.index_tag = index_tag
    custom_method.sub_method_tag = sub_method_tag
    custom_method.settings = settings
    return custom_method



