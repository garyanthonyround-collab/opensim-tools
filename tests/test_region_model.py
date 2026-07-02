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

def test_region_model_defaults_to_standard_internal_port():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.internal_port == 9000


def test_region_model_stores_internal_port():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        internal_port=9001,
    )

    assert region.internal_port == 9001

def test_region_model_has_no_terrain_by_default():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    assert region.terrain is None


def test_region_model_stores_terrain():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        terrain="welcome.r32",
    )

    assert region.terrain == "welcome.r32"

def test_region_model_has_no_estate_by_default():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
    )

    assert region.estate is None


def test_region_model_stores_estate():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        estate="Main Estate",
    )

    assert region.estate == "Main Estate"
