# CursedTodo

CursedTodo is a lightweight and straightforward todo manager for the terminal. Using `.ics` files for storage, it can be used with [vdirsync](http://vdirsyncer.pimutils.org) for CalDAV synchronization. Efforts are made to support most of [RFC-5545](https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/) and to be compatible with most other projects.

CursedTodo is developed in Python using the [Curses library](https://docs.python.org/3.13/library/curses.html) and has only [ics](https://github.com/ics-py/ics-py) as a dependency.

## Roadmap

- [x] Basic todo list (ordered by priority, show/hide completed)
- [ ] Todo creation, modification, and deletion
- [ ] Category filtering
- [ ] Subtasks and linked todos
- [ ] Search

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Alternatives

Projects with similar goals:

- [Todoman](https://github.com/pimutils/todoman) (CLI only)
- [Calcurse](https://calcurse.org/) (Calendar with simple todo list)
- [Calcure](https://github.com/anufrievroman/calcure) (Only imports todos)
