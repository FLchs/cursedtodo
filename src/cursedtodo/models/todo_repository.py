from glob import glob
from os import path
import os
from uuid import uuid1

from ics import Calendar, Todo as IcsTodo
from cursedtodo.models.todo import Todo
from cursedtodo.utils.config import Config


class TodoRepository:
    @staticmethod
    def get_list(show_completed: bool = False, asc: bool = False) -> list[Todo]:
        # calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar/*")
        calendar_dir = path.expanduser(
            str(Config.get("MAIN", "calendars"))
        )
        ics_files = glob(path.join(calendar_dir, "*.ics"))

        events_todos = [
            Todo(
                event.uid,
                event.name or "",
                event.description or "",
                [getattr(x, "value", "") for x in event.extra if x.name == "CATEGORIES"]
                or [],
                path.basename(path.dirname(ics_file)),
                ics_file,
                event.priority or 0,
                event.completed.datetime if event.completed is not None else None,
                event.due.datetime if event.due is not None else None,
                event.location,
            )
            for ics_file in ics_files
            for event in Calendar(open(ics_file).read()).todos
            if event.completed is None or show_completed
        ]

        return sorted(events_todos, reverse=not asc)

    @staticmethod
    def get_lists_names() -> list[str]:
        calendar_dir = path.expanduser(
            str(Config.get("MAIN", "calendars"))
        ).strip("*")
        return [f.name for f in os.scandir(calendar_dir) if f.is_dir() and f.name != "*"]

    @staticmethod
    def save(todo: Todo) -> None:
        if todo.path is None:
            calendar = Calendar()
            todo_item = IcsTodo()
            calendar_dir = path.expanduser(
                str(Config.get("MAIN", "calendars")).strip("*/")
            )            
            new_dir = os.path.join(calendar_dir, todo.list)
            os.makedirs(new_dir, exist_ok=True)
            todo.path = os.path.join(new_dir, f"{uuid1()}.ics")
        else:
            with open(todo.path, "r") as f:
                calendar = Calendar(f.read())
            todo_item = calendar.todos.pop()
            if todo_item is None:
                raise Exception("Todo cannot be opened")

        todo._add_attributes(todo_item)
        calendar.todos.add(todo_item)
        with open(todo.path, "w") as f:
            f.writelines(calendar.serialize_iter())

    @staticmethod
    def delete(todo: Todo) -> None:
        if todo.path is None:
            raise Exception(f"Cannot delete {todo.summary} because path is null")
        os.remove(todo.path)
