from curses import window

from cursedtodo.controlers.main_controller import MainController




class Router:
    def __init__(self, window: window) -> None:
        self.window = window

    def route_main(self) -> None:
        acontroller = MainController(self)
        acontroller.run()

    # def gotoB(self, data: str):
    #     bcontroller = BController(self.window, self, data = "nigga")
    #     bcontroller.run()
