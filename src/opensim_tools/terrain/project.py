from dataclasses import dataclass


@dataclass
class TerrainProject:
    centre_reference: str | None = None
    centre_point: tuple[int, int] | None = None
    size_m: int | None = None

    def centre(self, reference: str):
        self.centre_reference = reference.upper()
        self.centre_point = self._parse_reference(reference)
        return self

    def size(self, metres: int):
        self.size_m = metres
        return self

    def _parse_reference(self, reference: str) -> tuple[int, int]:
        ref = reference.upper()

        if len(ref) != 6:
            raise ValueError(f"Invalid centre reference: {reference}")

        prefix = ref[:2]
        digits = ref[2:]

        if prefix != "NY" or not digits.isdigit():
            raise ValueError(f"Invalid centre reference: {reference}")

        east = int(digits[:2]) * 1000
        north = int(digits[2:]) * 1000

        return 300000 + east, 500000 + north
