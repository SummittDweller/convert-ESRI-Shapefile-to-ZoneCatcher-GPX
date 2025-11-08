# ESRI Shapefile to Zone Catcher GPX Converter

A Python utility that converts ESRI shapefiles to GPX format with zones/tracks, suitable for use with zone catcher applications.

## Features

- Converts polygon and multipolygon geometries from shapefiles to GPX tracks
- Each zone is numbered sequentially in the output GPX file
- Handles both simple polygons and complex multipolygon features
- Automated virtual environment setup and dependency management

## Requirements

- Python 3.x
- geopandas
- gpxpy

## Installation & Usage

### Quick Start

Simply run the provided shell script:

```bash
./run.sh
```

The script will automatically:
1. Create a virtual environment if it doesn't exist
2. Install required dependencies
3. Run the conversion script

### Manual Setup

If you prefer to set up manually:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r python-requirements.txt

# Run the script
python main.py
```

## Data Source

The example GIS data used in this application comes from the Iowa Geodata Portal:
- **Source**: https://geodata.iowa.gov/datasets/
- **Dataset**: Public Lands Used for Conservation and Recreation in Iowa

## Configuration

The script is currently configured to:
- **Input**: `/Users/mark/Downloads/Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa/Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa.shp`
- **Output**: `/Users/mark/Downloads/iowa_zones.gpx`

To use your own shapefile, modify the `shapefile_path` variable in `main.py`.

## Output Format

The converter creates GPX files with:
- Each polygon/multipolygon as a separate track
- Sequential zone numbering (Zone 1, Zone 2, etc.)
- Proper latitude/longitude coordinates from the shapefile geometries

## License

This project is provided as-is for converting ESRI shapefiles to GPX format.
