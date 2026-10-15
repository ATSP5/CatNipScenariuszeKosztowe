import json
import os
from typing import Dict, List

import pandas as pd

from ProjectFolders import ProjectFolders


class DemoCostData:
    """Dane demonstracyjne producenta stolarki aluminiowej i PVC: produkty, BOM, ceny surowców i koszty stałe.

    Pliki powstają w input/ tylko wtedy, gdy ich tam nie ma — podmień je na dane firmy (te same kolumny).
    Ceny produktów są dobrane tak, żeby firma miała ok. 9% marży EBITDA, a najtańsze wyroby aluminiowe
    (parapety, rolety) — cienką marżę, którą wzrost ceny aluminium łatwo zjada.
    """

    FILES = ("products.xlsx", "bom.csv", "resources.json", "overheads.json")

    RESOURCES = [  # resource_id, nazwa, jednostka, cena, dostawca
        ("R-AL", "Aluminium (profile)", "kg", 13.20, "Hydro Extrusion"),
        ("R-GL", "Szkło zespolone", "m2", 140.00, "Pilkington"),
        ("R-ST", "Stal", "kg", 4.40, "Stalprodukt"),
        ("R-PVC", "Profil PVC", "kg", 9.50, "Veka"),
        ("R-EN", "Energia elektryczna", "kWh", 0.95, "Tauron"),
        ("R-HW", "Okucia", "kpl", 85.00, "Roto"),
        ("R-PK", "Opakowanie", "szt", 18.00, "Smurfit Kappa"),
    ]
    PRODUCTS = [  # product_id, nazwa, rodzina, roczny wolumen, robocizna na szt., docelowa marża pokrycia, BOM
        ("OA-1", "Okno aluminiowe OA-1", "Okna", 6000, 260, 0.30, {"R-AL": 14, "R-GL": 1.6, "R-HW": 1, "R-EN": 35, "R-PK": 1}),
        ("DA-2", "Drzwi aluminiowe DA-2", "Drzwi", 2200, 520, 0.32, {"R-AL": 28, "R-GL": 1.8, "R-HW": 1.5, "R-EN": 60, "R-PK": 1}),
        ("FS-3", "Fasada słupowo-ryglowa FS-3 (m²)", "Fasady", 9000, 210, 0.25, {"R-AL": 22, "R-GL": 1.05, "R-ST": 2, "R-EN": 40}),
        ("OP-4", "Okno PVC OP-4", "Okna", 14000, 150, 0.29, {"R-PVC": 16, "R-ST": 4, "R-GL": 1.6, "R-HW": 1, "R-EN": 20, "R-PK": 1}),
        ("BS-5", "Brama stalowa BS-5", "Bramy", 1500, 640, 0.27, {"R-ST": 85, "R-HW": 2, "R-EN": 90, "R-PK": 1}),
        ("BA-6", "Balustrada aluminiowa BA-6 (mb)", "Balustrady", 5000, 160, 0.23, {"R-AL": 9, "R-GL": 0.9, "R-EN": 15}),
        ("RA-7", "Roleta aluminiowa RA-7", "Osłony", 9000, 95, 0.13, {"R-AL": 7, "R-HW": 1, "R-EN": 12, "R-PK": 1}),
        ("PA-8", "Parapet aluminiowy PA-8 (mb)", "Parapety", 30000, 14, 0.09, {"R-AL": 3.2, "R-EN": 4, "R-PK": 0.5}),
    ]
    OVERHEAD_SHARES = [  # pozycja kosztów stałych i jej udział w sumie
        ("OH-01", "Wynagrodzenia administracji i sprzedaży", "Ludzie", 0.38),
        ("OH-02", "Utrzymanie hali i maszyn", "Produkcja", 0.22),
        ("OH-03", "Logistyka i flota", "Logistyka", 0.16),
        ("OH-04", "Marketing i targi", "Sprzedaż", 0.08),
        ("OH-05", "IT i licencje", "Administracja", 0.06),
        ("OH-06", "Ubezpieczenia, doradztwo, pozostałe", "Administracja", 0.10),
    ]
    TARGET_EBITDA_MARGIN = 0.09

    def generator(self) -> "DemoCostData":
        return self

    def ensure(self, folders: ProjectFolders) -> bool:
        """Tworzy brakujące pliki demonstracyjne; zwraca True, gdy coś zapisano."""
        if all(os.path.exists(folders.input_path(name)) for name in self.FILES):
            return False
        self.write(folders)
        return True

    def write(self, folders: ProjectFolders) -> None:
        prices = {r[0]: r[3] for r in self.RESOURCES}
        products = self.products(prices)
        pd.DataFrame(products).to_excel(folders.input_path("products.xlsx"), index=False)
        pd.DataFrame(self.bom()).to_csv(folders.input_path("bom.csv"), index=False)
        resources = [{"resource_id": r[0], "name": r[1], "unit": r[2], "price": r[3], "supplier": r[4]} for r in self.RESOURCES]
        self.write_json(resources, folders.input_path("resources.json"))
        self.write_json(self.overheads(products, prices), folders.input_path("overheads.json"))

    @staticmethod
    def write_json(records: List[dict], path: str) -> None:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(records, handle, ensure_ascii=False, indent=1)

    def unit_cost(self, bom: Dict[str, float], labour: float, prices: Dict[str, float]) -> float:
        return sum(qty * prices[rid] for rid, qty in bom.items()) + labour

    def products(self, prices: Dict[str, float]) -> List[dict]:
        rows = []
        for pid, name, family, volume, labour, margin, bom in self.PRODUCTS:
            price = self.unit_cost(bom, labour, prices) / (1 - margin)
            price = round(price, -1 if price >= 500 else 0)
            rows.append({"product_id": pid, "name": name, "family": family, "sell_price": price,
                         "annual_volume": volume, "labour_cost": labour})
        return rows

    def bom(self) -> List[dict]:
        return [{"product_id": pid, "resource_id": rid, "qty_per_unit": qty}
                for pid, _, _, _, _, _, bom in self.PRODUCTS for rid, qty in bom.items()]

    def overheads(self, products: List[dict], prices: Dict[str, float]) -> List[dict]:
        boms = {p[0]: (p[6], p[4]) for p in self.PRODUCTS}
        revenue = sum(p["sell_price"] * p["annual_volume"] for p in products)
        contribution = sum((p["sell_price"] - self.unit_cost(*boms[p["product_id"]], prices)) * p["annual_volume"] for p in products)
        fixed = contribution - self.TARGET_EBITDA_MARGIN * revenue
        return [{"cost_id": cid, "name": name, "category": category, "annual_pln": round(fixed * share, -3)}
                for cid, name, category, share in self.OVERHEAD_SHARES]
