from opensim_tools.terrain.project import TerrainProject


def test_terrain_project_stores_centre_reference():
    project = TerrainProject().centre("NY4452")

    assert project.centre_reference == "NY4452"

def test_terrain_project_parses_centre_reference():
    project = TerrainProject().centre("NY4452")

    assert project.centre_point == (344000, 520000)
