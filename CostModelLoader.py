import time

from CostModel import CostModel
from DataScanner import DataScanner
from DemoCostData import DemoCostData
from PipelineStep import PipelineStep
from ProjectFolders import ProjectFolders
from TableReader import TableReader


class CostModelLoader:
    """Wczytuje produkty, BOM, ceny surowców i koszty stałe z input/, sprawdza spójność i robi Data Scan."""

    REQUIRED = {
        "products.xlsx": ["product_id", "name", "sell_price", "annual_volume", "labour_cost"],
        "bom.csv": ["product_id", "resource_id", "qty_per_unit"],
        "resources.json": ["resource_id", "name", "unit", "price"],
        "overheads.json": ["cost_id", "name", "annual_pln"],
    }

    def __init__(self, folders: ProjectFolders, reader: TableReader, generator: DemoCostData, scanner: DataScanner):
        self.folders = folders
        self.reader = reader
        self.generator = generator
        self.scanner = scanner

    def model(self) -> CostModel:
        demo = self.generator.ensure(self.folders)
        started = time.perf_counter()
        tables = {}
        for name, columns in self.REQUIRED.items():
            path = self.folders.input_path(name)
            frame = self.reader.read(path)
            missing = [c for c in columns if c not in frame.columns]
            if missing:
                raise ValueError("%s: brak kolumn %s" % (name, ", ".join(missing)))
            tables[name] = (self.reader.format_of(path), frame)
        loaded = time.perf_counter() - started
        frames = {name: frame for name, (_, frame) in tables.items()}
        scan = self.scanner.scan(tables)
        rows = sum(len(frame) for frame in frames.values())
        scan.pipeline.insert(0, PipelineStep("Load", "%d plików (CSV, JSON, Excel), %d wierszy" % (len(frames), rows), loaded))
        started = time.perf_counter()
        self.validate(frames)
        scan.pipeline.append(PipelineStep("Validate", "każda pozycja BOM ma produkt i cenę surowca", time.perf_counter() - started))
        return CostModel(products=frames["products.xlsx"], bom=frames["bom.csv"], resources=frames["resources.json"],
                         overheads=frames["overheads.json"], scan=scan, demo=demo)

    @staticmethod
    def validate(frames) -> None:
        bom = frames["bom.csv"]
        unknown_products = set(bom.product_id) - set(frames["products.xlsx"].product_id)
        unknown_resources = set(bom.resource_id) - set(frames["resources.json"].resource_id)
        if unknown_products or unknown_resources:
            raise ValueError("BOM wskazuje nieznane produkty %s lub surowce %s" % (sorted(unknown_products), sorted(unknown_resources)))
