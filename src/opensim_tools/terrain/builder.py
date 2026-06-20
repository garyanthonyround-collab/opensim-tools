import json
from pathlib import Path

import numpy as np

from .model import TerrainModel
from .os_grid import OSTile


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

    def build_from_tile(
        self,
        tile_ref,
        out_prefix=None,
        size=256,
        min_height=2.0,
        max_height=65.0,
        smooth=1,
    ):
        tile = OSTile(tile_ref)

        if not tile.exists:
            raise FileNotFoundError(f"OS Terrain 50 tile not found: {tile.path}")

        if out_prefix is None:
            out_prefix = f"/var/lib/opensim/terrains/{tile.reference}"

        return self.build_from_file(
            tile.path,
            out_prefix,
            size=size,
            min_height=min_height,
            max_height=max_height,
            smooth=smooth,
        )
