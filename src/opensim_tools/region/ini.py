from pathlib import Path

class RegionIni:

    def __init__(self, text):
        self.text = text

    @classmethod
    def from_model(cls, model):
        text = (
            "[Welcome]\n"
            "RegionName = Welcome\n"
        )

        return cls(text)

    def write(self, path: Path):
        path.write_text(self.text)
