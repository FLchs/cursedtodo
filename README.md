# CursedTodo

CursedTodo is a lightweight and straightforward todo manager for the terminal. Using `.ics` files for storage, it can be used with [vdirsync](http://vdirsyncer.pimutils.org) for CalDAV synchronization. Efforts are made to support most of [RFC-5545](https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/) and to be compatible with most other projects.

CursedTodo is developed in Python using the [Curses library](https://docs.python.org/3.13/library/curses.html) and has only [ics](https://github.com/ics-py/ics-py) as a dependency.

## Roadmap

- [x] Basic todo list (ordered by priority, show/hide completed)
- [x] Todo creation, modification, and deletion
- [ ] Keymaps customization
- [ ] Category filtering
- [ ] Subtasks and linked todos
- [ ] Search
- [ ] Basic CLI for adding todos

## Will not be implemented
- Mouse support

## Usage
Cursedtodo need a config.toml files in `$XDG_CONFIG_HOME/cursedtodo/`
Keybinds are based on Vim hjkl for movement.

Here is an example [config.toml](config.toml):
```
# Calendars configuration
[[calendars]]
name = "Personal"
path = "~/.local/share/vdirsyncer/calendar/personal"
# available colors : black, red, green, yellow, blue, magenta, cyan, white
color = "blue"
default = true

[[calendars]]
name= "Work"
path = "~/.local/share/vdirsyncer/calendar/work"
color = "green"
default = false

# UI configuration
[ui]
window_name = "Todos"
show_footer_keybindings = true
select_first = true
rounded_borders = true
date_format = "%m/%d/%y %H:%M:%S"

```

> [!IMPORTANT]  
> Cursedtodo is still in early development, expect some bugs and possibly breaking changes to the
> config file. Please backup your data regularly.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Alternatives

Projects with similar goals:

- [Todoman](https://github.com/pimutils/todoman) (CLI only)
- [Calcurse](https://calcurse.org/) (Calendar with simple todo list)
- [Calcure](https://github.com/anufrievroman/calcure) (Only imports todos)
