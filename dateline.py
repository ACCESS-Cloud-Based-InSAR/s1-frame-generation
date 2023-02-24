import geopandas as gpd
import pandas as pd


def dateline_frame_fix(df_frames: gpd.GeoDataFrame, dateline_buffer: int = 8) -> gpd.GeoDataFrame:
    df_dateline = df_frames.cx[:-180 + dateline_buffer, :]

    multipolygon_index = df_dateline.geometry.map(lambda geo: (geo.geom_type != 'Polygon'))
    df_dateline_multi = df_dateline[multipolygon_index].copy()

    df_dateline_l = df_dateline_multi.copy()
    df_dateline_r = df_dateline_multi.copy()

    # The buffer ensures there is some overlap for merging by frame id
    geo_l = df_dateline_multi.translate(xoff=-360).buffer(1e-7)
    df_dateline_l.geometry = df_dateline_multi.geometry.union(geo_l)
    df_dateline_l_f = df_dateline_l.dissolve(by='frame_id', aggfunc='first').explode(index_parts=False)
    # only want the areas that are at the left hemisphere dateline
    df_dateline_l_f = df_dateline_l_f.cx[-180 - 80:-180 + dateline_buffer, :].reset_index(drop=False)

    geo_r = df_dateline_multi.translate(xoff=360).buffer(1e-7)
    df_dateline_r.geometry = df_dateline_multi.geometry.union(geo_r)
    df_dateline_r_f = df_dateline_r.dissolve(by='frame_id', aggfunc='first').explode(index_parts=False)
    # only want the areas that are at the right hemisphere dateline
    df_dateline_r_f = df_dateline_r_f.cx[180 - dateline_buffer: 180 + 80, :].reset_index(drop=False)

    frame_ids_l = df_dateline_l_f.frame_id.tolist()
    frame_ids_r = df_dateline_r_f.frame_id.tolist()
    frame_ids_dateline = list(set(frame_ids_l + frame_ids_r))

    dateline_ind = df_frames.frame_id.isin(frame_ids_dateline)
    df_dateline_removed = df_frames[~dateline_ind].copy()
    dfs = [df_dateline_removed, df_dateline_r_f, df_dateline_l_f]
    df_frames_final = pd.concat(dfs, axis=0).reset_index(drop=True)
    return df_frames_final
