from datetime import datetime
from tecton import TemporalAggregateFeaturePackage, FeatureAggregation, sql_transformation, MaterializationConfig
from feature_repo.shared import data_sources, entities

@sql_transformation(inputs=data_sources.events_vds)
def ad_group_ctr_performance_transformer(input_df):
    return f"""
        select
            ad_id,
            clicked,
            1 as impression,
            timestamp
        from
            {input_df}
        """


ad_group_ctr_performance = TemporalAggregateFeaturePackage(
    name="ad_group_ctr_performance",
    description="[Batch Feature] The aggregate CTR of an ad_group across all impressions (clicks / total impressions)",
    entities=[entities.ad_group_entity.with_join_keys('ad_id')],
    transformation=ad_group_ctr_performance_transformer,
    aggregation_slide_period="1h",
    aggregations=[
        FeatureAggregation(column="impression", function="count", time_windows=["1h", "12h", "24h","72h","168h"]),
        FeatureAggregation(column="clicked", function="sum", time_windows=["1h", "12h", "24h","72h","168h"])
        ],
    materialization=MaterializationConfig(
        online_enabled=True,
        offline_enabled=True,
        feature_start_time=datetime(2020, 6, 1),
    ),
    family='ad_serving',
    tags={'release': 'development'},
    owner="mike@tecton.ai"
)
