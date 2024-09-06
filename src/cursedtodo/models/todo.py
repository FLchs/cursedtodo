import os
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid1

from ics import Calendar, Event
from ics import Todo as IcsTodo


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

    def get_fields(self):
        return ["summary", "priority"]

    def __lt__(self, other):
        return self.priority < other.priority

    def save(self):
        try:
            if self.path and os.path.exists(self.path):
                self.edit_existing_todo()
            else:
                self.create_new_todo()
        except Exception as ex:
            error_message = f"An error occurred while saving the Todo: {ex}"
            print(error_message)
            raise RuntimeError(error_message) from ex

    def create_new_todo(self):
        # Initialize new calendar and todo item
        calendar = Calendar()
        todo_item = IcsTodo()

        # Determine the new path
        calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
        new_dir = os.path.join(calendar_dir, self.list)
        os.makedirs(new_dir, exist_ok=True)

        new_path = os.path.join(new_dir, f"{uuid1()}.ics")

        # Set the todo fields
        todo_item.name = self.summary
        todo_item.priority = self.priority
        calendar.todos.add(todo_item)

        # Update the path in the object
        self.path = new_path

        # Write the calendar to the file
        with open(self.path, "w") as f:
            f.writelines(calendar.serialize_iter())

    def edit_existing_todo(self):
        if self.path is None:
            raise Exception("Path is None")
        # Open existing calendar and retrieve the todo item
        with open(self.path, "r") as f:
            calendar = Calendar(f.read())

        todo_item = calendar.todos.pop() if calendar.todos else IcsTodo()

        # Update the todo fields
        todo_item.name = self.summary
        todo_item.priority = self.priority
        calendar.todos.add(todo_item)

        # Check if the directory needs to be changed
        pp = Path(self.path)
        if pp.parent.name != self.list:
            calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
            new_path = os.path.join(calendar_dir, self.list, pp.name)
            os.remove(self.path)
            self.path = new_path

        # Write the updated calendar back to the file
        with open(self.path, "w") as f:
            f.writelines(calendar.serialize_iter())

    def delete(self):
        if self.path is None:
            raise Exception("Path is None")
        os.remove(self.path)

    # def save(self):
    #     try:
    #         path = ""
    #         # Initialize the calendar and todo item
    #         if self.path is not None and os.path.exists(self.path):
    #             pp = Path(self.path)
    #             with open(self.path, "r") as f:
    #                 c = Calendar(f.read())
    #             e = c.todos.pop() if c.todos else IcsTodo()
    #             if pp.parent.name is not self.list:
    #                 calendar_dir = os.path.expanduser(
    #                     "~/.local/share/vdirsyncer/calendar"
    #                 )
    #                 path = os.path.join(calendar_dir, self.list, pp.name)
    #                 os.remove(self.path)
    #         else:
    #             c = Calendar()
    #             e = IcsTodo()
    #             calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar")
    #             path = os.path.join(calendar_dir, self.list)
    #
    #             # Ensure directory exists
    #             os.makedirs(path, exist_ok=True)
    #
    #             path = os.path.join(path, f"{uuid1()}.ics")
    #
    #         # Update todo item fields
    #         e.name = self.summary
    #         e.priority = self.priority
    #         c.todos.add(e)
    #
    #         # Update the path in case it was None
    #         self.path = path
    #         # Write back to file
    #         with open(self.path or path, "w") as f:
    #             f.writelines(c.serialize_iter())
    #
    #     except Exception as ex:
    #         print(f"An error occurred while saving the Todo: {ex}")
    #         raise

    # def save(self):
    #     c: Calendar
    #     e: IcsTodo
    #     path: str
    #
    #     if self.path is not None:
    #         c = Calendar(open(self.path).read())
    #         e = c.todos.pop()
    #         path = self.path
    #     else:
    #         c = Calendar()
    #         e = IcsTodo()
    #         calendar_dir = os.path.expanduser("~/.local/share/vdirsyncer/calendar/*")
    #         path = os.path.join(calendar_dir, self.list, str(uuid1()) + ".ics")
    #     e.name = self.summary
    #     e.priority = self.priority
    #     c.todos.add(e)
