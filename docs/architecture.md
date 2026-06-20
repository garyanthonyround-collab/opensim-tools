# OpenSim Tools Architecture

OpenSim Tools is designed as a reusable Python library with a thin command-line interface.

The project started as terrain conversion tooling, but its architecture is intended to support a much broader OpenSimulator administration toolkit over time.

The long-term goal is to provide a coherent toolset for terrain processing, region management, database operations, backups, services, assets, and automation.

---

## Design Principles

OpenSim Tools follows a few core principles:

1. **Library first, CLI second**
2. **Small classes with clear responsibilities**
3. **Composable terrain workflows**
4. **Test-first development**
5. **OpenSimulator-specific behaviour kept above generic terrain operations**

The command-line interface should not contain complex business logic. It should parse user input, call the library, and report results.

---

## Current Terrain Architecture

```text
CLI
 │
 ▼
TerrainBuilder
 │
 ├── OSTile
 │
 ├── TerrainMosaic
 │
 ▼
TerrainModel
 │
 ├── ascii_grid
 │
 ├── resample
 │
 ├── normalize
 │
 ├── preview
 │
 └── r32
```

The terrain system is built around four main classes:

| Class            | Responsibility                           |
| ---------------- | ---------------------------------------- |
| `OSTile`         | Represents one OS Terrain 50 tile        |
| `TerrainMosaic`  | Represents a collection of terrain tiles |
| `TerrainModel`   | Represents terrain data in memory        |
| `TerrainBuilder` | Orchestrates complete terrain workflows  |

---

## `OSTile`

`OSTile` represents a single Ordnance Survey Terrain 50 tile.

It is responsible for:

* Validating tile references
* Resolving tile paths
* Checking whether source files exist
* Reading tile origin coordinates
* Calculating tile bounds

Example:

```python
from opensim_tools.terrain.os_grid import OSTile

tile = OSTile("NY43")

print(tile.reference)
print(tile.path)
print(tile.exists)
print(tile.origin)
print(tile.bounds)
```

`OSTile` does not process terrain data. It only describes where a tile is and what its spatial extent is.

---

## `TerrainMosaic`

`TerrainMosaic` represents a group of `OSTile` objects.

It is responsible for:

* Managing tile collections
* Validating that required files exist
* Reporting tile references and paths
* Calculating mosaic extent
* Stitching tiles into a single `TerrainModel`

Example:

```python
from opensim_tools.terrain.mosaic import TerrainMosaic

mosaic = TerrainMosaic.from_tiles(
    "NY43",
    "NY44",
    "NY53",
    "NY54",
)

terrain = mosaic.to_model()
```

`TerrainMosaic.to_model()` loads each tile, orders tiles by origin coordinates, stitches their arrays together, and returns a `TerrainModel`.

It deliberately does **not** resample, normalise, smooth, crop, or export terrain. Those remain `TerrainModel` responsibilities.

---

## `TerrainModel`

`TerrainModel` represents terrain data in memory.

It contains:

* ASCII Grid header metadata
* A NumPy array of height values

It is responsible for terrain operations:

* Resampling
* Height normalisation
* Smoothing
* PNG preview export
* OpenSimulator RAW32 export

Example:

```python
terrain = (
    TerrainMosaic
        .from_tiles("NY43", "NY44", "NY53", "NY54")
        .to_model()
        .resample(512)
        .normalize(2, 65)
        .smooth(1)
)

terrain.write_r32("terrain.r32")
terrain.write_preview("terrain.png")
```

`TerrainModel` methods return `self` where appropriate, allowing fluent method chaining.

---

## `TerrainBuilder`

`TerrainBuilder` provides higher-level workflow orchestration.

It is intended for cases where callers want a complete terrain-processing pipeline rather than manually composing lower-level objects.

Current responsibilities include:

* Building terrain from an ASCII Grid file
* Building terrain from an OS Terrain 50 tile
* Applying resampling
* Applying normalisation
* Applying smoothing
* Writing output files and metadata

