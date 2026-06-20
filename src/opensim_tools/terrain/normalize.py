import numpy as np

def normalize_height(data, min_height, max_height):
    src_min = np.nanmin(data)
    src_max = np.nanmax(data)

    if src_max == src_min:
        raise ValueError("Cannot normalize a flat terrain tile.")

    out = (data - src_min) / (src_max - src_min)
    return out * (max_height - min_height) + min_height
