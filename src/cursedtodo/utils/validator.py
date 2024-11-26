from typing import Any, List, TypeVar

T = TypeVar("T")


class Validator:
    @staticmethod
    def validate(value: Any, T: type[T]) -> T:
        if isinstance(value, T):
            return value
        else:
            raise Exception(f"{type(value).__name__} received, expected: {T.__name__}")

    @staticmethod
    def validate_optional(value: Any, T: type[T]) -> T | None:
        if value is None:
            return None
        if isinstance(value, T):
            return value
        else:
            raise Exception(f"{type(value).__name__} received, expected: {T.__name__}")

    @staticmethod
    def validate_list(value: Any, T: type[T]) -> List[T]:
        if not isinstance(value, list):
            raise TypeError(f"Expected a list, but got {type(value).__name__}.")

        if all(isinstance(item, T) for item in value):
            return value  

        raise ValueError(f"All items in the list must be of type {T.__name__}.")
