import pandas as pd


def calc_data_size(start_year, end_year, max_lat, min_lat, max_lon, min_lon, t_res, s_res):
    lat_size = (max_lat - min_lat) / s_res
    lon_size = (max_lon - min_lon) / s_res
    if t_res == "hour":
        time_size = (end_year - start_year) * 365 * 24
    elif t_res == "day":
        time_size = (end_year - start_year) * 365
    elif t_res == "month":
        time_size = (end_year - start_year) * 12
    elif t_res == "year":
        time_size = end_year - start_year

    byte_size = lat_size * lon_size * time_size * 1.7
    gb_size = byte_size / 1024 / 1024 / 1024
    if s_res != 0.25 or t_res != "hour":
        gb_size = gb_size * 3  # coarse resolution has min, max, and mean aggregation
    return gb_size


def create_meta_record(row):
    new_meta_records = []
    all_temporal_resolutions = ["hour", "day", "month", "year"]
    all_spatial_resolutions = [0.25, 0.5, 1]
    t_res = row.temporal_resolution
    s_res = row.spatial_resolution
    for tr in all_temporal_resolutions[all_temporal_resolutions.index(t_res) :]:
        for sr in all_spatial_resolutions[all_spatial_resolutions.index(s_res) :]:
            new_meta_records.append(
                [
                    row.ui_id,
                    row.variable,
                    row.start_year,
                    row.end_year,
                    row.max_lat,
                    row.min_lat,
                    row.max_lon,
                    row.min_lon,
                    row.temporal_resolution,
                    row.spatial_resolution,
                    tr,
                    sr,
                ]
            )
    return new_meta_records


def create_metadata_from_ui(df_ui):
    meta_records = []
    for row in df_ui.itertuples():
        new_records = create_meta_record(row)
        meta_records += new_records

    df_meta = pd.DataFrame(
        meta_records,
        columns=[
            "ui_id",
            "variable",
            "start_year",
            "end_year",
            "max_lat",
            "min_lat",
            "max_lon",
            "min_lon",
            "ui_temporal_resolution",
            "ui_spatial_resolution",
            "actual_temporal_resolution",
            "actual_spatial_resolution",
        ],
    )
    return df_meta
