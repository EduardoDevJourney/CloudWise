from typing import Generic, TypeVar

T = TypeVar("T")


class WatchedList(Generic[T]):
    def __init__(self, initial_items: list[T] | None = None) -> None:
        self._current_items = list(initial_items or [])
        self._new_items: list[T] = []
        self._removed_items: list[T] = []

    @property
    def items(self) -> list[T]:
        return list(self._current_items)

    def add(self, item: T) -> None:
        self._current_items.append(item)
        self._new_items.append(item)

    def remove(self, item: T) -> None:
        self._current_items.remove(item)
        self._removed_items.append(item)

    def get_new_items(self) -> list[T]:
        return list(self._new_items)

    def get_removed_items(self) -> list[T]:
        return list(self._removed_items)

    def get_updated_items(self) -> list[T]:
        return [
            item
            for item in self._current_items
            if item not in self._new_items and item not in self._removed_items
        ]
