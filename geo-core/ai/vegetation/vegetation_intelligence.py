
import numpy as np
import rasterio
from rasterio.transform import from_origin
import geopandas as gpd
from shapely.geometry import Polygon
from sklearn.cluster import KMeans


# Grid size
width, height = 256, 256

# Simulated terrain features
np.random.seed(42)
elevation = np.random.rand(height, width)     # normalized DEM
moisture = np.random.rand(height, width)      # soil moisture
slope = np.random.rand(height, width)         # slope

# Vegetation density formula
density = (
    0.5 * moisture +
    0.3 * (1 - slope) +
    0.2 * (1 - elevation)
)

# Normalize to 0–1
density = (density - density.min()) / (density.max() - density.min())
transform = from_origin(0, 0, 1, 1)

with rasterio.open(
    "data/ai/vegetation_density.tif",
    "w",
    driver="GTiff",
    height=height,
    width=width,
    count=1,
    dtype=density.dtype,
    crs="+proj=latlong",
    transform=transform
) as dst:
    dst.write(density, 1)
# Flatten density for clustering
X = density.reshape(-1, 1)

# Cluster into vegetation zones
kmeans = KMeans(n_clusters=3, random_state=0)
labels = kmeans.fit_predict(X)

zone_map = labels.reshape(height, width)


polygons = []

for zone in range(3):
    mask = zone_map == zone
    indices = np.argwhere(mask)

    if len(indices) == 0:
        continue

    min_y, min_x = indices.min(axis=0)
    max_y, max_x = indices.max(axis=0)

    poly = Polygon([
        (min_x, min_y),
        (max_x, min_y),
        (max_x, max_y),
        (min_x, max_y)
    ])

    polygons.append({
        "geometry": poly,
        "zone": int(zone)
    })

gdf = gpd.GeoDataFrame(polygons, crs="EPSG:4326")


gdf.to_file("data/ai/tree_zones.geojson", driver="GeoJSON")
