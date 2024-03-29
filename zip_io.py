import json
from zipfile import ZIP_DEFLATED, ZipFile

import geopandas as gpd
import shapely


def to_geojson_obj(geodataframe: gpd.geodataframe.GeoDataFrame):
    features = geodataframe.to_dict('records')

    def mapping_geojson(entry):
        geometry = entry.pop('geometry')
        new_entry = {"type": "Feature",
                     "properties": entry,
                     "geometry": shapely.geometry.mapping(geometry)}
        return new_entry
    features = list(map(mapping_geojson, features))
    geojson = {"type": "FeatureCollection",
               "features": features
               }
    return geojson


def to_geojson_zip(geodataframe: gpd.geodataframe.GeoDataFrame,
                   dest_path: str):
    if '.zip' != dest_path[-4:]:
        ValueError('dest_path should have ".zip" as suffix')
    dst_path_decompressed = dest_path.replace('.zip', '')
    geojson_ob = to_geojson_obj(geodataframe)

    with ZipFile(dest_path, 'w') as file_out:
        data = json.dumps(geojson_ob).encode('utf-8')
        file_out.writestr(dst_path_decompressed,
                          data,
                          compress_type=ZIP_DEFLATED)
    return dest_path
