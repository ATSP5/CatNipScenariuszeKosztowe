class PlnFormat:
    """Liczby po polsku: spacja tysięcy, przecinek dziesiętny, kwoty w zł, tys. i mln."""

    def formatter(self) -> "PlnFormat":
        return self

    @staticmethod
    def num(value: float, decimals: int = 0) -> str:
        if value is None or value != value:
            return "—"
        if value in (float("inf"), float("-inf")):
            return "∞"
        if round(value, decimals) == 0:
            value = 0.0
        return format(value, ",.%df" % decimals).replace(",", " ").replace(".", ",").replace("-", "−")

    @classmethod
    def zl(cls, value: float, decimals: int = 0) -> str:
        return cls.num(value, decimals) + " zł"

    @classmethod
    def short_zl(cls, value: float) -> str:
        if abs(value) >= 1_000_000:
            return cls.num(value / 1_000_000, 2) + " mln zł"
        if abs(value) >= 1_000:
            return cls.num(value / 1_000, 0) + " tys. zł"
        return cls.zl(value)

    @classmethod
    def pct(cls, value: float, decimals: int = 1) -> str:
        return cls.num(value, decimals) + "%"

    @classmethod
    def signed_pct(cls, value: float, decimals: int = 1) -> str:
        return ("+" if round(value, decimals) > 0 else "") + cls.pct(value, decimals)

    @classmethod
    def pp(cls, value: float, decimals: int = 1) -> str:
        return ("+" if round(value, decimals) > 0 else "") + cls.num(value, decimals) + " pp"
