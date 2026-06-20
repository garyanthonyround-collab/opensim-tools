from pathlib import Path
import numpy as np
from PIL import Image

def write_preview_png(path, terrain):
    arr = np.asarray(terrain, dtype=float)
    mn = np.nanmin(arr)
    mx = np.nanmax(arr)

    if mx == mn:
        img = np.zeros(arr.shape, dtype=np.uint8)
    else:
        img = ((arr - mn) / (mx - mn) * 255).astype(np.uint8)

    Image.fromarray(img, mode="L").save(Path(path))
