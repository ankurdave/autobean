# DO NOT EDIT
# This file is automatically generated by autobean.refactor.modelgen.

from typing import Type, TypeVar, final
from .. import base
from .. import internal
from ..punctuation import Whitespace
from ..tag import Tag

_Self = TypeVar('_Self', bound='Poptag')


@internal.token_model
class PoptagLabel(internal.SimpleDefaultRawTokenModel):
    RULE = 'POPTAG'
    DEFAULT = 'poptag'


@internal.tree_model
class Poptag(base.RawTreeModel):
    RULE = 'poptag'

    _label = internal.required_field[PoptagLabel]()
    _tag = internal.required_field[Tag]()

    raw_tag = internal.required_node_property(_tag)

    tag = internal.required_string_property(raw_tag)

    @final
    def __init__(
            self,
            token_store: base.TokenStore,
            label: PoptagLabel,
            tag: Tag,
    ):
        super().__init__(token_store)
        self._label = label
        self._tag = tag

    @property
    def first_token(self) -> base.RawTokenModel:
        return self._label.first_token

    @property
    def last_token(self) -> base.RawTokenModel:
        return self._tag.last_token

    def clone(self: _Self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> _Self:
        return type(self)(
            token_store,
            self._label.clone(token_store, token_transformer),
            self._tag.clone(token_store, token_transformer),
        )
    
    def _reattach(self, token_store: base.TokenStore, token_transformer: base.TokenTransformer) -> None:
        self._token_store = token_store
        self._label = self._label.reattach(token_store, token_transformer)
        self._tag = self._tag.reattach(token_store, token_transformer)

    def _eq(self, other: base.RawTreeModel) -> bool:
        return (
            isinstance(other, Poptag)
            and self._label == other._label
            and self._tag == other._tag
        )

    @classmethod
    def from_children(
            cls: Type[_Self],
            tag: Tag,
    ) -> _Self:
        label = PoptagLabel.from_default()
        tokens = [
            *label.detach(),
            Whitespace.from_default(),
            *tag.detach(),
        ]
        token_store = base.TokenStore.from_tokens(tokens)
        label.reattach(token_store)
        tag.reattach(token_store)
        return cls(token_store, label, tag)
