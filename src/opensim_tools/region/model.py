from dataclasses import dataclass


@dataclass
class RegionModel:
    name: str
    x: int
    y: int
    size: int = 256
    terrain: str | None = None
    estate: str | None = None
