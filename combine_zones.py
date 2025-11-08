import gpxpy
import gpxpy.gpx
import os
import glob

# Input and output directories
input_dir = "/Users/mark/Downloads/iowa_zones"

# Find all zone files (excluding already combined files)
all_zone_files = sorted(glob.glob(os.path.join(input_dir, "zones_*.gpx")))

if not all_zone_files:
    print("No zone files found!")
    exit(1)

print(f"Found {len(all_zone_files)} zone files to process")

# Configuration
zones_per_combined_file = 1000
zones_per_input_file = 100  # Each input file has 100 zones
files_per_group = zones_per_combined_file // zones_per_input_file  # 10 files per group

# Process files in groups
total_combined_files = 0
for group_idx in range(0, len(all_zone_files), files_per_group):
    group_files = all_zone_files[group_idx:group_idx + files_per_group]
    
    # Create a new GPX file for this group
    combined_gpx = gpxpy.gpx.GPX()
    zones_in_group = 0
    first_zone = group_idx * zones_per_input_file + 1
    
    print(f"\nProcessing group {group_idx // files_per_group + 1}...")
    
    # Process each file in the group
    for zone_file in group_files:
        print(f"  Processing: {os.path.basename(zone_file)}")
        
        with open(zone_file, 'r') as f:
            gpx = gpxpy.parse(f)
        
        # Add all tracks from this file to the combined GPX
        for track in gpx.tracks:
            combined_gpx.tracks.append(track)
            zones_in_group += 1
    
    # Calculate zone range for filename
    last_zone = first_zone + zones_in_group - 1
    output_file = os.path.join(input_dir, f"combined_zones_{first_zone:04d}-{last_zone:04d}.gpx")
    
    # Save the combined GPX file
    with open(output_file, 'w') as f:
        f.write(combined_gpx.to_xml())
    
    print(f"  Created: {os.path.basename(output_file)} with {zones_in_group} zones")
    total_combined_files += 1

print(f"\n✓ Successfully created {total_combined_files} combined GPX files")
