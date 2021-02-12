from tecton import FeatureService, FeaturesConfig
from feature_repo.shared.features.ad_ground_truth_ctr_performance_7_days import ad_ground_truth_ctr_performance_7_days
from feature_repo.shared.features.ad_group_ctr_performance import ad_group_ctr_performance


ctr_prediction_service = FeatureService(
    name='ctr_prediction_service',
    description='A FeatureService used for supporting a CTR prediction model.',
    online_serving_enabled=True,
    features=[
        ad_ground_truth_ctr_performance_7_days,
        ad_group_ctr_performance,
    ],
    family='ad_serving',
    tags={'release': 'production'},
    owner="matt@tecton.ai",
)
