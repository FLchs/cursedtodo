import json
from subprocess import PIPE, Popen
from types import SimpleNamespace

from cursedtodo.todo import Todo


class Data:

    @staticmethod
    def loadTodos() -> list[Todo]:
        cmd = Popen("todo --porcelain list", shell=True, stdout=PIPE, stderr=PIPE)
        result, _err = cmd.communicate()
        parsed = json.loads(result.decode(), object_hook=lambda d: SimpleNamespace(**d))
        parsed.sort(key=lambda x: x.priority, reverse=False)
        return parsed
