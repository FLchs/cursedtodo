from dataclasses import dataclass
import os
import pathlib
import tomllib
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
    def from_dict(cls, data: dict[str, Any]) -> "_Config":
        print("Parsing configuration file...")
        calendars: list[Calendar] = [
            Calendar(i, **cal) for i, cal in enumerate(data.get("calendars", {}))
        ]
        ui = UIConfig(**data.get("ui", {}))
        columns: list[Columns] = [Columns(**col) for col in data.get("columns", {})]
        default_calendar = next(filter(lambda cal: cal.default, calendars))
        ui.default_calendar = (
            default_calendar.name if default_calendar is not None else None
        )
        # raise Exception(calendars, data)
        return cls(calendars=calendars, ui=ui, columns=columns)


def _init_config() -> _Config:
    """Load the configuration from a TOML file."""
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
        os.path.expanduser("~"), ".config"
    )
    config_file_path = Arguments.config or os.path.join(
        xdg_config_home, "cursedtodo/config.toml"
    )
    config_file = pathlib.Path(config_file_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with config_file.open("rb") as file:
        data = tomllib.load(file)

    return _Config.from_dict(data)
