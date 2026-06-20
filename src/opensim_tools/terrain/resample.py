import numpy as np

def resample_nearest(data, size=256):
    y_idx = np.linspace(0, data.shape[0] - 1, size).round().astype(int)
    x_idx = np.linspace(0, data.shape[1] - 1, size).round().astype(int)
    return data[np.ix_(y_idx, x_idx)]

def resample_bilinear(data, size=256):
    data = np.asarray(data, dtype=float)

    src_h, src_w = data.shape
    dst_y = np.linspace(0, src_h - 1, size)
    dst_x = np.linspace(0, src_w - 1, size)

    x, y = np.meshgrid(dst_x, dst_y)

    x0 = np.floor(x).astype(int)
    x1 = np.clip(x0 + 1, 0, src_w - 1)
    y0 = np.floor(y).astype(int)
    y1 = np.clip(y0 + 1, 0, src_h - 1)

    x_weight = x - x0
    y_weight = y - y0

    top = data[y0, x0] * (1 - x_weight) + data[y0, x1] * x_weight
    bottom = data[y1, x0] * (1 - x_weight) + data[y1, x1] * x_weight

    return top * (1 - y_weight) + bottom * y_weight

def smooth_mean(data, passes=1):
    out = np.asarray(data, dtype=float)

    for _ in range(passes):
        padded = np.pad(out, 1, mode="edge")
        out = (
            padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:] +
            padded[1:-1, :-2] + padded[1:-1, 1:-1] + padded[1:-1, 2:] +
            padded[2:, :-2] + padded[2:, 1:-1] + padded[2:, 2:]
        ) / 9.0

    return out
