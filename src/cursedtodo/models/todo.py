from __future__ import annotations
from dataclasses import dataclass
import os
from uuid import uuid1

from arrow import Arrow
from ics import Calendar, Todo as IcsTodo
from ics.parsers.parser import ContentLine


@dataclass
class Todo:
    id: int | str
    summary: str
    description: str
    categories: list[str] | None
    list: str
    path: str | None
    priority: int
    completed: Arrow | None
    due: Arrow | None
    location: str | None

    def __lt__(self, other: Todo) -> bool:
        return self.priority < other.priority

    def save(self) -> None:
        # Initialize new calendar and todo item
        calendar = Calendar()
        todo_item = IcsTodo()
        # categories = categories_str.split(",")

        # Determine the new path
        calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
        new_dir = os.path.join(calendar_dir, self.list)
        os.makedirs(new_dir, exist_ok=True)

        new_path = os.path.join(new_dir, f"{uuid1()}.ics")

        # Set the todo fields
        todo_item.name = self.summary
        todo_item.description = self.description
        todo_item.location = self.location or ""
        todo_item.priority = self.priority
        todo_item.extra.append(
            ContentLine(name="CATEGORIES", value=",".join(self.categories or ""))
        )
        calendar.todos.add(todo_item)

        # Update the path in the object
        self.path = new_path


        # Write the calendar to the file
        with open(self.path, "w") as f:
            f.writelines(calendar.serialize_iter())
