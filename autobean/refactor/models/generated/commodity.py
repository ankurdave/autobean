# DO NOT EDIT
# This file is automatically generated by autobean.refactor.modelgen.

import datetime
from typing import Iterable, Mapping, Optional, Type, TypeVar, final
from .. import base, internal, meta_item_internal
from ..currency import Currency
from ..date import Date
from ..meta_item import MetaItem
from ..meta_value import MetaRawValue, MetaValue
from ..punctuation import Eol, Newline, Whitespace

_Self = TypeVar('_Self', bound='Commodity')


@internal.token_model
class CommodityLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'COMMODITY'
    DEFAULT = 'commodity'


@internal.tree_model
class Commodity(base.RawTreeModel):
    RULE = 'commodity'

    _date = internal.required_field[Date]()
    _label = internal.required_field[CommodityLabel]()
    _currency = internal.required_field[Currency]()
    _eol = internal.required_field[Eol]()
    _meta = internal.repeated_field[MetaItem](separators=(Newline.from_default(), Whitespace.from_raw_text('    ')))

    raw_date = internal.required_node_property(_date)
    raw_currency = internal.required_node_property(_currency)
    raw_meta = meta_item_internal.repeated_raw_meta_item_property(_meta)

    date = internal.required_date_property(raw_date)
    currency = internal.required_string_property(raw_currency)
    meta = meta_item_internal.repeated_meta_item_property(_meta)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            date: Date,
            label: CommodityLabel,
            currency: Currency,
            eol: Eol,
            meta: internal.Repeated[MetaItem],
    ):
        super().__init__(token_store)
        self._date = date
        self._label = label
        self._currency = currency
        self._eol = eol
        self._meta = meta

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._date.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._meta.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._date.clone(token_store, token_transformer),
            self._label.clone(token_store, token_transformer),
            self._currency.clone(token_store, token_transformer),
            self._eol.clone(token_store, token_transformer),
            self._meta.clone(token_store, token_transformer),
        )

    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._date = self._date.reattach(token_store, token_transformer)
        self._label = self._label.reattach(token_store, token_transformer)
        self._currency = self._currency.reattach(token_store, token_transformer)
        self._eol = self._eol.reattach(token_store, token_transformer)
        self._meta = self._meta.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Commodity)
            and self._date == other._date
            and self._label == other._label
            and self._currency == other._currency
            and self._eol == other._eol
            and self._meta == other._meta
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            date: Date,
            currency: Currency,
            meta: Iterable[MetaItem] = (),
    ) -> _Self:
        label = CommodityLabel.from_default()
        eol = Eol.from_default()
        repeated_meta = internal.Repeated.from_children(meta, separators=cls._meta.separators)
        tokens = [
            *date.detach(),
            Whitespace.from_default(),
            *label.detach(),
            Whitespace.from_default(),
            *currency.detach(),
            *eol.detach(),
            *repeated_meta.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        date.reattach(token_store)
        label.reattach(token_store)
        currency.reattach(token_store)
        eol.reattach(token_store)
        repeated_meta.reattach(token_store)
        return cls(token_store, date, label, currency, eol, repeated_meta)

    @classmethod
    def from_value(
            cls: Type[_Self],
            date: datetime.date,
            currency: str,
            *,
            meta: Optional[Mapping[str, MetaValue | MetaRawValue]] = None,
    ) -> _Self:
        return cls.from_children(
            Date.from_value(date),
            Currency.from_value(currency),
            meta_item_internal.from_mapping(meta) if meta is not None else (),
        )
