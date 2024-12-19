from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from ics import Todo as IcsTodo
from ics.parsers.parser import ContentLine

from cursedtodo.models.calendar import Calendar
from cursedtodo.utils.time import get_locale_tz


@dataclass
class Todo:
    id: int | str
    calendar: Calendar
    summary: str
    description: str
    categories: list[str] | None
    path: str | None
    priority: int
    completed: datetime | None
    due: datetime | None
    location: str | None

    def __lt__(self, other: Todo) -> bool:
        return self.priority < other.priority

    def _add_categories(self, todo_item: IcsTodo) -> None:
        for item in todo_item.extra:
            if isinstance(item, ContentLine) and item.name == "CATEGORIES":
                item.value = ",".join(self.categories or "")
                return
        todo_item.extra.append(
            ContentLine(name="CATEGORIES", value=",".join(self.categories or ""))
        )

    def _add_attributes(self, todo_item: IcsTodo) -> None:
        todo_item.name = self.summary
        todo_item.description = self.description
        todo_item.location = self.location or ""
        todo_item.priority = self.priority
        todo_item.due = self.due
        # TODO: find a way to fix types...
        # either by using "arrow", updating ics or writing our own lib
        todo_item.completed = self.completed  # type: ignore
        self._add_categories(todo_item)

    def mark_as_done(self) -> None:
        tz = get_locale_tz()
        self.completed = datetime.now(tz) if self.completed is None else None
