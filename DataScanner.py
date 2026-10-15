import time
from typing import Dict, List, Tuple

import pandas as pd

from ColumnProfile import ColumnProfile
from DataScan import DataScan
from PipelineStep import PipelineStep
from TableProfile import TableProfile


class DataScanner:
    """Data Scan: rozpoznaje typy kolumn, klucze i powiązania między plikami — bez ręcznego opisu danych."""

    SAMPLE = 5000

    def scanner(self) -> "DataScanner":
        return self

    def scan(self, tables: Dict[str, Tuple[str, pd.DataFrame]]) -> DataScan:
        """tables: nazwa pliku -> (format, DataFrame)."""
        started = time.perf_counter()
        profiles = [TableProfile(name, source_format, len(frame), [self.profile_column(frame[c]) for c in frame.columns])
                    for name, (source_format, frame) in tables.items()]
        self.mark_keys(profiles, tables)
        self.link_references(profiles, tables)
        scan = DataScan(profiles)
        detail = "%d plików, %d kolumn, %d powiązań" % (len(profiles), sum(len(p.columns) for p in profiles),
                                                        len(scan.relations()))
        scan.pipeline.append(PipelineStep("Data Scan", detail, time.perf_counter() - started))
        return scan

    def profile_column(self, series: pd.Series) -> ColumnProfile:
        sample = series.dropna()
        if len(sample) > self.SAMPLE:
            sample = sample.sample(self.SAMPLE, random_state=0)
        example = str(sample.iloc[0]) if len(sample) else ""
        return ColumnProfile(name=str(series.name), type_name=self.type_of(series, sample),
                             null_pct=float(series.isna().mean() * 100),
                             distinct=int(series.nunique(dropna=True)), example=example[:30])

    @staticmethod
    def type_of(series: pd.Series, sample: pd.Series) -> str:
        if pd.api.types.is_bool_dtype(series):
            return "bool"
        if pd.api.types.is_integer_dtype(series):
            return "int"
        if pd.api.types.is_float_dtype(series):
            return "int" if len(sample) and bool((sample % 1 == 0).all()) else "decimal"
        if pd.api.types.is_datetime64_any_dtype(series):
            return "DateTime"
        if len(sample) and bool(sample.astype(str).str.match(r"^\d{4}-\d{2}-\d{2}").all()):
            return "DateTime"
        return "string"

    @staticmethod
    def is_id_name(name: str) -> bool:
        lowered = name.lower()
        return lowered == "id" or lowered.endswith("_id")

    def mark_keys(self, profiles: List[TableProfile], tables: Dict[str, Tuple[str, pd.DataFrame]]) -> None:
        for profile in profiles:
            frame = tables[profile.name][1]
            for column in profile.columns:
                values = frame[column.name]
                if self.is_id_name(column.name) and bool(values.notna().all()) and values.is_unique:
                    column.is_key = True
                    break

    def link_references(self, profiles: List[TableProfile], tables: Dict[str, Tuple[str, pd.DataFrame]]) -> None:
        owners = [(p.key(), p.name) for p in profiles if p.key()]
        for profile in profiles:
            frame = tables[profile.name][1]
            for column in profile.columns:
                if column.is_key:
                    continue
                for key, owner in owners:
                    if key == column.name and owner != profile.name:
                        own_values = pd.Series(frame[column.name].dropna().unique())
                        if bool(own_values.isin(tables[owner][1][key]).all()):
                            column.references = "%s.%s" % (owner, key)
