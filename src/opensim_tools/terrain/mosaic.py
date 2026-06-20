from dataclasses import dataclass, field

from .os_grid import OSTile


@dataclass
class TerrainMosaic:
    tiles: list[OSTile] = field(default_factory=list)

    @classmethod
    def from_tiles(cls, *tile_refs):
        mosaic = cls()
        for tile_ref in tile_refs:
            mosaic.add_tile(tile_ref)
        return mosaic

    def add_tile(self, tile_ref):
        tile = tile_ref if isinstance(tile_ref, OSTile) else OSTile(tile_ref)
        self.tiles.append(tile)
        return self

    @property
    def references(self):
        return [tile.reference for tile in self.tiles]

    @property
    def paths(self):
        return [tile.path for tile in self.tiles]

    def missing_tiles(self):
        return [tile for tile in self.tiles if not tile.exists]

    def validate(self):
        missing = self.missing_tiles()
        if missing:
            refs = ", ".join(tile.reference for tile in missing)
            raise FileNotFoundError(f"Missing OS Terrain 50 tiles: {refs}")
        return self
