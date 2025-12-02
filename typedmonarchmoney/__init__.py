"""Init."""

# Apply patches before importing TypedMonarchMoney
from . import patch  # noqa: F401

from .monarchmoney_typed import TypedMonarchMoney

__all__ = ["TypedMonarchMoney"]
