from dataclasses import dataclass
import os
import pathlib
import tomllib
from typing import Any, Optional

from cursedtodo.config.arguments import Arguments


@dataclass
class CalendarConfig:
    path: str
    color: Optional[str] = None
    default: Optional[bool] = None


@dataclass
class UIConfig:
    window_name: str
    show_footer_keybindings: bool
    select_first: bool
    rounded_borders: bool
    date_format: str


@dataclass
class _Config:
    calendars: dict[str, CalendarConfig]
    ui: UIConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "_Config":
        print("Parsing configuration file...")
        calendars = {
            name: CalendarConfig(**details)
            for name, details in data.get("Calendars", {}).items()
        }
        ui = UIConfig(**data.get("UI", {}))
        return cls(calendars=calendars, ui=ui)


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


Config = _init_config()
