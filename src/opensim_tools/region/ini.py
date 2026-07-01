from pathlib import Path

class RegionIni:

    def __init__(self, text):
        self.text = text

    @classmethod
    def from_model(cls, model):
        text = (
            "[Welcome]\n"
            "RegionName = Welcome\n"
            "Location = 1000,1001\n"
            "SizeX = 256\n"
            "SizeY = 256\n"
            "InternalAddress = 0.0.0.0\n"
            "InternalPort = 9000\n"
        )

        return cls(text)

    def write(self, path: Path):
        path.write_text(self.text)
