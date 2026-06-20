from opensim_tools.terrain.os_grid import OSTile


def test_os_tile_normalises_reference():
    tile = OSTile("ny43")
    assert tile.reference == "NY43"


def test_os_tile_path():
    tile = OSTile("NY43")
    assert str(tile.path).endswith("/srv/gis/os-terrain50/data/ny/NY43.asc")


def test_invalid_tile_reference():
    try:
        OSTile("bad")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")

def test_os_tile_origin_from_ascii_header(tmp_path):
    dataset = tmp_path / "data"
    write_ascii_grid(dataset / "ny" / "NY43.asc", 340000, 530000)

    tile = OSTile("NY43", dataset=dataset)

    assert tile.origin == (340000, 530000)

def test_os_tile_bounds_from_ascii_header(tmp_path):
    dataset = tmp_path / "data"
    write_ascii_grid(dataset / "ny" / "NY43.asc", 340000, 530000)

    tile = OSTile("NY43", dataset=dataset)

    assert tile.bounds == (340000, 530000, 350000, 540000)

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
