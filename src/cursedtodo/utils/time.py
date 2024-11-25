from datetime import datetime
import os
from zoneinfo import ZoneInfo

from cursedtodo.utils.config import Config

format =  str(Config.get("UI", "date_format"))

# TODO: make it a class and maybe use dateutil for more robust parsing

def get_locale_tz() -> ZoneInfo:
    local_tz_path = os.readlink('/etc/localtime')
    local_tz_name = local_tz_path.split('/usr/share/zoneinfo/')[-1]
    return ZoneInfo(local_tz_name)

def datetime_format(datetime: datetime) -> str:
    local_tz = get_locale_tz()
    return datetime.astimezone(local_tz).strftime(format)

def parse_to_datetime(string: str) -> datetime:
    return datetime.strptime(string, format)
