from dataclasses import dataclass


@dataclass
class Todo:
    summary: str
    list: str
    id: int
    priority: int
