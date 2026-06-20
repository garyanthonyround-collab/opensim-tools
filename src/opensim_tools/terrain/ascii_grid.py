from pathlib import Path
import numpy as np

HEADER_KEYS = {
    "ncols", "nrows", "xllcorner", "yllcorner",
    "xllcenter", "yllcenter", "cellsize", "nodata_value",
}

def read_ascii_grid(path):
    header = {}
    data_lines = []

    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) == 2 and parts[0].lower() in HEADER_KEYS:
                header[parts[0].lower()] = float(parts[1])
            else:
                data_lines.append(line)
                break

        data_lines.extend(f.readlines())

    data = np.array(
        [[float(v) for v in line.split()] for line in data_lines if line.strip()],
        dtype=float,
    )

    nodata = header.get("nodata_value")
    if nodata is not None:
        data = np.where(data == nodata, np.nan, data)

    return header, data
