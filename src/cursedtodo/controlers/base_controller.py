
from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from curses import window

if TYPE_CHECKING:
    from cursedtodo.utils.router import Router


class Controller(ABC):
    def __init__(self, router: Router) -> None:
        self.window: window = router.window
        self.router = router

    @abstractmethod
    def handle_key(self, key: int) -> bool: ...
