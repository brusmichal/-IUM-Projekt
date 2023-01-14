from typing import TypeVar

T = TypeVar("T")


class UnwrapExeption(Exception):
    pass


def unwrap(x: T | None) -> T:
    if x is None:
        raise UnwrapExeption()
    else:
        return x
