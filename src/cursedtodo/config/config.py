from dataclasses import dataclass
import os
import pathlib
import tomllib
from typing import Any, Optional

from cursedtodo.config.arguments import Arguments


@dataclass
class CalendarConfig:
    name: str
    path: str
    color: Optional[str] = None
    default: Optional[bool] = None

    def __post_init__(self) -> None:
        self.path = os.path.expanduser(self.path)


@dataclass
class UIConfig:
    window_name: str
    show_footer_keybindings: bool
    select_first: bool
    rounded_borders: bool
    date_format: str
    default_calendar: Optional[str] = None


@dataclass
class _Config:
    calendars: list[CalendarConfig]
    ui: UIConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "_Config":
        print("Parsing configuration file...")
        calendars: list[CalendarConfig] = [
            CalendarConfig(**cal) for cal in data.get("calendars", {})
        ]
        ui = UIConfig(**data.get("ui", {}))
        default_calendar = next(filter(lambda cal: cal.default, calendars))
        ui.default_calendar = (
            default_calendar.name if default_calendar is not None else None
        )
        # raise Exception(calendars, data)
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
