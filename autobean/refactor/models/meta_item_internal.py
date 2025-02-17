from typing import Generic, ItemsView, Iterable, Iterator, KeysView, Mapping, MutableMapping, Optional, Type, TypeVar, ValuesView, no_type_check, overload
from .meta_item import MetaItem
from .meta_value import MetaRawValue, MetaValue
from . import base, internal

_V = TypeVar('_V')
_W = TypeVar('_W', bound='internal.RepeatedNodeWrapper[MetaItem]')


class _Empty:
    pass


_EMPTY = _Empty()


class _DictView(Generic[_W]):
    def __init__(self, wrapper: internal.RepeatedNodeWrapper[MetaItem]):
        self._wrapper = wrapper

    def __len__(self) -> int:
        return len(self._wrapper)


class RepeatedRawMetaKeysView(_DictView['RepeatedRawMetaItemWrapper'], KeysView[str]):
    def __iter__(self) -> Iterator[str]:
        for item in self._wrapper:
            yield item.key

    def __reversed__(self) -> Iterator[str]:
        for item in reversed(self._wrapper):
            yield item.key


class RepeatedRawMetaValuesView(_DictView['RepeatedRawMetaItemWrapper'], ValuesView[MetaItem]):
    def __iter__(self) -> Iterator[MetaItem]:
        return iter(self._wrapper)

    def __reversed__(self) -> Iterator[MetaItem]:
        return reversed(self._wrapper)


class RepeatedRawMetaItemsView(_DictView['RepeatedRawMetaItemWrapper'], ItemsView[str, MetaItem]):
    def __iter__(self) -> Iterator[tuple[str, MetaItem]]:
        for item in self._wrapper:
            yield item.key, item

    def __reversed__(self) -> Iterator[tuple[str, MetaItem]]:
        for item in reversed(self._wrapper):
            yield item.key, item


class RepeatedRawMetaItemWrapper(internal.RepeatedNodeWrapper[MetaItem], MutableMapping[str, MetaItem]):
    @overload
    def __getitem__(self, index: int) -> MetaItem:
        ...
    @overload
    def __getitem__(self, index: slice) -> list[MetaItem]:
        ...
    @overload
    def __getitem__(self, index: str) -> MetaItem:
        ...
    def __getitem__(self, index: int | slice | str) -> MetaItem | list[MetaItem] | MetaItem:
        if not isinstance(index, str):
            return super().__getitem__(index)
        for item in self._repeated.items:
            if item.key == index:
                return item
        raise KeyError(index)

    def __delitem__(self, index: int | slice | str) -> None:
        if not isinstance(index, str):
            return super().__delitem__(index)
        for i, item in enumerate(self._repeated.items):
            if item.key == index:
                return super().__delitem__(i)
        raise KeyError(index)

    @overload
    def __setitem__(self, index: int, value: MetaItem) -> None:
        ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[MetaItem]) -> None:
        ...
    @overload
    def __setitem__(self, index: str, value: MetaItem) -> None:
        ...
    @no_type_check  # mypy does not seem to work well with overload
    def __setitem__(self, index: int | slice | str, value: MetaItem | Iterable[MetaItem]) -> None:
        if not isinstance(index, str):
            return super().__setitem__(index, value)
        for i, item in enumerate(self._repeated.items):
            if item.key == index:
                return super().__setitem__(i, value)
        self.append(value)

    @overload
    def pop(self, index: int = -1) -> MetaItem:
        ...
    @overload
    def pop(self, index: str) -> MetaItem:
        ...
    @overload
    def pop(self, index: str, default: _V) -> MetaItem | _V:
        ...
    def pop(self, index: int | str = -1, default: _V | _Empty = _EMPTY) -> MetaItem | _V:
        if not isinstance(index, str):
            return super().pop(index)
        for i, item in enumerate(self._repeated.items):
            if item.key == index:
                return super().pop(i)
        if not isinstance(default, _Empty):
            return default
        raise KeyError(index)

    def keys(self) -> KeysView[str]:
        return RepeatedRawMetaKeysView(self)

    def values(self) -> ValuesView[MetaItem]:
        return RepeatedRawMetaValuesView(self)

    def items(self) -> ItemsView[str, MetaItem]:
        return RepeatedRawMetaItemsView(self)


class RepeatedMetaKeysView(_DictView['RepeatedMetaItemWrapper'], KeysView[str]):
    def __iter__(self) -> Iterator[str]:
        for item in self._wrapper:
            yield item.key

    def __reversed__(self) -> Iterator[str]:
        for item in reversed(self._wrapper):
            yield item.key


class RepeatedMetaValuesView(_DictView['RepeatedMetaItemWrapper'], ValuesView[Optional[MetaValue]]):
    def __iter__(self) -> Iterator[Optional[MetaValue]]:
        for item in self._wrapper:
            yield item.value

    def __reversed__(self) -> Iterator[Optional[MetaValue]]:
        for item in reversed(self._wrapper):
            yield item.value


