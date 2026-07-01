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

def test_region_ini_contains_external_hostname():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    ini = RegionIni.from_model(region)

    assert "ExternalHostName = SYSTEMIP" in ini.text

def test_region_ini_disables_alternate_ports():
    region = RegionModel(name="Welcome", x=1000, y=1000)

    ini = RegionIni.from_model(region)

    assert "AllowAlternatePorts = False" in ini.text

def test_region_ini_contains_terrain_image():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        terrain="welcome.r32",
    )

    ini = RegionIni.from_model(region)

    assert "TerrainImage = welcome.r32" in ini.text

def test_region_ini_uses_region_name():
    region = RegionModel(
        name="Sandbox",
        x=1000,
        y=1000,
    )

    ini = RegionIni.from_model(region)

    assert "[Sandbox]" in ini.text
    assert "RegionName = Sandbox" in ini.text

def test_region_ini_contains_terrain_image():
    region = RegionModel(
        name="Welcome",
        x=1000,
        y=1000,
        terrain="welcome.r32",
    )

    ini = RegionIni.from_model(region)

    assert "TerrainImage = welcome.r32" in ini.text
