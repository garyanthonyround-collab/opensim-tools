from opensim_tools.region.model import RegionModel


def test_region_model_stores_name():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.name == "Welcome"

def test_region_model_stores_location():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.x == 1000
    assert region.y == 1000

def test_region_model_defaults_to_standard_size():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.size == 256


def test_region_model_stores_size():
    region = RegionModel(name="Welcome", x=1000, y=1000, size=512)

    assert region.size == 512
