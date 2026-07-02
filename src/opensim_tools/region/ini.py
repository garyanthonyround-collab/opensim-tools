from pathlib import Path


class RegionIni:

    def __init__(self, text):
        self.text = text

    @classmethod
    def from_model(cls, model):
        text = (
            f"[{model.name}]\n"
            f"RegionName = {model.name}\n"
            f"Location = {model.x},{model.y}\n"
            f"SizeX = {model.size}\n"
            f"SizeY = {model.size}\n"
            "InternalAddress = 0.0.0.0\n"
            f"InternalPort = {model.internal_port}\n"
            "ExternalHostName = SYSTEMIP\n"
            "AllowAlternatePorts = False\n"
        )

        if model.terrain:
            text += f"TerrainImage = {model.terrain}\n"

        if model.estate:
            text += f"EstateName = {model.estate}\n"

        return cls(text)

    def write(self, path: Path):
        path.write_text(self.text)
