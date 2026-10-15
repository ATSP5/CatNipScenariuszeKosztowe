from dataclasses import dataclass

import pandas as pd

from DataScan import DataScan


@dataclass
class CostModel:
    """Model kosztowy firmy: produkty, receptury (BOM), ceny surowców, koszty stałe i wynik Data Scan."""

    products: pd.DataFrame
    bom: pd.DataFrame
    resources: pd.DataFrame
    overheads: pd.DataFrame
    scan: DataScan
    demo: bool = False
