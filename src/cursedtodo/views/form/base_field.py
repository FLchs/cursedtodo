
from abc import ABC, abstractmethod
from collections.abc import Callable
from curses import window
from datetime import datetime

class BaseField(ABC):
    def __init__(
        self,
        y: int,
        window: window,
        name: str,
        id: str,
        validator: Callable[[int | str], int | str],
        value: str | list[str] | int | datetime | None = None,
    ):
        # Positional attributes
        self.window = window
        self.y = y

        # Field identification
        self.name = name
        self.id = id

        # Field value and validation
        self.value = value
        self.validator = validator

    @abstractmethod
    def _validator(self, ch: int | str) -> int | str:
        """Validate input for the field."""
        pass

    @abstractmethod
    def render(self) -> None:
        """Render the field's label and input area."""
        pass

    @abstractmethod
    def focus(self) -> None:
        """Focus on the field to allow user input."""
        pass

