from cursedtodo.config import Config


class Help:
    @staticmethod
    def get_keybindings() -> list[str | tuple[str, int]]:
        return [
            f"Up: {chr(Config.keybindings.up)}",
            f"Down: {chr(Config.keybindings.down)}",
            f"New: {chr(Config.keybindings.new)}",
            f"Edit: {chr(Config.keybindings.edit)}",
            f"Show completed: {chr(Config.keybindings.show_completed)}",
            f"Change order: {chr(Config.keybindings.change_order)}",
            f"Mark as done: {'space' if Config.keybindings.mark_as_done == 32 else chr(Config.keybindings.mark_as_done)}",
            f"Delete: {chr(Config.keybindings.delete)}",
            "Help: ?",
            "Quit: q",
        ]
