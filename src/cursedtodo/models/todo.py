from __future__ import annotations
from dataclasses import dataclass

from arrow import Arrow



@dataclass
class Todo:
    id: int | str
    summary: str
    description: str
    categories: list[str] | None
    list: str
    path: str | None
    priority: int
    completed: Arrow
    due: Arrow | None


    def __lt__(self, other: Todo) -> bool:
        return self.priority < other.priority

