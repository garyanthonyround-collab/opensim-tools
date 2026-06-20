from opensim_tools.terrain.mosaic import TerrainMosaic
from opensim_tools.terrain.os_grid import OSTile


def test_mosaic_from_tiles_normalises_references():
    mosaic = TerrainMosaic.from_tiles("ny43", "ny44")
    assert mosaic.references == ["NY43", "NY44"]


def test_mosaic_accepts_ostile_instances():
    mosaic = TerrainMosaic()
    mosaic.add_tile(OSTile("ny43"))
    assert mosaic.references == ["NY43"]


def test_mosaic_paths():
    mosaic = TerrainMosaic.from_tiles("NY43")
    assert str(mosaic.paths[0]).endswith("/srv/gis/os-terrain50/data/ny/NY43.asc")
