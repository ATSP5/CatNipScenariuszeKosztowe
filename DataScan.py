from dataclasses import dataclass, field
from typing import Dict, List

from PipelineStep import PipelineStep
from TableProfile import TableProfile


@dataclass
class DataScan:
    """Wynik Data Scan: rozpoznane tabele, typy kolumn, klucze, powiązania i kroki przetwarzania."""

    tables: List[TableProfile] = field(default_factory=list)
    pipeline: List[PipelineStep] = field(default_factory=list)

    def total_rows(self) -> int:
        return sum(t.rows for t in self.tables)

    def relations(self) -> List[str]:
        return ["%s.%s → %s" % (t.name, c.name, c.references) for t in self.tables for c in t.columns if c.references]

    def tree_text(self) -> str:
        lines = []
        for table in self.tables:
            lines.append("%s  [%s, %s wierszy]" % (table.name, table.source_format, format(table.rows, ",").replace(",", " ")))
            width = max([len(c.name) for c in table.columns] + [4])
            for index, column in enumerate(table.columns):
                branch = "└─" if index == len(table.columns) - 1 else "├─"
                notes = []
                if column.is_key:
                    notes.append("klucz")
                if column.references:
                    notes.append("→ " + column.references)
                if column.null_pct > 0:
                    notes.append("braki %.1f%%" % column.null_pct)
                suffix = ("  (" + ", ".join(notes) + ")") if notes else ""
                lines.append(" %s %s → %s%s" % (branch, column.name.ljust(width), column.type_name.ljust(8), suffix))
            lines.append("")
        return "\n".join(lines).rstrip()

    def column_rows(self) -> List[Dict[str, object]]:
        return [{"Plik": t.name, "Kolumna": c.name, "Typ": c.type_name, "Unikalne": c.distinct,
                 "Braki %": round(c.null_pct, 1), "Przykład": c.example,
                 "Rola": "klucz" if c.is_key else ("→ " + c.references if c.references else "")}
                for t in self.tables for c in t.columns]

    def pipeline_rows(self) -> List[Dict[str, object]]:
        return [{"Krok": s.name, "Co": s.detail, "Czas [s]": round(s.seconds, 2)} for s in self.pipeline]
