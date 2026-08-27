# GeoSim Studio

> A modular geospatial processing pipeline for transforming GIS, terrain, and AI-derived information into simulation-ready assets.

## Overview

GeoSim Studio is structured as a modular geospatial engineering project. It separates the data lifecycle from domain-specific processing so ingestion, normalization, geometry, terrain, feature enrichment, AI analysis, validation, and packaging can evolve independently.

The current implementation includes a feature enrichment and validation pipeline that converts cleaned building and road datasets into richer simulation primitives.

## Architecture

```text
GeoSim Studio
│
├── data/                         # Data lifecycle and pipeline outputs
│   ├── raw/                      # Source data
│   ├── processed/                # Intermediate datasets
│   ├── normalized/               # Normalized datasets and metadata
│   ├── phase1_output/            # Phase outputs
│   ├── phase2_output/
│   ├── phase3_output/
│   └── export/                   # Export-ready artifacts
│
└── geo-core/                     # Core geospatial processing
    ├── ingestion/                # Data acquisition
    ├── normalization/            # CRS and data normalization
    ├── geometry/                 # Geometry processing
    ├── terrain/                  # Terrain processing
    ├── features_Enrichment_Engine/
    │   ├── cli/                  # Command-line interface
    │   ├── features/             # Feature enrichment logic
    │   ├── schema/               # Feature schemas
    │   └── validation/           # Validation engine
    ├── ai/                       # AI-assisted geospatial components
    │   ├── landuse/
    │   └── vegetation/
    ├── validation/               # Core validation layer
    └── packaging/                # Simulation/export packaging
```

## Core pipeline

```text
Raw GIS / Raster / AI Inputs
            │
            ▼
       Ingestion
            │
            ▼
      Normalization
            │
      ┌─────┴─────┐
      ▼           ▼
  Geometry      Terrain
      │           │
      └─────┬─────┘
            ▼
   Feature Enrichment
            │
            ▼
       Validation
            │
            ▼
    Packaging / Export
            │
            ▼
 Simulation-ready assets
```

## Implemented module: Feature Enrichment & Validation

`geo-core/features_Enrichment_Engine` provides the current processing implementation.

### Building enrichment

The engine derives:

- Estimated building height.
- Usage classification.
- Level-of-detail (LOD) class.
- Footprint area and perimeter.
- Confidence score.

Height estimation prioritizes OSM attributes such as `building:levels` and `height`, then falls back to building-type defaults.

### Road enrichment

Road features are enriched with:

- Estimated width.
- Road type.
- Navigation weight.
- Length and speed-related attributes.
- Confidence score.

### Validation

The validation layer checks:

- CRS consistency.
- Geometry validity.
- Attribute completeness.
- Schema and value ranges.
- Terrain continuity.
- Confidence thresholds.
- Cross-attribute consistency.

See `geo-core/features_Enrichment_Engine/README.md` for detailed API and CLI usage.

## Quick start

```bash
git clone https://github.com/ashadvalip/geosim-studio.git
cd geosim-studio/geo-core/features_Enrichment_Engine
python -m pip install -r requirements.txt
```

Enrich features:

```bash
geosim-features enrich \
  -b data/clean/buildings_clean.geojson \
  -r data/clean/roads_clean.geojson \
  -d data/normalized/dem_utm.tif \
  -o data/features/
```

Validate outputs:

```bash
geosim-features validate \
  -d data/ \
  -o data/validated/validation_report.json
```

## Development principles

- **Modularity** — keep processing stages independently evolvable.
- **Data lineage** — separate raw, processed, normalized, and exported artifacts.
- **Simulation readiness** — enrich GIS features with downstream simulation attributes.
- **Validation first** — treat quality checks as a pipeline stage.
- **Extensibility** — expand AI modules without tightly coupling them to every component.

## Repository status

The repository is under active development. Some directories currently act as architectural placeholders while functionality is added incrementally.

## Suggested workflow

1. Add or ingest source data under `data/raw`.
2. Normalize coordinate systems and metadata.
3. Process geometry and terrain.
4. Enrich features with simulation attributes.
5. Validate generated outputs.
6. Package validated assets for downstream simulation or export.

## Contributing

When adding a module:

1. Keep processing logic scoped to one responsibility.
2. Document input and output contracts.
3. Add validation for generated artifacts.
4. Avoid committing large generated datasets unless required for reproducibility.
5. Update this README when the architecture changes materially.

## License

No license has been specified yet. Add one before distributing the project for reuse.
