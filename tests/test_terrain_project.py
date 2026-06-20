from opensim_tools.terrain.project import TerrainProject


def test_terrain_project_stores_centre_reference():
    project = TerrainProject().centre("NY4452")

    assert project.centre_reference == "NY4452"
