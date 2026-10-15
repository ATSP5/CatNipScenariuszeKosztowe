import os
from typing import Dict, Optional

import pandas as pd


class TableReader:
    """Czyta tabelę z pliku CSV, JSON (lista rekordów) albo Excel do DataFrame."""

    FORMATS = {".csv": "CSV", ".json": "JSON", ".xlsx": "Excel", ".xls": "Excel"}

    def reader(self) -> "TableReader":
        return self

    def format_of(self, path: str) -> str:
        return self.FORMATS.get(os.path.splitext(path)[1].lower(), "?")

    def read(self, path: str, dtypes: Optional[Dict[str, str]] = None) -> pd.DataFrame:
        """dtypes: typy kolumn dla dużych CSV, np. {"customer_id": "category"} — oszczędza pamięć."""
        kind = self.format_of(path)
        if kind == "CSV":
            return pd.read_csv(path, dtype=dtypes)
        if kind == "JSON":
            return pd.read_json(path, orient="records", convert_dates=False)
        if kind == "Excel":
            return pd.read_excel(path)
        raise ValueError("Nieobsługiwany format pliku: %s" % path)
