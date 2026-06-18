# СЛОВАРЬ СО СТРУКТУРОЙ МЕТАДОВ ОБРАБОТКИ
DICTIONARY_METHODS_CONFIG = {
    'Decoloration': {
        'frames': {
            'main_frame': 'decoloration_sub_frame',
        },
        'frames_settings': {
            'main_frame': {
                'sub_choosing_button': 'decoloration_sub_choosing_button',
                'sub_choosing_frame': 'decoloration_sub_choosing_frame',
                'sub_settings_button': 'decoloration_sub_settings_button',
                'sub_settings_frame': 'decoloration_sub_settings_frame', }},
        'frames_data': {
            'main_frame': {'choosing_frame_data': 'data',
                           'settings_frame_data': 'data'}, },
        'sub_methods': {
            'decoloration_standard': {
                'frames': {'main_frame': 'main_decoloration_standard_setting_frame',
                           'sub_frame': 'sub_decoloration_standard_setting_frame',
                           'main_settings_frame': 'decoloration_standard_setting_frame',
                           'main_settings_button_frame': {
                               'main_settings_button_frame': 'decoloration_standard_setting_button_frame'}},

            },
            'decoloration_weighted': {}
        }}, 'Color Mapping': {
        'color_mapping_two_colors': {

        }
    }}
# СЛОВАРЬ СО СПИСКАМИ СОЗДАНЫХ МЕТАДОВ
DICTIONARY_CREATED_METHODS_CONFIG = {
    'Decoloration': {},
    'Color Mapping': {}
}
# ТЕКУЩИЙ САБ МЕТОД
DICTIONARY_CURRENT_SUB_METHODS_CONFIG = {
    'Current': 'current',
    'Decoloration': 'current',
    'Color Mapping': 'current'
}

# ТЕКУЩИЙ МЕТОД
DICTIONARY_CURRENT_METHODS_CONFIG = {
    'Method': 'current'
}
