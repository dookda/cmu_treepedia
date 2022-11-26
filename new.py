import mercantile
import mapbox_vector_tile
import requests
import json

from vt2geojson.tools import vt_bytes_to_geojson
# define an empty geojson as output

output = {"type": "FeatureCollection", "features": []}
# vector tile endpoints -- change this in the API request to reference the correct endpoint

tile_coverage = 'mly1_public'

# tile layer depends which vector tile endpoints:
# 1. if map features or traffic signs, it will be "point" always
# 2. if looking for coverage, it will be "image" for points, "sequence" for lines, or "overview" for far zoom
tile_layer = "image"

# Mapillary access token -- user should provide their own
access_token = 'MLY|8045836652156959|8a007fa3a9d9107c96e2b2004a231a64'
# a bounding box in [east_lng,_south_lat,west_lng,north_lat] format

west, south, east, north = [28.796033233,
                            47.000293577, 28.892778241, 47.0432798382116]

# get the list of tiles with x and y coordinates which intersect our bounding box
# MUST be at zoom level 14 where the data is available, other zooms currently not supported
tiles = list(mercantile.tiles(west, south, east, north, 14))

# loop through list of tiles to get tile z/x/y to plug in to Mapillary endpoints and make request

for tile in tiles:
    tile_url = 'https://tiles.mapillary.com/maps/vtp/{}/2/{}/{}/{}?access_token={}'.format(
        tile_coverage, tile.z, tile.x, tile.y, access_token)
    response = requests.get(tile_url)
    data = vt_bytes_to_geojson(
        response.content, tile.x, tile.y, tile.z, layer=tile_layer)

    # push to output geojson object if yes
    for feature in data['features']:
        output['features'].append(feature)

# save a local geojson with the filtered data
with open('images.geojson', 'w') as f:
    json.dump(output, f)
