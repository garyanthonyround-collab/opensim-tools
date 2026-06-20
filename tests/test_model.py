import numpy as np

from opensim_tools.terrain.model import TerrainModel


def test_terrain_model_resample_normalize_smooth():
    data = np.array([[0.0, 10.0], [20.0, 30.0]])
    terrain = TerrainModel({}, data)

    terrain.resample(4).normalize(2, 65).smooth(1)

    assert terrain.data.shape == (4, 4)
    assert terrain.data.min() >= 2
    assert terrain.data.max() <= 65
