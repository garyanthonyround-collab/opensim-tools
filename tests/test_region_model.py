from opensim_tools.region.model import RegionModel


def test_region_model_stores_name():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.name == "Welcome"

def test_region_model_stores_location():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.x == 1000
    assert region.y == 1000
