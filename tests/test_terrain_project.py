from opensim_tools.terrain.project import TerrainProject

from opensim_tools.terrain.os_grid import OSTile


def test_terrain_project_required_tiles_are_os_tiles():
    project = (
        TerrainProject()
        .centre("NY4452")
        .size(1024)
    )

    tiles = project.required_tiles

    assert len(tiles) == 1
    assert isinstance(tiles[0], OSTile)
    assert tiles[0].reference == "NY45"

def test_terrain_project_stores_centre_reference():
    project = TerrainProject().centre("NY4452")

    assert project.centre_reference == "NY4452"

def test_terrain_project_parses_centre_reference():
    project = TerrainProject().centre("NY4452")

    assert project.centre_point == (344000, 552000)

def test_terrain_project_stores_size():
    project = TerrainProject().size(1024)

    assert project.size_m == 1024

def test_terrain_project_bounds():
    project = (
        TerrainProject()
        .centre("NY4452")
        .size(1024)
    )

    assert project.bounds == (
        343488,
        551488,
        344512,
        552512,
    )

def test_terrain_project_required_tiles():
    project = (
        TerrainProject()
        .centre("NY4452")
        .size(1024)
    )

    assert project.required_tile_references == ["NY45"]

def test_terrain_project_required_tiles_use_dataset(tmp_path):
    project = (
        TerrainProject(dataset=tmp_path)
        .centre("NY4452")
        .size(1024)
    )

    tiles = project.required_tiles

    assert tiles[0].dataset == tmp_path
