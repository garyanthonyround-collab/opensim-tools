import pytest
import numpy as np

from opensim_tools.terrain.mosaic import TerrainMosaic
from opensim_tools.terrain.model import TerrainModel
from opensim_tools.terrain.os_grid import OSTile


def test_mosaic_to_model_returns_terrain_model(sample_mosaic):
    model = sample_mosaic.to_model()

    assert isinstance(model, TerrainModel)


def test_mosaic_to_model_stitches_tiles_by_origin(sample_mosaic):
    model = sample_mosaic.to_model()

    assert model.data.shape == (400, 400)

    # top-left tile
    assert np.all(model.data[0:200, 0:200] == 1)

    # top-right tile
    assert np.all(model.data[0:200, 200:400] == 2)

    # bottom-left tile
    assert np.all(model.data[200:400, 0:200] == 3)

    # bottom-right tile
    assert np.all(model.data[200:400, 200:400] == 4)

def write_ascii_grid(path, value, xllcorner, yllcorner):
    data = np.full((200, 200), value)

    with open(path, "w") as f:
        f.write("ncols 200\n")
        f.write("nrows 200\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write("cellsize 50\n")
        f.write("NODATA_value -9999\n")

        for row in data:
            f.write(" ".join(str(v) for v in row) + "\n")


@pytest.fixture
def sample_mosaic(tmp_path):
    dataset = tmp_path / "data"
    ny_dir = dataset / "ny"
    ny_dir.mkdir(parents=True)

    tile_specs = [
        ("NY43", 1, 400000, 300000),
        ("NY44", 2, 410000, 300000),
        ("NY53", 3, 400000, 290000),
        ("NY54", 4, 410000, 290000),
    ]

    tiles = []

    for reference, value, x, y in tile_specs:
        path = ny_dir / f"{reference}.asc"
        write_ascii_grid(path, value, x, y)
        tiles.append(OSTile(reference, dataset=dataset))

    return TerrainMosaic.from_tiles(*tiles)
