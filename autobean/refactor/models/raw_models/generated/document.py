# DO NOT EDIT
# This file is automatically generated by autobean.refactor.modelgen.

from typing import Type, TypeVar, final
from .. import base
from .. import internal
from ..account import Account
from ..date import Date
from ..escaped_string import EscapedString
from ..punctuation import Whitespace

_Self = TypeVar('_Self', bound='Document')


@internal.token_model
class DocumentLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'DOCUMENT'
    DEFAULT = 'document'


@internal.tree_model
class Document(base.RawTreeModel):
    RULE = 'document'

    _date = internal.required_field[Date]()
    _label = internal.required_field[DocumentLabel]()
    _account = internal.required_field[Account]()
    _filename = internal.required_field[EscapedString]()

    raw_date = internal.required_node_property(_date)
    raw_account = internal.required_node_property(_account)
    raw_filename = internal.required_node_property(_filename)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: DocumentLabel,
            account: Account,
            filename: EscapedString,
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._account = account
        self._filename = filename

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._filename.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._account.clone(token_store, token_transformer),
            self._filename.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._account = self._account.reattach(token_store, token_transformer)
        self._filename = self._filename.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Document)
            and self._date == other._date
            and self._label == other._label
            and self._account == other._account
            and self._filename == other._filename
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            account: Account,
            filename: EscapedString,
    ) -> _Self:
        label = DocumentLabel.from_default()
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *account.detach(),
            Whitespace.from_default(),
            *filename.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        account.reattach(token_store)
        filename.reattach(token_store)
        return cls(token_store, date, label, account, filename)
