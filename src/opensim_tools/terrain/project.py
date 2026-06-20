from dataclasses import dataclass


@dataclass
class TerrainProject:
    centre_reference: str | None = None

    def centre(self, reference: str):
        self.centre_reference = reference.upper()
        return self
