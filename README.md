# OpenSim Tools

OpenSim Tools is a modern Python toolkit for administering OpenSimulator grids and processing terrain datasets.

It is designed to provide a clean, scriptable, and extensible command-line interface for common OpenSimulator administration tasks, including terrain generation, region management, backups, database maintenance, and automation.

The long-term goal is to become the equivalent of **git** or **kubectl** for OpenSimulator administration.

---

# Current Features

## Terrain Processing

* Read Ordnance Survey Terrain 50 ASCII Grid files
* Automatically select required terrain tiles
* Stitch multiple terrain tiles into a terrain mosaic
* Crop terrain to a requested project area
* Bilinear terrain resampling
* Height normalisation
* Mean smoothing
* Generate PNG terrain previews
* Export OpenSimulator RAW32 (`.r32`) terrain files

---

# Library API

OpenSim Tools is designed as an object-oriented Python library with a fluent API.

```python
from opensim_tools.terrain import TerrainProject

terrain = (
    TerrainProject()
        .centre("NY4452")
        .size(1024)
        .resolution(512)
        .height_range(2, 65)
        .smooth(1)
        .build()
)

terrain.write_r32("terrain.r32")
terrain.write_preview("terrain.png")
```

---

# Terrain Workflow

`TerrainProject` automatically performs the complete terrain generation workflow:

* Select required terrain tiles
* Build a terrain mosaic
* Crop to the requested project bounds
* Resample to the requested output resolution
* Normalise terrain heights
* Apply optional smoothing

The resulting `TerrainModel` can then be exported as an OpenSimulator RAW32 terrain or previewed as a PNG image.

---

# Design Philosophy

OpenSim Tools is designed as a reusable Python library.

The command-line interface is intentionally lightweight and delegates all processing to the underlying library.

Current architecture:

```
CLI
 │
 ▼
TerrainProject
 │
 ▼
TerrainMosaic
 │
 ▼
TerrainModel
 │
 ├── Crop
 ├── Resample
 ├── Normalize
 ├── Smooth
 ├── RAW32 Export
 └── PNG Preview
```

Each class has a single responsibility.

| Class            | Responsibility                            |
| ---------------- | ----------------------------------------- |
| `TerrainProject` | High-level terrain workflow orchestration |
| `TerrainMosaic`  | Tile collection and stitching             |
| `TerrainModel`   | Terrain processing operations             |
| `OSTile`         | Represents a single OS Terrain 50 tile    |

---

# Installation

Clone the repository:

```bash
git clone https://github.com/<username>/opensim-tools.git
cd opensim-tools
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package:

```bash
pip install -e .
```

---

# Running Tests

```bash
pytest
```

Current status:

* ✅ 30 tests
* ✅ 30 passing

---

# Project Status

Current release:

**v0.8.0**

Implemented:

* TerrainProject workflow API
* Automatic terrain tile selection
* Terrain mosaics
* Automatic terrain cropping
* Automatic terrain resampling
* Automatic height normalisation
* Automatic smoothing
* RAW32 terrain export
* PNG preview generation

---

# Roadmap

## v0.9

* Region management
* Region creation
* Region.ini generation
* OpenSimulator configuration tools

## v1.x

A complete OpenSimulator administration toolkit including:

* Terrain
* Regions
* Varregions
* Services
* Assets
* Databases
* Backups
* Automation
* Command-line administration

---

# Contributing

Contributions, bug reports, feature requests, and pull requests are welcome.

Development follows a test-first approach using `pytest`.

Every feature should:

* Begin with a failing test
* Be implemented in small incremental commits
* Preserve a clean, reusable library architecture
* Include appropriate unit tests

---

# Licence

MIT License

