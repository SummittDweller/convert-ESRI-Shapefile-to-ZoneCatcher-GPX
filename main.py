import geopandas as gpd
import gpxpy
import gpxpy.gpx
import os

# Load the shapefile
shapefile_path = "/Users/mark/Downloads/Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa/Public_Lands_Used_for_Conservation_and_Recreation_in_Iowa.shp"
gdf = gpd.read_file(shapefile_path)

# Reproject to WGS84 (EPSG:4326) for GPS coordinates
gdf = gdf.to_crs(epsg=4326)

# Configuration
max_points_per_zone = 200

def simplify_coords(coords, max_points):
    """Reduce number of points while preserving shape"""
    from shapely.geometry import LineString
    
    coords_list = list(coords)
    if len(coords_list) <= max_points:
        return coords_list
    
    # Create a LineString and simplify using Douglas-Peucker algorithm
    # Start with a small tolerance and increase until we get under the limit
    line = LineString(coords_list)
    tolerance = 0.00001  # Start with very small tolerance (in degrees)
    
    while len(coords_list) > max_points and tolerance < 0.1:
        simplified_line = line.simplify(tolerance, preserve_topology=True)
        coords_list = list(simplified_line.coords)
        tolerance *= 1.5  # Increase tolerance
    
    # If still too many points, use uniform sampling as fallback
    if len(coords_list) > max_points:
        step = len(coords_list) // max_points
        coords_list = [coords_list[i] for i in range(0, len(coords_list), step)][:max_points]
    
    return coords_list

# Output directory
output_dir = "/Users/mark/Downloads/iowa_zones"
os.makedirs(output_dir, exist_ok=True)

# Configuration
zones_per_file = 100
zone_counter = 1
file_counter = 1
gpx = gpxpy.gpx.GPX()

def save_gpx_file(gpx_obj, file_num, zone_start, zone_end):
    """Save a GPX file with the given zones"""
    output_file = os.path.join(output_dir, f"zones_{file_num:04d}_{zone_start:04d}-{zone_end:04d}.gpx")
    with open(output_file, "w") as f:
        f.write(gpx_obj.to_xml())
    print(f"Created {output_file} with {zone_end - zone_start + 1} zones")

zones_in_current_file = 0
file_start_zone = 1

for idx, row in gdf.iterrows():
    shape = row.geometry
    
    # Build description from available attributes
    desc_parts = []
    if 'NAME' in row and row['NAME']:
        desc_parts.append(f"Name: {row['NAME']}")
    if 'OWNER' in row and row['OWNER']:
        desc_parts.append(f"Owner: {row['OWNER']}")
    if 'MANAGER' in row and row['MANAGER']:
        desc_parts.append(f"Manager: {row['MANAGER']}")
    if 'TYPE' in row and row['TYPE']:
        desc_parts.append(f"Type: {row['TYPE']}")
    if 'COUNTY' in row and row['COUNTY']:
        desc_parts.append(f"County: {row['COUNTY']}")
    if 'ACRES' in row and row['ACRES']:
        desc_parts.append(f"Acres: {row['ACRES']}")
    if 'ACCESS' in row and row['ACCESS']:
        desc_parts.append(f"Access: {row['ACCESS']}")
    if 'PUB_HUNT' in row and row['PUB_HUNT']:
        desc_parts.append(f"Public Hunting: {row['PUB_HUNT']}")
    
    description = " | ".join(desc_parts) if desc_parts else None
    
    # For polygons: extract exterior coordinates as a GPX track (zone)
    if shape.type == "Polygon":
        track_name = f"Zone {zone_counter}"
        if 'NAME' in row and row['NAME']:
            track_name = f"Zone {zone_counter}: {row['NAME']}"
        
        track = gpxpy.gpx.GPXTrack(name=track_name)
        if description:
            track.description = description
        segment = gpxpy.gpx.GPXTrackSegment()
        
        # Simplify coordinates to stay under max_points_per_zone
        simplified_coords = simplify_coords(shape.exterior.coords, max_points_per_zone)
        for lon, lat in simplified_coords:
            point = gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon)
            segment.points.append(point)
        track.segments.append(segment)
        gpx.tracks.append(track)
        zones_in_current_file += 1
        zone_counter += 1
        
        # Save file if we've reached the limit
        if zones_in_current_file >= zones_per_file:
            save_gpx_file(gpx, file_counter, file_start_zone, zone_counter - 1)
            gpx = gpxpy.gpx.GPX()
            file_counter += 1
            file_start_zone = zone_counter
            zones_in_current_file = 0
        
    # For multipolygons: create a separate track for each part
    elif shape.type == "MultiPolygon":
        for poly_idx, poly in enumerate(shape.geoms):
            track_name = f"Zone {zone_counter}"
            if 'NAME' in row and row['NAME']:
                track_name = f"Zone {zone_counter}: {row['NAME']}"
                if len(shape.geoms) > 1:
                    track_name += f" (Part {poly_idx + 1})"
            
            track = gpxpy.gpx.GPXTrack(name=track_name)
            if description:
                track.description = description
            segment = gpxpy.gpx.GPXTrackSegment()
            
            # Simplify coordinates to stay under max_points_per_zone
            simplified_coords = simplify_coords(poly.exterior.coords, max_points_per_zone)
            for lon, lat in simplified_coords:
                point = gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon)
                segment.points.append(point)
            track.segments.append(segment)
            gpx.tracks.append(track)
            zones_in_current_file += 1
            zone_counter += 1
            
            # Save file if we've reached the limit
            if zones_in_current_file >= zones_per_file:
                save_gpx_file(gpx, file_counter, file_start_zone, zone_counter - 1)
                gpx = gpxpy.gpx.GPX()
                file_counter += 1
                file_start_zone = zone_counter
                zones_in_current_file = 0

# Save any remaining zones
if zones_in_current_file > 0:
    save_gpx_file(gpx, file_counter, file_start_zone, zone_counter - 1)

print(f"\nSuccessfully created {file_counter} GPX files with {zone_counter - 1} total zones in {output_dir}")