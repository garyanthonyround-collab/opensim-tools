def write_ascii_grid(path, xllcorner, yllcorner, value=1):
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w") as f:
        f.write("ncols 2\n")
        f.write("nrows 2\n")
        f.write(f"xllcorner {xllcorner}\n")
        f.write(f"yllcorner {yllcorner}\n")
        f.write("cellsize 50\n")
        f.write("NODATA_value -9999\n")
        f.write(f"{value} {value}\n")
        f.write(f"{value} {value}\n")
