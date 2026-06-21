# OpenSim Tools Architecture

## Overview

OpenSim Tools is an object-oriented Python toolkit for administering OpenSimulator grids.

The project is designed as a reusable library with a lightweight command-line interface. All functionality is implemented within the library, allowing it to be reused by command-line tools, automation scripts, graphical applications, or third-party projects.

The long-term objective is to become the equivalent of **git** or **kubectl** for OpenSimulator administration.

---

# Architectural Principles

The project follows a number of core design principles.

## Single Responsibility

Each class has one clearly defined responsibility.

Processing logic belongs to processing classes.

Workflow orchestration belongs to workflow classes.

The command-line interface contains no business logic.

---

## Library First

The library is the primary product.

The command-line interface is simply a thin wrapper around the library API.

This makes the toolkit reusable from Python while keeping the CLI straightforward.

---

## Test First

Development follows a test-driven workflow.

Every feature is implemented as:

1. Write a failing test.
2. Implement the feature.
3. Run the complete test suite.
4. Commit a single logical feature.

This produces a clean and understandable Git history.

---

# Layered Architecture

The terrain subsystem is organised into four layers.

```text
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
 ▼
Low-level terrain utilities
```

Each layer has a single responsibility.

---

# Layer Responsibilities

## Low-Level Utilities

Low-level modules provide individual terrain processing operations.

Current modules include:

* ascii_grid.py
* normalize.py
* preview.py
* r32.py
* resample.py

These modules perform isolated processing tasks and contain no workflow logic.

---

## TerrainModel

`TerrainModel` represents terrain data held in memory.

It is responsible for terrain manipulation.

Current operations include:

* Loading ASCII Grid files
* Cropping
* Resampling
* Height normalisation
* Mean smoothing
* PNG preview generation
* RAW32 export

`TerrainModel` has no knowledge of terrain tiles or projects.

---

## TerrainMosaic

`TerrainMosaic` represents a collection of terrain tiles.

Responsibilities include:

* Managing tile collections
* Validating tile layouts
* Loading ASCII Grid files
* Stitching terrain into a single NumPy array
* Producing a TerrainModel

It has no knowledge of project configuration.

---

## OSTile

`OSTile` represents a single Ordnance Survey Terrain 50 tile.

Responsibilities include:

* Grid reference parsing
* Dataset path resolution
* Tile metadata
* Tile origin calculation

---

## TerrainProject

`TerrainProject` is the primary public API for terrain generation.

It represents an entire terrain generation workflow rather than an individual processing operation.

Current configuration options include:

* Project centre
* Physical project size
* Output resolution
* Height range
* Smoothing passes

Calling `build()` executes the complete workflow.

---

# Terrain Generation Pipeline

The complete terrain generation pipeline is:

```text
Project configuration
        │
        ▼
Determine project bounds
        │
        ▼
Determine required terrain tiles
        │
        ▼
Load terrain tiles
        │
        ▼
Construct TerrainMosaic
        │
        ▼
Generate TerrainModel
        │
        ▼
Crop
        │
        ▼
Resample
        │
        ▼
Normalise
        │
        ▼
Smooth
        │
        ▼
Finished TerrainModel
```

Each processing stage is optional where appropriate.

`TerrainProject` orchestrates the workflow while `TerrainModel` performs the processing.

---

# Public API

The recommended public API is the fluent `TerrainProject` interface.

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

# Class Relationships

```text
TerrainProject
        │
        ▼
TerrainMosaic
        │
        ▼
TerrainModel
        ▲
        │
Low-level processing modules
```

The relationships are intentionally one-directional.

Low-level processing modules know nothing about higher-level workflow classes.

---

# Current Package Structure

```text
opensim_tools/
    terrain/
        ascii_grid.py
        normalize.py
        os_grid.py
        preview.py
        project.py
        mosaic.py
        model.py
        r32.py
        resample.py
```

Each module contains one primary responsibility.

---

# Future Architecture

The terrain subsystem is intended to become one component within the wider OpenSim administration toolkit.

The same architectural pattern will be used throughout the project.

```text
TerrainProject
RegionProject
ServiceProject
AssetProject
BackupProject
DatabaseProject
```

Each project class will provide a high-level workflow while delegating processing to specialised domain classes.

This consistent architecture will allow both the command-line interface and external Python applications to interact with OpenSimulator through a unified and reusable API.

