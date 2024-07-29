from pyray import *
loaded_fonts = {}

def get_font(font):
    if font in loaded_fonts:
        return loaded_fonts[font]
    else:
        loaded_font = load_font("assets/fonts/PixAntiqua.ttf")
        loaded_fonts['default'] = loaded_font
        return loaded_font
