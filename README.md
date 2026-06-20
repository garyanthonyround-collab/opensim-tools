OpenSim Tools
OpenSim Tools is a modern Python toolkit for administering OpenSimulator grids and processing terrain datasets.
It is designed to provide a clean, scriptable, and extensible command-line interface for common OpenSimulator administration tasks, including terrain generation, region management, backups, database maintenance, and automation.
The long-term goal is to become the equivalent of git or kubectl for OpenSimulator administration.
________________________________________
Current Features
Terrain Processing
•	Read Ordnance Survey Terrain 50 ASCII Grid files
•	Stitch multiple terrain tiles into a single terrain model
•	Bilinear terrain resampling
•	Height normalisation
•	Mean smoothing
•	Generate PNG terrain previews
•	Export OpenSimulator RAW32 (.r32) terrain files
Library API
Object-oriented design with fluent method chaining.
from opensim_tools.terrain import TerrainMosaic

terrain = (
    TerrainMosaic
        .from_tiles(
            "NY43",
            "NY44",
            "NY53",
            "NY54",
        )
        .to_model()
        .resample(512)
        .normalize(2, 65)
        .smooth(1)
)

terrain.write_r32("terrain.r32")
terrain.write_preview("terrain.png")
________________________________________
Design Philosophy
OpenSim Tools is designed as a reusable Python library.
The command-line interface is intentionally lightweight and delegates all processing to the underlying library.
Current architecture:
CLI
 │
 ▼
TerrainBuilder
 │
 ▼
TerrainMosaic
 │
 ▼
TerrainModel
 │
 ▼
ASCII Grid
RAW32
PNG Preview
Resampling
Normalisation
Each class has a single responsibility.
Class	Responsibility
TerrainBuilder	High-level workflows
TerrainMosaic	Tile collection and stitching
TerrainModel	Terrain processing operations
OSTile	Represents a single OS Terrain 50 tile
________________________________________
Installation
Clone the repository:
git clone https://github.com/<username>/opensim-tools.git
cd opensim-tools
Create a virtual environment:
python3 -m venv .venv
source .venv/bin/activate
Install dependencies:
pip install -e .
________________________________________
Running Tests
pytest
Current status:
•	✅ 12 tests
•	✅ 12 passing
________________________________________
Project Status
Current release:
v0.6.0
Implemented:
•	TerrainBuilder
•	TerrainModel
•	TerrainMosaic
•	OSTile
•	Terrain stitching
•	Terrain resampling
•	Terrain normalisation
•	RAW32 export
•	PNG preview generation
________________________________________
Roadmap
v0.7
•	Project documentation
•	GitHub Actions
•	Packaging improvements
•	API polishing
v0.8
•	Automatic terrain stitching
•	OpenSimulator varregion support
•	Terrain cropping
•	Terrain padding
v0.9
•	Region administration
•	Database utilities
•	Backup and restore tools
•	OpenSimulator service management
v1.0
A comprehensive administration toolkit for OpenSimulator grids.
________________________________________
Contributing
Contributions, bug reports, feature requests, and pull requests are welcome.
Development follows a test-first approach using pytest, and all new features should include appropriate unit tests.
________________________________________
Licence
MIT License