`TerrainBuilder` is useful for command-line workflows, while `TerrainModel`, `OSTile`, and `TerrainMosaic` remain useful for direct library usage.

---

## Module Responsibilities

| Module          | Responsibility                          |
| --------------- | --------------------------------------- |
| `ascii_grid.py` | Read OS Terrain 50 ASCII Grid files     |
| `model.py`      | In-memory terrain model                 |
| `mosaic.py`     | Multi-tile terrain mosaics              |
| `os_grid.py`    | OS Terrain 50 tile references and paths |
| `builder.py`    | High-level terrain build workflows      |
| `normalize.py`  | Height normalisation                    |
| `resample.py`   | Resampling and smoothing                |
| `preview.py`    | PNG preview generation                  |
| `r32.py`        | OpenSimulator RAW32 export              |

---

## Data Flow

A typical terrain mosaic workflow follows this path:

```text
Tile references
      │
      ▼
OSTile objects
      │
      ▼
TerrainMosaic
      │
      ▼
ASCII Grid files
      │
      ▼
NumPy arrays
      │
      ▼
TerrainModel
      │
      ├── resample
      ├── normalise
      ├── smooth
      ├── write preview
      └── write RAW32
```

This keeps data loading, spatial organisation, terrain transformation, and file output separate.

---

## Why the CLI Should Stay Thin

The CLI should act as an adapter rather than the core of the application.

Good CLI responsibilities:

* Parse command-line arguments
* Validate user input
* Call library classes
* Display output
* Return suitable exit codes

Poor CLI responsibilities:

* Parsing terrain files directly
* Manually stitching arrays
* Performing resampling logic
* Writing OpenSimulator formats directly
* Owning database or service-management behaviour

Keeping the CLI thin makes the project easier to test and easier to reuse from scripts, notebooks, services, or future graphical tools.

---

## Testing Philosophy

Every new feature should include tests.

Current test coverage includes:

* `TerrainModel`
* `OSTile`
* `TerrainMosaic`
* Terrain stitching via `TerrainMosaic.to_model()`

Tests are run with:

```bash
pytest
```

The project should continue to prefer small unit tests around library behaviour rather than large end-to-end tests around CLI output.

---

## Future Architecture

OpenSim Tools is expected to grow beyond terrain processing.

Potential future packages:

```text
opensim_tools/
│
├── terrain/
├── regions/
├── database/
├── services/
├── assets/
├── backups/
└── cli/
```

Possible future responsibilities:

| Package    | Responsibility                                          |
| ---------- | ------------------------------------------------------- |
| `terrain`  | Terrain processing and varregion support                |
| `regions`  | Region creation, cloning, configuration, and inspection |
| `database` | MariaDB backup, restore, and diagnostics                |
| `services` | systemd integration and service monitoring              |
| `assets`   | Asset and inventory tooling                             |
| `backups`  | OAR/IAR/archive workflows                               |
| `cli`      | Command-line interface adapters                         |

The terrain package should remain a self-contained subsystem while the wider project grows around it.

---

## Release Direction

Current milestone:

* `v0.6.0` — Terrain mosaics and stitching

Planned milestones:

* `v0.7.0` — Documentation, GitHub Actions, packaging polish
* `v0.8.0` — Varregion terrain support
* `v0.9.0` — Region administration tools
* `v1.0.0` — Stable OpenSimulator administration toolkit

---

## Summary

OpenSim Tools is intentionally structured around composable, testable Python objects.

The current terrain architecture separates:

* Tile identity: `OSTile`
* Tile collections: `TerrainMosaic`
* Terrain data and operations: `TerrainModel`
* Workflow orchestration: `TerrainBuilder`
* User interaction: CLI

This separation keeps the codebase maintainable today and gives the project room to grow into a broader OpenSimulator administration toolkit.
