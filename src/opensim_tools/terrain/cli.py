from pathlib import Path
import click
import numpy as np
import json

from .ascii_grid import read_ascii_grid
from .resample import resample_nearest, resample_bilinear, smooth_mean
from .normalize import normalize_height
from .r32 import write_r32
from .preview import write_preview_png

@click.group()
def main():
    """OpenSimulator terrain tools."""
    pass

@main.command()
@click.argument("path")
def info(path):
    """Show basic info about an ASCII Grid file."""
    header, data = read_ascii_grid(path)

    click.echo(f"File: {path}")
    click.echo(f"Grid: {data.shape[1]} cols x {data.shape[0]} rows")
    click.echo(f"Cell size: {header.get('cellsize')} m")
    click.echo(f"Origin: {header.get('xllcorner')}, {header.get('yllcorner')}")
    click.echo(f"Elevation min/max: {np.nanmin(data):.2f} / {np.nanmax(data):.2f} m")
    click.echo(f"Header: {header}")

@main.command("write-r32")
@click.argument("asc_file")
@click.argument("out_file")
@click.option("--size", default=256, show_default=True)
@click.option("--offset", default=None, type=float)
@click.option("--scale", default=None, type=float)
@click.option("--min-height", default=None, type=float)
@click.option("--max-height", default=None, type=float)
def write_r32_cmd(asc_file, out_file, size, offset, scale, min_height, max_height):
    """Convert an ASCII Grid tile to OpenSim .r32 terrain."""
    header, data = read_ascii_grid(asc_file)

    terrain = resample_bilinear(data, size=size)

    if (min_height is None) != (max_height is None):
        raise click.ClickException("--min-height and --max-height must be used together.")

    if min_height is not None:
        terrain = normalize_height(terrain, min_height, max_height)
    else:
        terrain = (terrain - (offset or 0.0)) * (scale or 1.0)

    write_r32(out_file, terrain)

    click.echo(f"Wrote: {out_file}")
    click.echo(f"Shape: {terrain.shape[1]} cols x {terrain.shape[0]} rows")
    click.echo(f"Elevation min/max: {np.nanmin(terrain):.2f} / {np.nanmax(terrain):.2f} m")


@main.command()
@click.argument("asc_file")
@click.argument("out_file")
@click.option("--size", default=256, show_default=True)
@click.option("--min-height", default=None, type=float)
@click.option("--max-height", default=None, type=float)
def preview(asc_file, out_file, size, min_height, max_height):
    """Create a PNG preview from an ASCII Grid tile."""
    _, data = read_ascii_grid(asc_file)

    terrain = resample_bilinear(data, size=size)

    if (min_height is None) != (max_height is None):
        raise click.ClickException("--min-height and --max-height must be used together.")

    if min_height is not None:
        terrain = normalize_height(terrain, min_height, max_height)

    write_preview_png(out_file, terrain)

    click.echo(f"Wrote preview: {out_file}")
    click.echo(f"Elevation min/max: {np.nanmin(terrain):.2f} / {np.nanmax(terrain):.2f} m")

@main.command()
@click.argument("asc_file")
@click.argument("out_prefix")
@click.option("--size", default=256, show_default=True)
@click.option("--min-height", default=2.0, show_default=True)
@click.option("--max-height", default=65.0, show_default=True)
@click.option("--smooth", default=1, show_default=True, help="Number of smoothing passes.")
def build(asc_file, out_prefix, size, min_height, max_height, smooth):
    """Build OpenSim terrain files: .r32 plus preview .png."""
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
        "source": asc_file,
        "header": header,
        "output": {
            "r32": r32_path,
            "preview": png_path,
            "size": size,
            "min_height": float(np.nanmin(terrain)),
            "max_height": float(np.nanmax(terrain)),
            "smooth": smooth,
        },
    }

    Path(json_path).write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    click.echo(f"Wrote terrain: {r32_path}")
    click.echo(f"Wrote preview: {png_path}")
    click.echo(f"Wrote metadata: {json_path}")
    click.echo(f"Shape: {terrain.shape[1]} cols x {terrain.shape[0]} rows")
    click.echo(f"Elevation min/max: {np.nanmin(terrain):.2f} / {np.nanmax(terrain):.2f} m")
