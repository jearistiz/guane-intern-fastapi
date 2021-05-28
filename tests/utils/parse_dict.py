from typing import Any, Callable


def update_dict_fmt_item(obj: dict, key: Any, format: Callable):
    obj.update({key: format(obj[key])})
