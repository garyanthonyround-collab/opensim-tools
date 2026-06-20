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

def test_mosaic_extent(tmp_path):
    dataset = tmp_path / "data"

    write_ascii_grid(dataset / "ny" / "NY43.asc", 340000, 530000)
    write_ascii_grid(dataset / "ny" / "NY44.asc", 340000, 540000)

    mosaic = TerrainMosaic.from_tiles(
        OSTile("NY43", dataset=dataset),
        OSTile("NY44", dataset=dataset),
    )

    assert mosaic.extent == (340000, 530000, 350000, 550000)

def write_ascii_grid(path, xllcorner, yllcorner):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        f.write("ncols 2\n")
        f.write("nrows 2\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write("cellsize 50\n")
        f.write("NODATA_value -9999\n")
        f.write("1 1\n")
        f.write("1 1\n")
