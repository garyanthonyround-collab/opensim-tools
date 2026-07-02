# OpenSim Tools Development Guide

OpenSim Tools is an open-source Python toolkit for OpenSimulator administration.

## Philosophy

- Test-first development.
- One logical feature per commit.
- Keep commits small.
- Thin CLI.
- Rich reusable Python library.
- Follow the Single Responsibility Principle.
- Prefer composition over large classes.

## Architecture

Terrain subsystem:

CLI
→ TerrainProject
→ TerrainMosaic
→ TerrainModel

Region subsystem:

CLI
→ RegionProject
→ RegionModel
→ RegionIni

TerrainProject and RegionProject are orchestration layers.

Business logic belongs in models.

Do not place business logic inside CLI commands.

## Workflow

1. Write a failing pytest.
2. Implement the feature.
3. Run pytest.
4. Ensure all tests pass.
5. Stop before committing unless explicitly asked.

## Coding Style

- Prefer dataclasses for models.
- Keep methods small.
- Avoid duplicated logic.
- Avoid global state.
- Use pathlib rather than os.path.
- Maintain fluent APIs where appropriate.

## Current Goal

Develop the Region Management subsystem.

Current version: v0.9.x development.
