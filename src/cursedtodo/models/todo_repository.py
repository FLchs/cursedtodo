from glob import glob
from os import path
import os
from uuid import uuid1

from ics import Calendar, Todo as IcsTodo
from cursedtodo.config import Config
from cursedtodo.models.todo import Todo


class TodoRepository:
    @staticmethod
    def get_list(show_completed: bool = False, asc: bool = False) -> list[Todo]:
        todos: list[Todo] = []
        for calendar in Config.calendars:
            calendar_dir = os.path.expanduser(calendar.path)
            ics_files = glob(path.join(calendar_dir, "*.ics"))

            events_todos = [
                Todo(
                    event.uid,
                    calendar,
                    event.name or "",
                    event.description or "",
                    [
                        cat.strip()
                        for x in event.extra
                        if x.name == "CATEGORIES"
                        for cat in getattr(x, "value", "").split(",")
                    ]
                    or [],
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

            todos.extend(sorted(events_todos, reverse=not asc))
        return todos

    @staticmethod
    def get_lists_names() -> list[str]:
        return [cal.name for cal in Config.calendars]

    @staticmethod
    def save(todo: Todo) -> None:
        if todo.path is None:
            calendar = Calendar()
            todo_item = IcsTodo()
            local_calendar_path = todo.calendar.path
            os.makedirs(local_calendar_path, exist_ok=True)
            todo.path = os.path.join(local_calendar_path, f"{uuid1()}.ics")
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
