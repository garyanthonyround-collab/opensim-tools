from opensim_tools.region.ini import RegionIni
from opensim_tools.region.model import RegionModel


def test_region_ini_contains_region_name():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
    )

    ini = RegionIni.from_model(region)

    assert "RegionName = Welcome" in ini.text

def test_region_ini_can_be_written(tmp_path):
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
    )

    ini = RegionIni.from_model(region)

    output = tmp_path / "Region.ini"

    ini.write(output)

    assert output.exists()
    assert "RegionName = Welcome" in output.read_text()

def test_region_ini_contains_region_location():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1001,
    )

    ini = RegionIni.from_model(region)

    assert "Location = 1000,1001" in ini.text

def test_region_ini_contains_region_size():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        size=256,
    )

    ini = RegionIni.from_model(region)

    assert "SizeX = 256" in ini.text
    assert "SizeY = 256" in ini.text

def test_region_ini_contains_internal_address():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    ini = RegionIni.from_model(region)

    assert "InternalAddress = 0.0.0.0" in ini.text

def test_region_ini_contains_internal_port():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
    )

    ini = RegionIni.from_model(region)

    assert "InternalPort = 9000" in ini.text
