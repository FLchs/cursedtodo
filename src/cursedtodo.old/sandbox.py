import os

from ics import Calendar



def main():
    calendar_file = os.path.expanduser(
        "~/.local/share/vdirsyncer/calendar/personal/565515484531002000.ics"
    )
    aa = "hello"
    print(aa)
    with open(calendar_file, encoding="utf8") as file:
        cal = Calendar(file.read()).todos
        print(cal.pop().extra)

main()
