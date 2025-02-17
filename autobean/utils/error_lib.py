from typing import Iterable, NamedTuple
from beancount.loader import LoadError
from beancount.core.data import Directive, Meta


class Error(NamedTuple):
    source: Meta
    message: str
    entry: Directive | list[Directive] | None


class InvalidDirectiveError(Error):
    pass


class ErrorLogger:
    errors: list[Error]

    def __init__(self) -> None:
        self.errors = []

    def log_error(self, error: Error) -> None:
        self.errors.append(error)

    def log_errors(self, errors: Iterable[Error]) -> None:
        self.errors.extend(errors)

    def log_loading_errors(self, errors: Iterable[Error], entry: Directive) -> None:
        for error in errors:
            if isinstance(error, LoadError):
                error = error._replace(
                    source=entry.meta,
                    entry=entry,
                )
            self.errors.append(error)
