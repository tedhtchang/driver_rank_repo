from datetime import timedelta

from feast import FileSource, Entity, Feature, FeatureView, ValueType

driver = Entity(name="driver_id", join_key="driver_id", value_type=ValueType.INT64,)

driver_stats_source = FileSource(
    path="driver_rank_repo/data/driver_stats.parquet",
    # If you like your driver stats file in object store:
    # path="s3://driver_rank_repo/data/driver_stats.parquet"
    # s3_endpoint_override="https://s3.us-south.cloud-object-storage.appdomain.cloud"
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created",
)

driver_stats_fv = FeatureView(
    name="driver_hourly_stats",
    entities=["driver_id"],
    ttl=timedelta(weeks=52),
    features=[
        Feature(name="conv_rate", dtype=ValueType.FLOAT),
        Feature(name="acc_rate", dtype=ValueType.FLOAT),
        Feature(name="avg_daily_trips", dtype=ValueType.INT64),
    ],
    batch_source=driver_stats_source,
    tags={"team": "driver_performance"},
)
