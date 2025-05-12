from kivy.properties import StringProperty

from kivymd.uix.button import MDIconButton


class DevIcon(MDIconButton):

    def __init__(self, *args, **kwargs):
        super(DevIcon, self).__init__(*args, **kwargs)
