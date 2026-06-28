from dataclasses import dataclass
from typing import Generic, TypeVar, Union

L = TypeVar("L")
R = TypeVar("R")


@dataclass(frozen=True, slots=True)
class Left(Generic[L]):
    value: L

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class Right(Generic[R]):
    value: R

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True


Either = Union[Left[L], Right[R]]
