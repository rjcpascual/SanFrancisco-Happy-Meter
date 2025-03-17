import pandas as pd
from pyproj import Transformer

# Transformer for WGS84 (lat/long) to UTM Zone 10N
# Adjust EPSG code if you're in a different UTM zone.
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32610", always_xy=True)

def latlon_to_utm(lon, lat):
    easting, northing = transformer.transform(lon, lat)
    return easting, northing

#list of (input_csv, output_csv) pairs
file_pairs = [
    ("parkLatLongName.csv", "parksUTMconversion.csv"),
    ("schoolLatLongName.csv", "schoolsUTMconversion.csv"),
    ("waterLatLongName.csv", "waterUTMconversion.csv")
]

for input_file, output_file in file_pairs:
    df = pd.read_csv(f"./processed datasets/{input_file}")
    df["UTM_Easting"], df["UTM_Northing"] = zip(*df.apply(
        lambda row: latlon_to_utm(row["longitude"], row["latitude"]), axis=1
    ))
    df.to_csv(f"./converted datasets/{output_file}", index=False)
