from glob import glob
from os import path

from ics import Calendar
from cursedtodo.models.todo import Todo
from cursedtodo.utils.config import Config


class TodoRepository:
    @staticmethod
    def get_list(show_completed: bool = False, asc: bool = False) -> list[Todo]:
        # calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar/*")
        calendar_dir = path.expanduser(
            # str(config.config.getstr("", "MAIN", "calendars") or "").strip()
            str(Config.get("MAIN", "calendars"))
        )
        ics_files = glob(path.join(calendar_dir, "*.ics"))

        events_todos = [
            Todo(
                event.uid,
                event.name or "",
                event.description or "",
                [getattr(x, 'value', '') for x in event.extra if x.name == "CATEGORIES"] or [],
                path.basename(path.dirname(ics_file)),
                ics_file,
                event.priority or 0,
                event.completed,
                event.due,
                event.location,
            )
            for ics_file in ics_files
            for event in Calendar(open(ics_file).read()).todos
            if event.completed is None or show_completed
        ]

        return sorted(events_todos, reverse=not asc)