class RepeatedMetaItemsView(_DictView['RepeatedMetaItemWrapper'], ItemsView[str, Optional[MetaValue]]):
    def __iter__(self) -> Iterator[tuple[str, Optional[MetaValue]]]:
        for item in self._wrapper:
            yield item.key, item.value

    def __reversed__(self) -> Iterator[tuple[str, Optional[MetaValue]]]:
        for item in reversed(self._wrapper):
            yield item.key, item.value


class RepeatedMetaItemWrapper(internal.RepeatedNodeWrapper[MetaItem], MutableMapping[str, Optional[MetaValue | MetaRawValue]]):
    @overload
    def __getitem__(self, index: int) -> MetaItem:
        ...
    @overload
    def __getitem__(self, index: slice) -> list[MetaItem]:
        ...
    @overload
    def __getitem__(self, index: str) -> Optional[MetaValue]:
        ...
    def __getitem__(self, index: int | slice | str) -> MetaItem | list[MetaItem] | Optional[MetaValue]:
        if not isinstance(index, str):
            return super().__getitem__(index)
        for item in self._repeated.items:
            if item.key == index:
                return item.value
        raise KeyError(index)

    def __delitem__(self, index: int | slice | str) -> None:
        if not isinstance(index, str):
            return super().__delitem__(index)
        for i, item in enumerate(self._repeated.items):
            if item.key == index:
                return super().__delitem__(i)
        raise KeyError(index)

    @overload
    def __setitem__(self, index: int, value: MetaItem) -> None:
        ...
    @overload
    def __setitem__(self, index: slice, value: Iterable[MetaItem]) -> None:
        ...
    @overload
    def __setitem__(self, index: str, value: Optional[MetaValue | MetaRawValue]) -> None:
        ...
    @no_type_check  # mypy does not seem to work well with overload
    def __setitem__(self, index: int | slice | str, value: MetaItem | Iterable[MetaItem] | Optional[MetaValue | MetaRawValue]) -> None:
        if not isinstance(index, str):
            return super().__setitem__(index, value)
        for _, item in enumerate(self._repeated.items):
            if item.key == index:
                item.value = value
                return
        self.append(MetaItem.from_value(index, value))

    @overload
    def pop(self, index: int = -1) -> MetaItem:
        ...
    @overload
    def pop(self, index: str) -> Optional[MetaValue]:
        ...
    @overload
    def pop(self, index: str, default: _V) -> Optional[MetaValue] | _V:
        ...
    def pop(self, index: int | str = -1, default: _V | _Empty = _EMPTY) -> MetaItem | Optional[MetaValue] | _V:
        if not isinstance(index, str):
            return super().pop(index)
        for i, item in enumerate(self._repeated.items):
            if item.key != index:
                continue
            item = super().pop(i)
            value = item.value
            if isinstance(value, base.RawModel) and value.token_store:
                if prev := value.token_store.get_prev(value.first_token):
                    value.token_store.remove(item.first_token, prev)
                if next := value.token_store.get_next(value.last_token):
                    value.token_store.remove(next, item.last_token)
            return value
        if not isinstance(default, _Empty):
            return default
        raise KeyError(index)

    def keys(self) -> KeysView[str]:
        return RepeatedMetaKeysView(self)

    def values(self) -> ValuesView[Optional[MetaValue]]:
        return RepeatedMetaValuesView(self)

    def items(self) -> ItemsView[str, Optional[MetaValue]]:
        return RepeatedMetaItemsView(self)


class repeated_raw_meta_item_property:
    def __init__(self, inner_field: internal.repeated_field[MetaItem]):
        self._inner_field = inner_field

    def __set_name__(self, owner: base.RawTreeModel, name: str) -> None:
        self._name = name

    def __get__(self, instance: base.RawTreeModel, owner: Optional[Type[base.RawTreeModel]] = None) -> RepeatedRawMetaItemWrapper:
        repeated = self._inner_field.__get__(instance, owner)
        wrapper = RepeatedRawMetaItemWrapper(repeated, self._inner_field)
        setattr(instance, self._name, wrapper)
        return wrapper


class repeated_meta_item_property:
    def __init__(self, inner_field: internal.repeated_field[MetaItem]):
        self._inner_field = inner_field

    def __set_name__(self, owner: base.RawTreeModel, name: str) -> None:
        self._name = name

    def __get__(self, instance: base.RawTreeModel, owner: Optional[Type[base.RawTreeModel]] = None) -> RepeatedMetaItemWrapper:
        repeated = self._inner_field.__get__(instance, owner)
        wrapper = RepeatedMetaItemWrapper(repeated, self._inner_field)
        setattr(instance, self._name, wrapper)
        return wrapper


def from_mapping(mapping: Mapping[str, MetaValue | MetaRawValue]) -> Iterator[MetaItem]:
    for key, value in mapping.items():
        yield MetaItem.from_value(key, value)
