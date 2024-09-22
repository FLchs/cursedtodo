from __future__ import annotations
from dataclasses import dataclass



@dataclass
class Todo:
    id: int | str
    summary: str
    description: str
    categories: list[str] | None
    list: str
    path: str | None
    priority: int
    completed: bool


    def __lt__(self, other: Todo) -> bool:
        return self.priority < other.priority

