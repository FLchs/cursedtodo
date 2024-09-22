from abc import ABC, abstractmethod
from curses import window
from typing import Any


class Controller(ABC):
    def __init__(self, router: Any) -> None:
        self.window: window = router.window
        self.router = router

    @abstractmethod
    def handle_key(self, key: int) -> bool: ...
