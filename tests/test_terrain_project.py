from opensim_tools.terrain.project import TerrainProject


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
