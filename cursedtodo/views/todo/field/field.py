from collections.abc import Callable


class Field:
    def __init__(self, name: str, id: int, validator: Callable[[int], int]):
        self.name = name
        self.id = id
        self.validator = validator

    def render(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def gather(self):
        raise NotImplementedError("Subclasses should implement this method.")
