from pathlib import Path
import numpy as np

def write_r32(path, terrain):
    terrain = np.asarray(terrain, dtype="<f4")
    Path(path).write_bytes(terrain.tobytes())
