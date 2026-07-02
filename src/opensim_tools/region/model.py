from dataclasses import dataclass


@dataclass
class RegionModel:
    name: str
    x: int
    y: int
    size: int = 256
    internal_port: int = 9000
    terrain: str | None = None
    estate: str | None = None
