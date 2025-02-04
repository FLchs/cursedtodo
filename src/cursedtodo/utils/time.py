from datetime import datetime
import os
from zoneinfo import ZoneInfo

from cursedtodo.config import Config


class TimeUtil:
    @staticmethod
    def get_locale_tz() -> ZoneInfo:
        local_tz_path = os.readlink("/etc/localtime")
        local_tz_name = local_tz_path.split("/usr/share/zoneinfo/")[-1]
        return ZoneInfo(local_tz_name)

    @staticmethod
    def datetime_format(datetime: datetime) -> str:
        return datetime.strftime(Config.ui.date_format)

    @staticmethod
    def parse_to_datetime(string: str) -> datetime:
        format = Config.ui.date_format
        while len(format) > 1:
            try:
                return datetime.strptime(string, format)
            except ValueError:
                pass
            format = format[: len(format) - 1]
        raise Exception("Date error")
