import datetime
import decimal
from typing import Iterable, Iterator, Mapping, NoReturn, Optional, Type, TypeVar, Union, cast

from . import internal, meta_item_internal
from .generated import custom
from .generated.custom import CustomLabel, CustomRawValue
from .escaped_string import EscapedString
from .date import Date
from .account import Account
from .amount import Amount
from .bool import Bool
from .number_expr import NumberExpr
from .number_unary_expr import NumberUnaryExpr
from .meta_item import MetaItem
from .meta_value import MetaRawValue, MetaValue

_ValueTypeSimplified = str | datetime.date | bool | decimal.Decimal
_ValueTypePreserved = Account | Amount
CustomValue = Union[_ValueTypeSimplified, _ValueTypePreserved]
_Self = TypeVar('_Self', bound='Custom')


def _simplify_value(raw_value: CustomRawValue) -> CustomValue:
    if isinstance(raw_value, EscapedString | Date | Bool | NumberExpr):
        return raw_value.value
    return raw_value


def _unsimplify_value(value: CustomValue | CustomRawValue) -> CustomRawValue:
    match value:
        case str():
            return EscapedString.from_value(value)
        case datetime.date():
            return Date.from_value(value)
        case bool():
            return Bool.from_value(value)
        case decimal.Decimal():
            return NumberExpr.from_value(value)
        case _:
            return value


def _disambiguate_values(values: Iterable[CustomRawValue]) -> Iterator[CustomRawValue]:
    prev = None
    for value in values:
        if isinstance(prev, NumberExpr):
            if isinstance(value, Amount):
                number = value.raw_number
            elif isinstance(value, NumberExpr):
                number = value
            else:
                number = None
            if number is not None and isinstance(
                    number.raw_number_add_expr.raw_operands[0].raw_operands[0], NumberUnaryExpr):
                number.wrap_with_parenthesis()
        yield value
        prev = value


def _update_raw(raw_value: CustomRawValue, value: CustomValue) -> bool:
    match raw_value, value:
        case EscapedString() as r, str() as v:
            r.value = v
        case Date() as r, datetime.date() as v:
            r.value = v
        case Bool() as r, bool() as v:
            r.value = v
        case NumberExpr() as r, decimal.Decimal() as v:
            r.value = v
        case _:
            return False
    return True


# TODO: disambiguate values inserted through repeated wrapper
@internal.tree_model
class Custom(custom.Custom):

    @property
    def values(self) -> internal.RepeatedValueWrapper[CustomRawValue, CustomValue]:
        wrapper = self.__dict__.get('values')
        if wrapper:
            return wrapper
        wrapper = internal.RepeatedValueWrapper[CustomRawValue, CustomValue, NoReturn](
            raw_wrapper=self.raw_values,
            # cast as mypy isn't good at handling unions
            raw_type=cast(Type[CustomRawValue], CustomRawValue),
            type=cast(Type[CustomValue], CustomValue),
            from_raw_type=_simplify_value,
            to_raw_type=_unsimplify_value,
            update_raw=_update_raw,
        )
        self.__dict__['values'] = wrapper
        return wrapper

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            type: EscapedString,
            values: Iterable[CustomRawValue],
            meta: Iterable[MetaItem] = (),
    ) -> _Self:
        return super().from_children(date, type, _disambiguate_values(values), meta)

    @classmethod
    def from_value(
            cls: Type[_Self],
            date: datetime.date,
            type: str,
            values: Iterable[CustomValue | CustomRawValue],
            *,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
    ) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            EscapedString.from_value(type),
            map(_unsimplify_value, values),
            meta_item_internal.from_mapping(meta) if meta is not None else (),
        )
