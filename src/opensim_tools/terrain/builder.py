import json
from pathlib import Path
import numpy as np

from .ascii_grid import read_ascii_grid
from .normalize import normalize_height
from .preview import write_preview_png
from .r32 import write_r32
from .resample import resample_bilinear, smooth_mean


class TerrainBuilder:
    def build_from_file(
        self,
        asc_file,
        out_prefix,
        size=256,
        min_height=2.0,
        max_height=65.0,
        smooth=1,
    ):
        header, data = read_ascii_grid(asc_file)

        terrain = resample_bilinear(data, size=size)
        terrain = normalize_height(terrain, min_height, max_height)

        if smooth > 0:
            terrain = smooth_mean(terrain, passes=smooth)

        r32_path = f"{out_prefix}.r32"
        png_path = f"{out_prefix}.png"
        json_path = f"{out_prefix}.json"

        write_r32(r32_path, terrain)
        write_preview_png(png_path, terrain)

        metadata = {
            "source": str(asc_file),
            "header": header,
            "output": {
                "r32": r32_path,
                "preview": png_path,
                "metadata": json_path,
                "size": size,
                "min_height": float(np.nanmin(terrain)),
                "max_height": float(np.nanmax(terrain)),
                "smooth": smooth,
            },
        }

        Path(json_path).write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        return metadata
