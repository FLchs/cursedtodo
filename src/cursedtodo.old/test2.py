from typing import TypeVar, Literal, Union

# Define a type variable for the object, which depends on the string.
T = TypeVar("T")

# Define the function that accepts a string and an argument depending on the string.
def process_command(command: Literal["int_command", "str_command"], arg: Union[int, str]) -> None:
    if command == "int_command":
        # Expect 'arg' to be an int for 'int_command'
        if not isinstance(arg, int):
            raise ValueError(f"Expected an int for command '{command}'")
        print(f"Processing integer command with value: {arg}")
    elif command == "str_command":
        # Expect 'arg' to be a string for 'str_command'
        if not isinstance(arg, str):
            raise ValueError(f"Expected a string for command '{command}'")
        print(f"Processing string command with value: {arg}")
    else:
        raise ValueError(f"Unknown command: {command}")

# Example usage
process_command("int_command", 42)      # Valid: Processes an int
process_command("str_command", "hello") # Valid: Processes a string

# Uncommenting this would raise a ValueError because the argument types don't match the command
process_command("int_command", "wrong_type")  # Invalid: Raises ValueError

