import numpy as np
import pytest

from opensim_tools.terrain.model import TerrainModel


def test_terrain_model_crop():
    data = np.arange(100).reshape((10, 10))

    model = TerrainModel(
        {
            "ncols": 10,
            "nrows": 10,
            "xllcorner": 0,
            "yllcorner": 0,
            "cellsize": 1,
            "nodata_value": -9999,
        },
        data,
    )

    model.crop(2, 3, 4, 5)

    assert model.data.shape == (5, 4)
    assert np.array_equal(model.data, data[3:8, 2:6])


def test_terrain_model_crop_updates_header():
    data = np.arange(100).reshape((10, 10))

    model = TerrainModel(
        {
            "ncols": 10,
            "nrows": 10,
            "xllcorner": 100,
            "yllcorner": 200,
            "cellsize": 10,
            "nodata_value": -9999,
        },
        data,
    )

    model.crop(2, 3, 4, 5)

    assert model.header["ncols"] == 4
    assert model.header["nrows"] == 5
    assert model.header["xllcorner"] == 120
    assert model.header["yllcorner"] == 230
