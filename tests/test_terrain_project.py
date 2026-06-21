from opensim_tools.terrain.project import TerrainProject

from opensim_tools.terrain.os_grid import OSTile

from opensim_tools.terrain.mosaic import TerrainMosaic

from opensim_tools.terrain.model import TerrainModel

def write_ascii_grid(path, xllcorner, yllcorner, value=1):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        f.write("ncols 2\n")
        f.write("nrows 2\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write("cellsize 50\n")
        f.write("NODATA_value -9999\n")
        f.write(f"{value} {value}\n")
        f.write(f"{value} {value}\n")

def test_terrain_project_builds_model(tmp_path):
    dataset = tmp_path / "data"
    write_ascii_grid(dataset / "ny" / "NY45.asc", 343950, 551950)

    project = (
        TerrainProject(dataset=dataset)
        .centre("NY4452")
        .size(100)
    )

    terrain = project.build()

    assert isinstance(terrain, TerrainModel)

def test_terrain_project_creates_mosaic(tmp_path):
    project = (
        TerrainProject(dataset=tmp_path)
        .centre("NY4452")
        .size(1024)
    )

    mosaic = project.mosaic

    assert isinstance(mosaic, TerrainMosaic)
    assert mosaic.references == ["NY45"]

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

def test_project_resolution_defaults_to_none():
    project = TerrainProject()

    assert project.resolution_samples is None


def test_project_resolution_can_be_set():
    project = TerrainProject().resolution(512)

    assert project.resolution_samples == 512

def test_project_build_crops_model_to_project_size():
    project = (
        TerrainProject()
        .centre("NY4452")
        .size(1024)
    )

    model = project.build()

    assert model.data.shape == (20, 20)

def test_project_build_resamples_when_resolution_set():
    project = (
        TerrainProject()
        .centre("NY4452")
        .size(1024)
        .resolution(512)
    )

    model = project.build()
  
    assert model.data.shape == (512,512)
