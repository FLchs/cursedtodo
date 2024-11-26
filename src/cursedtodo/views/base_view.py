from abc import ABC, abstractmethod
from curses import window
from typing import Any



class BaseView(ABC):
    def __init__(self, controler: Any) -> None:
        self.window: window = controler.window
        self.controller = controler

    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def main_loop(self) -> None: ...

