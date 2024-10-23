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

    def mark_as_done(self) -> None:
        if self.path is None:
            raise Exception("Todo path is none")
        calendar = Calendar(open(self.path).read())
        todo_item = next(
            (todo for todo in calendar.todos if todo.uid == self.id),
            None,
        )
        if todo_item is None:
            raise Exception("Cannot find todo")

        self.completed = Arrow.now() if self.completed is None else None
        # TODO: check ics new version
        # There is a type issue with ics, will be resolved in next version.
        todo_item.completed = self.completed  # type: ignore
        calendar.todos.add(todo_item)

        with open(self.path, "w") as f:
            f.writelines(calendar.serialize_iter())

    def save(self) -> None:
        calendar = Calendar()
        todo_item = IcsTodo()

        calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
        new_dir = os.path.join(calendar_dir, self.list)
        os.makedirs(new_dir, exist_ok=True)

        new_path = os.path.join(new_dir, f"{uuid1()}.ics")

        todo_item.name = self.summary
        todo_item.description = self.description
        todo_item.location = self.location or ""
        todo_item.priority = self.priority
        todo_item.extra.append(
            ContentLine(name="CATEGORIES", value=",".join(self.categories or ""))
        )
        calendar.todos.add(todo_item)

        self.path = new_path

        with open(self.path, "w") as f:
            f.writelines(calendar.serialize_iter())

    def delete(self) -> None:
        if self.path is None:
            raise Exception(f"Cannot delete {self.summary} because paht is null")
        os.remove(self.path)
