import datetime
from typing import Type, TypeVar
from . import internal
from .account import Account
from .date import Date
from .generated import close
from .generated.close import CloseLabel

_Self = TypeVar('_Self', bound='Close')


@internal.tree_model
class Close(close.Close):

    @classmethod
    def from_value(cls: Type[_Self], date: datetime.date, account: str) -> _Self:
        return cls.from_children(Date.from_value(date), Account.from_value(account))
