import json
from pathlib import Path
import numpy as np

from .model import TerrainModel


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
        terrain = (
            TerrainModel.from_ascii(asc_file)
            .resample(size)
            .normalize(min_height, max_height)
            .smooth(smooth)
        )

        r32_path = f"{out_prefix}.r32"
        png_path = f"{out_prefix}.png"
        json_path = f"{out_prefix}.json"

        terrain.write_r32(r32_path)
        terrain.write_preview(png_path)

        metadata = {
            "source": str(asc_file),
            "header": terrain.header,
            "output": {
                "r32": r32_path,
                "preview": png_path,
                "metadata": json_path,
                "size": size,
                "min_height": float(np.nanmin(terrain.data)),
                "max_height": float(np.nanmax(terrain.data)),
                "smooth": smooth,
            },
        }

        Path(json_path).write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        return metadata
