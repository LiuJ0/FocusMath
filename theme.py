import configparser
import os

def hex_to_rgba_01(value):
    value = value.lstrip('#')
    lv = len(value)
    r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r /= 255
    g /= 255
    b /= 255
    a = 1
    return [r, g, b, a]


class themeConfig:
    def __init__(self):
        settings = configparser.ConfigParser()
        settings.read("settings.ini")
        self.theme_folder = settings["THEME"]["theme"]
        self.theme = configparser.ConfigParser()


    def read_theme(self):
        theme_file = os.path.join("themes", self.theme_folder, "theme.ini")
        self.theme.read(theme_file)
        #colors
        self.color_wrong = hex_to_rgba_01(self.theme["COLORS"]["wrong"])
        self.color_right = hex_to_rgba_01(self.theme["COLORS"]["right"])
        self.color_neutral = hex_to_rgba_01(self.theme["COLORS"]["neutral"])
        self.color_neutral_muted = hex_to_rgba_01(self.theme["COLORS"]["neutral_muted"])
        self.color_background = hex_to_rgba_01(self.theme["COLORS"]["background"])

        #fonts
        self.font_info = os.path.join("themes", self.theme_folder, "fonts", self.theme["FONTS"]["info"])
        self.font_math = os.path.join("themes", self.theme_folder, "fonts", self.theme["FONTS"]["math"])
        self.font_math_italic = os.path.join("themes", self.theme_folder, "fonts", self.theme["FONTS"]["math_italic"])
