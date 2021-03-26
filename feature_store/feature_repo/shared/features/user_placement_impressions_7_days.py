from tecton import pyspark_transformation, TemporalFeaturePackage, MaterializationConfig
from feature_repo.shared import entities as e, data_sources
from datetime import datetime


@pyspark_transformation(inputs=data_sources.ad_impressions_batch, has_context=True)
def user_placement_impression_count_7_days_transformer(context, input_df):
    import pyspark.sql.functions as F

    user_placement_views = input_df.groupBy("user_uuid", "ad_display_placement").agg(F.count(F.col("*")).alias("user_placement_impressions_7_days"))
    user_placement_views = user_placement_views.withColumn("timestamp", F.to_timestamp(F.lit(context.feature_data_end_time)))
    return user_placement_views

user_placement_impression_count_7_days = TemporalFeaturePackage(
    name="user_placement_impression_count_7_days",
    description="[Pyspark Feature] The number of ads a user has been shown from a given ad display placement over the past 7 days",
    transformation=user_placement_impression_count_7_days_transformer,
    entities=[e.user_entity, e.placement_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=True,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="7d"
    ),
    family='ad_serving',
    tags={'release': 'production'},
    owner="kzhao@okcupid.com"
)
