from dataclasses import dataclass

import numpy as np

from .ascii_grid import read_ascii_grid
from .normalize import normalize_height
from .preview import write_preview_png
from .r32 import write_r32
from .resample import resample_bilinear, smooth_mean


@dataclass
class TerrainModel:
    header: dict
    data: np.ndarray

    @classmethod
    def from_ascii(cls, filename):
        header, data = read_ascii_grid(filename)
        return cls(header, data)

    def crop(self, x, y, width, height):
        cellsize = self.header.get("cellsize", 1)

        row_start = y
        row_end = y + height
        col_start = x
        col_end = x + width

        self.data = self.data[row_start:row_end, col_start:col_end]

        self.header["ncols"] = width
        self.header["nrows"] = height
        self.header["xllcorner"] = self.header.get("xllcorner", 0) + (x * cellsize)
        self.header["yllcorner"] = self.header.get("yllcorner", 0) + (y * cellsize)

        return self

    def resample(self, size=256):
        self.data = resample_bilinear(self.data, size=size)
        return self

    def normalize(self, minimum=2.0, maximum=65.0):
        self.data = normalize_height(self.data, minimum, maximum)
        return self

    def smooth(self, passes=1):
        if passes > 0:
            self.data = smooth_mean(self.data, passes)
        return self

    def write_preview(self, filename):
        write_preview_png(filename, self.data)

    def write_r32(self, filename):
        write_r32(filename, self.data)
