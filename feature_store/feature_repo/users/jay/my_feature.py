# from tecton import TemporalFeaturePackage, pyspark_transformation, MaterializationConfig
# from feature_repo.shared import data_sources, entities
# from datetime import datetime

# @pyspark_transformation(inputs=data_sources.ad_impressions_batch)
# def ad_impression_count_monthly_transformer(input_view):
#     import pyspark.sql.functions as F
#     truncated_date_view = input_view.withColumn('timestamp', F.date_trunc('day', F.col('timestamp')))
#     return truncated_date_view.groupBy('ad_id', 'timestamp').agg(F.count(F.lit(1)).alias("ad_impression_count"))
#
# ad_impression_count_monthly = TemporalFeaturePackage(
#     name="ad_impression_count_monthly",
#     description="[Pyspark Feature] The total number of impressions that an ad has generated over the past month",
#     transformation=ad_impression_count_monthly_transformer,
#     entities=[entities.ad_entity],
#     materialization=MaterializationConfig(
#         online_enabled=False,
#         offline_enabled=False,
#         feature_start_time=datetime(2020, 6, 1),
#         schedule_interval='1day',
#         serving_ttl='1day'
#     )
#     family='ad_serving',
#     tags={'release': 'development'}
# )
