# The screen's dictionary contains the objects of the models and controllers
# of the screens of the application.

from Model.home_screen import HomeScreenModel
from Controller.home_screen import HomeScreenController

screens = {
    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },
}
