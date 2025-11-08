# ESRI Shapefile to Zone Catcher GPX Converter

A Python utility that converts ESRI shapefiles to GPX format with zones/tracks, optimized for use with zone catcher applications.

## Features

- **Automatic Coordinate Reprojection**: Converts shapefile data to WGS84 (EPSG:4326) for proper GPS coordinates
- **Smart Point Simplification**: Reduces zones to a maximum of 200 points while preserving shape integrity using the Douglas-Peucker algorithm
- **Rich Metadata**: Includes shapefile attributes (name, owner, manager, type, county, acres, access, hunting status) in GPX track names and descriptions
- **Flexible Output Options**: 
  - Creates individual files with 100 zones each
  - Includes `combine_zones.py` script to merge files into larger groups (up to 1000 zones per file)
- **Sequential Zone Numbering**: Four-digit zero-padded zone numbers (e.g., Zone 0001, Zone 0002) for proper file sorting
- **Automated Environment Setup**: Shell script handles virtual environment creation and dependency installation

## Requirements

- Python 3.x
- geopandas
- gpxpy
- shapely (included with geopandas)

## Installation & Usage

### Quick Start

Simply run the provided shell script:

```bash
./run.sh
```

The script will automatically:
1. Create a virtual environment (`.venv`) if it doesn't exist
2. Install required dependencies from `python-requirements.txt`
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

# Run the main conversion script
python main.py

# Optionally combine zone files (groups of 1000)
python combine_zones.py
```

## Scripts

### main.py

Converts ESRI shapefiles to GPX format with the following processing:
- Reads shapefile data from the configured directory
- Reprojects coordinates to WGS84 (latitude/longitude)
- Simplifies complex geometries to stay under 200 points per zone
- Enriches GPX tracks with metadata from shapefile attributes
- Outputs files containing 100 zones each

**Configuration:**
- `shapefile_path`: Path to input shapefile
- `output_dir`: Directory for GPX output files
- `zones_per_file`: Number of zones per output file (default: 100)
- `max_points_per_zone`: Maximum points per zone (default: 200)

### combine_zones.py

Merges individual zone files into larger combined files:
- Processes all zone files in groups
- Creates combined files with up to 1000 zones each
- Maintains zone numbering in output filenames
- Automatically handles remaining zones in the final file

## Data Source

The example GIS data used in this application comes from the Iowa Geodata Portal:
- **Source**: https://geodata.iowa.gov/datasets/
- **Dataset**: Public Lands Used for Conservation and Recreation in Iowa

## Configuration

The `main.py` script is currently configured with:
- **Input Directory**: `/Users/mark/Downloads/Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa/`
- **Input File**: `Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa.shp`
- **Output Directory**: `/Users/mark/Downloads/iowa_zones/`

To use your own shapefile, modify the `shapefile_path` and `output_dir` variables in `main.py`.

## Output Format

### Individual Zone Files

Files are named: `zones_NNNN_XXXX-YYYY.gpx` where:
- `NNNN` = file number (zero-padded)
- `XXXX-YYYY` = zone number range in the file

### Combined Zone Files

Files are named: `combined_zones_XXXX-YYYY.gpx` where:
- `XXXX-YYYY` = zone number range (typically 1000 zones per file)

### GPX Track Structure

Each zone includes:
- **Track Name**: `Zone NNNN: Location Name` (e.g., "Zone 0042: Auburn Hills Park")
- **Track Description**: Pipe-separated attributes including:
  - Name
  - Owner
  - Manager
  - Type
  - County
  - Acres
  - Access
  - Public Hunting status
- **Coordinates**: Simplified to ≤200 points while preserving shape
- **Proper GPS coordinates**: WGS84 latitude/longitude values

## Project Structure

```
.
├── main.py                    # Main conversion script
├── combine_zones.py           # Zone file combining utility
├── run.sh                     # Automated setup and run script
├── python-requirements.txt    # Python dependencies
├── .gitignore                 # Git ignore rules
├── .venv/                     # Virtual environment (auto-created)
└── README.md                  # This file
```

## License

This project is provided as-is for converting ESRI shapefiles to GPX format.
