# CursedTodo

![GitHub Release](https://img.shields.io/github/v/release/flchs/cursedtodo?include_prereleases)
![GitHub License](https://img.shields.io/github/license/flchs/cursedtodo)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/flchs/cursedtodo/release.yml)

CursedTodo is a minimalist, terminal base todo manager storing tasks as `.ics` files for storage.
It can be used with [vdirsyncer](http://vdirsyncer.pimutils.org) for CalDAV synchronization. Efforts are made to support most of [RFC-5545](https://icalendar.org/RFC-Specifications/iCalendar-RFC-5545/) and to be compatible with most other projects.
It has been tested with [vdirsyncer](http://vdirsyncer.pimutils.org), [Nextcloud Tasks](https://apps.nextcloud.com/apps/tasks) and [Tasks.org](https://tasks.org/).

Built in Python using the [Curses library](https://docs.python.org/3.13/library/curses.html) Cursedtodo has only one direct dependency: [ics](https://github.com/ics-py/ics-py).

## Demo

![demo of cursedtodo](demo.gif "Demo")
> Quick look at Cursedtodo in action.

## Roadmap

### Short term

- [x] Basic todo list (ordered by priority, show/hide completed)
- [x] Todo creation, modification, and deletion
- [ ] Arch aur package
- [ ] Other distributions packages
- [ ] Keymaps customization
- [ ] Category filtering
- [ ] Basic CLI for adding todos

### Long term

- [ ] Subtasks and linked todos
- [ ] Search

## Will not be implemented

- Mouse support
- Windows support (PR accepted)

## Usage

```
pip install cursedtodo
```

Cursedtodo will generate a config.toml files in `$XDG_CONFIG_HOME/cursedtodo/` at first start.
Keybinds are based on Vim hjkl for movement.

Here is an example [config.toml](config.toml):

``` toml
# Calendars configuration
[[calendars]]
name = "Personal"
path = "~/.local/share/cursedtodos/calendar/personal" # should be something like ~/.local/share/vdirsyncer/calendar/personal if you are using vdirsyncer
# available colors : black, red, green, yellow, blue, magenta, cyan, white
color = "blue"
default = true

[[calendars]]
name= "Work"
path = "~/.local/share/cursedtodos/calendar/work" # should be something like ~/.local/share/vdirsyncer/calendar/work if you are using vdirsyncer
color = "green"
default = false

# UI configuration
[ui]
window_name = "Todos"
show_footer_keybindings = true
select_first = true
rounded_borders = true
date_format = "%m/%d/%y %H:%M:%S"
category_colors = true
confirm_mark_as_done = true

# Columns configuration
[[columns]]
property = "calendar.name"
width = 10

[[columns]]
property = "summary"
width = 30

[[columns]]
property = "priority"
width = 15

[[columns]]
property = "due"
width = 25

[[columns]]
property = "categories"
width = 30
```

> [!IMPORTANT]  
> Cursedtodo is still in early development, expect some bugs and possibly breaking changes to the
> config file. Please backup your data regularly.

## Contributing

We welcome contributions! If you find a bug, have a feature request, or want to improve the project, feel free to open an issue or submit a pull request.

For discussions and suggestions, check out the [issues][https://github.com/FLchs/cursedtodo/issues] page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Alternatives

Projects with similar goals:

- [Todoman](https://github.com/pimutils/todoman) - CLI-based todo manager using .ics
- [Calcurse](https://calcurse.org/) Terminal-based calendar with a simple built-in todo list
- [Calcure](https://github.com/anufrievroman/calcure) A personal calendar and task manager that supports .ics imports (but not currently support write or export)
