from dataclasses import dataclass, field
from typing import List

from ColumnProfile import ColumnProfile


@dataclass
class TableProfile:
    """Jeden plik źródłowy: format, liczba wierszy i profile kolumn."""

    name: str
    source_format: str
    rows: int
    columns: List[ColumnProfile] = field(default_factory=list)

    def key(self) -> str:
        keys = [c.name for c in self.columns if c.is_key]
        return keys[0] if keys else ""
