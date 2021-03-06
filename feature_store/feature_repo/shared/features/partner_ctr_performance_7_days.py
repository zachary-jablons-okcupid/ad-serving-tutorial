from tecton import sql_transformation, TemporalFeaturePackage, MaterializationConfig
from feature_repo.shared import entities as e, data_sources
from datetime import datetime


@sql_transformation(inputs=data_sources.ad_impressions_batch, has_context=True)
def partner_ctr_performance_transformer(context, ad_impressions_batch):
    return f"""
    SELECT
        partner_id,
        sum(clicked) / count(*) as partner_total_ctr,
        to_timestamp('{context.feature_data_end_time}') as timestamp
    FROM
        {ad_impressions_batch}
    GROUP BY
        partner_id
    """

partner_ctr_performance_7d = TemporalFeaturePackage(
    name="partner_ctr_performance:7d",
    description="[SQL Feature] The aggregate CTR of a partner website (clicks / total impressions) over the past 7 days",
    transformation=partner_ctr_performance_transformer,
    entities=[e.partner_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=False,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="7d"
    ),
    family='ad_serving',
    tags={'release': 'development', ':production': 'true'},
    owner="ravi@tecton.ai",
)

partner_ctr_performance_14d = TemporalFeaturePackage(
    name="partner_ctr_performance:14d",
    description="[SQL Feature] The aggregate CTR of a partner website (clicks / total impressions) over the past 14 days",
    transformation=partner_ctr_performance_transformer,
    entities=[e.partner_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=False,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="14d"
    ),
    family='ad_serving',
    tags={'release': 'development', ':production': 'true'},
    owner="ravi@tecton.ai",
)

partner_ctr_performance_30d = TemporalFeaturePackage(
    name="partner_ctr_performance:30d",
    description="[SQL Feature] The aggregate CTR of a partner website (clicks / total impressions) over the past 30 days",
    transformation=partner_ctr_performance_transformer,
    entities=[e.partner_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=False,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="30d"
    ),
    family='ad_serving',
    tags={'release': 'development', ':production': 'true'},
    owner="ravi@tecton.ai",
)

partner_ctr_performance_60d = TemporalFeaturePackage(
    name="partner_ctr_performance:60d",
    description="[SQL Feature] The aggregate CTR of a partner website (clicks / total impressions) over the past 60 days",
    transformation=partner_ctr_performance_transformer,
    entities=[e.partner_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=False,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="60d"
    ),
    family='ad_serving',
    tags={'release': 'development', ':production': 'true'},
    owner="zach@okcupid.com",
)

partner_ctr_performance_90d = TemporalFeaturePackage(
    name="partner_ctr_performance:90d",
    description="[SQL Feature] The aggregate CTR of a partner website (clicks / total impressions) over the past 90 days",
    transformation=partner_ctr_performance_transformer,
    entities=[e.partner_entity],
    materialization=MaterializationConfig(
        offline_enabled=True,
        online_enabled=False,
        feature_start_time=datetime(year=2020, month=6, day=20),
        serving_ttl="1d",
        schedule_interval="1d",
        data_lookback_period="90d"
    ),
    family='ad_serving',
    tags={'release': 'development', ':production': 'true'},
    owner="zach@okcupid.com",
)
