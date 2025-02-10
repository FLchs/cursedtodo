from dataclasses import dataclass
import os
import pathlib
import tomllib
import shutil
from typing import Any, Optional

from cursedtodo.config.arguments import Arguments
from cursedtodo.models.calendar import Calendar


@dataclass
class UIConfig:
    window_name: str
    show_footer_keybindings: bool
    select_first: bool
    rounded_borders: bool
    date_format: str
    default_calendar: Optional[str] = None
    category_colors: bool = False
    confirm_mark_as_done: bool = False


@dataclass
class Columns:
    property: str
    width: int


@dataclass
class _Config:
    calendars: list[Calendar]
    ui: UIConfig
    columns: list[Columns]

    @classmethod
    def from_dict(cls, data: dict[str, Any], default_data: dict[str, Any]) -> "_Config":
        ui_data = dict()
        ui_data.update(default_data.get("ui", {}))
        ui_data.update(data.get("ui", {}))
        ui = UIConfig(**ui_data)

        columns_data = dict()
        columns_data.update(default_data.get("columns", {}))
        columns_data.update(data.get("columns", {}))
        columns: list[Columns] = [Columns(**col) for col in columns_data]

        calendars: list[Calendar] = [
            Calendar(i, **cal) for i, cal in enumerate(data.get("calendars", {}))
        ]

        default_calendar = next(filter(lambda cal: cal.default, calendars))
        ui.default_calendar = (
            default_calendar.name if default_calendar is not None else None
        )

        return cls(calendars=calendars, ui=ui, columns=columns)


def _init_config() -> _Config:
    print("Parsing configuration file...")
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    config_file_path = Arguments.config or os.path.join(
        xdg_config_home, "cursedtodo/config.toml"
    )
    config_file = pathlib.Path(config_file_path)
    default_config_file = pathlib.Path(
        os.path.join(pathlib.Path(__file__).parent.resolve(), "default_config.toml")
    )

    if not config_file.exists():
        if Arguments.config is None:
            print(
                "Configuration file not found, creating default configuration file..."
            )
            shutil.copy(default_config_file, config_file)
        else:
            raise Exception(f"Configuration file not found: {config_file}")

    with config_file.open("rb") as file:
        data = tomllib.load(file)

    with default_config_file.open("rb") as file:
        default_data = tomllib.load(file)

    return _Config.from_dict(data, default_data)
