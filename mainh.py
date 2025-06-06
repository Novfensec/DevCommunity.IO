"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
set DEBUG=1 && python main.py
"""

import importlib, os, registers

from kivy import Config

# Change the values of the application window size as you need.
Config.set("graphics", "height", "715")
Config.set("graphics", "width", "317")

# TODO: You may know an easier way to get the size of a computer display.
from PIL import ImageGrab
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

resolution = ImageGrab.grab().size

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width + 5

import webbrowser
from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSharedAxisTransition as SAT
from kivy.clock import Clock

Clock.max_iteration = 30


class UI(MDScreenManager):
    def __init__(self, *args, **kwargs):
        super(UI, self).__init__(*args, **kwargs)
        self.transition = SAT()


class DevCommunity(MDApp):
    DEBUG = True
    KV_DIRS = [os.path.join(os.getcwd(), "View")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Midnightblue"
        self.apply_styles("Light")

    def build_app(self) -> UI:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """

        import View.screens

        self.manager_screens = UI()
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

        return self.manager_screens

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        self.theme_cls.theme_style = style
        if style == "Light":
            Window.clearcolor = get_color_from_hex("#ffffff")
            style = "Dark"
        else:
            Window.clearcolor = get_color_from_hex("#000000")
            style = "Light"

    def referrer(self, destination: str = None) -> None:
        if self.manager_screens.current != destination:
            self.manager_screens.current = destination

    def web_open(self, url: str) -> None:
        webbrowser.open_new_tab(url)

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()


if __name__ == "__main__":
    DevCommunity().run()
