from dataclasses import dataclass


@dataclass
class ColumnProfile:
    """Jedna kolumna tabeli, tak jak zobaczył ją Data Scan."""

    name: str
    type_name: str
    null_pct: float
    distinct: int
    example: str
    is_key: bool = False
    references: str = ""
