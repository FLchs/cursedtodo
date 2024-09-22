from typing import Literal, Optional, overload, reveal_type


class Todo:
    name: str
    priority: int


@overload
def route(name: Literal["main"]): ...


@overload
def route(name: Literal["edit"], arg: Todo): ...


def route(name: Literal["main"] | Literal["edit"], arg: Optional[Todo] = None) -> None:
    if name == "main":
        print("main")
        reveal_type(arg)
    if name == "edit":
        print(arg)
        reveal_type(arg)
    else:
        raise TypeError("Malformed route")


route("main", Todo())

route("edit", Todo())

#
# type RouteName = Literal["main", "edit", "create"]
#
#
# class Todo:
#     name: str
#     priority: int
#
#
# type MainRoute = tuple[Literal["main"], None]
# type EditRoute = tuple[Literal["edit"], Todo]
#
#
# type Param = Union[MainRoute, EditRoute]
#
#
# def route(param: Param):
#     name, args = param
#     if name == "main":
#         print("main")
#         reveal_type(param)
#     if name == "edit":
#         print(args)
#         reveal_type(param)
#     else:
#         raise TypeError("Malformed route")
#
#
# route(("edit", Todo()))
#
# # route("edit", Todo())
