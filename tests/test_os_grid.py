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
