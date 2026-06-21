from opensim_tools.region.model import RegionModel


def test_region_model_stores_name():
    region = RegionModel(name="Welcome")

    assert region.name == "Welcome"
