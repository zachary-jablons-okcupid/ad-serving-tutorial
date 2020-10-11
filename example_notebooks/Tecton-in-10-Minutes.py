# Databricks notebook source
# MAGIC %md # 📚 Tecton in 10 minutes
# MAGIC 
# MAGIC In this quickstart, you will:
# MAGIC 
# MAGIC 1. Generate training data using a FeatureService
# MAGIC 2. Serve features at prediction through a productionized API
# MAGIC 3. Explore features from the Feature Library

# COMMAND ----------

# MAGIC %md ### 0. Attach the notebook to the cluster and run all commands in the notebook
# MAGIC 1. In the notebook menu bar, select <img src="http://docs.databricks.com/_static/images/notebooks/detached.png"/></a> > `notebook-cluster`.
# MAGIC 2. When the cluster changes from <img src="http://docs.databricks.com/_static/images/clusters/cluster-starting.png"/></a> to <img src="http://docs.databricks.com/_static/images/clusters/cluster-running.png"/></a>, click **<img src="http://docs.databricks.com/_static/images/notebooks/run-all.png"/></a> Run All**.

# COMMAND ----------

# Import Tecton
import tecton
tecton.version.summary()

# COMMAND ----------

# MAGIC %md ### 1. Generate training data using a FeatureService
# MAGIC 
# MAGIC 🔑 **Concept: FeatureServices**
# MAGIC 
# MAGIC A FeatureService is a set of features that have been grouped together for use in training and serving. Typically, each deployed model will have one FeatureService to serve features. One Tecton FeatureService can be used  for both generating training data sets and for serving feature values for batch and real-time predictions.
# MAGIC 
# MAGIC These commands do two things:
# MAGIC 1. *Load a set of sample events* - The index of a training set, the timestamps for prediction, and the labels. This would be created by your data scientists.
# MAGIC 2. *Pass those events to a FeatureService* - Tecton uses the index and the timestamp of the events to calculate the values for all features in the training data
# MAGIC 
# MAGIC Note: These queries may take a few minutes to run.

# COMMAND ----------

# Load a set of sample events from your Tecton environment:
events = tecton.get_virtual_data_source('sample_events_for_models')
events.preview()

# COMMAND ----------

# Generate training data using a Tecton FeatureService: 
fs = tecton.get_feature_service('ctr_prediction_service')
training_data = fs.get_feature_dataframe(events.dataframe())
display(training_data.to_spark())

# COMMAND ----------

# MAGIC %md ❗❗❗ If you received an error in running these commands, you may need to update your Feature Store. That can be done by [following these instructions.](https://staging-docs.tecton.ai/trial/tutorial/environment-set-up.html) 

# COMMAND ----------

# MAGIC %md You can learn more about the FeatureService by reviewing the Web UI - for example, the features in the FeatureService and operational metrics associated with the API endpoint.
# MAGIC 
# MAGIC 
# MAGIC 🛑 **Three things to notice:** 
# MAGIC * Tecton builds your training set with time management in mind. That is, the system automatically makes sure that all feature values are accurate with respect to the prediction timestamp and there is no target leakage. 
# MAGIC * This training set is created from a combination of features using batch and streaming data - traditionally a difficult undertaking. You can learn more about the different features in this FeatureService in the Tecton Web UI. 
# MAGIC * Training set generation was done with two lines of code. It is quick to begin building your models, defining your model metrics, and iterating on different algorithms when it is easy to access the features.

# COMMAND ----------

# MAGIC %md ### 2. Serve features at prediction through a productionized API
# MAGIC 
# MAGIC Let's assume the model created from the above training set was put into production. To use that model to make a prediction, it needs to be fed up-to-date data at the `ad_id` and `user_uuid` level (the index of the training set). If you make a request call to Tecton with the `ad_id` and `user_uuid` values you need data for, Tecton will return the feature values in a JSON object.

# COMMAND ----------

from pprint import pprint

keys = {
  'user_uuid': '0455fce0-dd62-53cb-9d37-035a905964f8',
  'ad_id': '5243'
}

response = fs.get_feature_vector(keys).to_dict()
pprint(response)

# COMMAND ----------

# MAGIC %md The dictionary above is a FeatureVector - all of the feature values are valid as of this exact moment in time. To see a different FeatureVector, you can choose other `ad_id` and `user_uuid` pairs by copying values from the training set above.
# MAGIC 
# MAGIC 🛑 **Three things to notice:** 
# MAGIC * These feature values are different from the values in the training set. The values in training set are associated with the stated timestamp; the FeatureVector values are true as of this point in time.
# MAGIC * These prediction values are accessible as soon as a data scientist defines a FeatureService. The infrastructure for serving in production is managed for you.
# MAGIC * These values are served with production SLAs in mind - Tecton offers a p99 request latency of 100ms. 

# COMMAND ----------

# MAGIC %md ### 3. Explore features from the Feature Library
# MAGIC 
# MAGIC 🔑 **Concept: Feature Library**
# MAGIC 
# MAGIC The Feature Library includes all of your organization's registered features. Once a feature is registered with Tecton, Tecton manages the orchestration, storage, and serving of that feature. You can review overviews of all of your features' properties by clicking on the Features button in the Tecton Web UI. You can also access all of your registered features in Notebooks using the Tecton SDK.
# MAGIC 
# MAGIC These commands do two things:
# MAGIC 1. Loads a individual feature from the FeatureService used in this tutorial and reviews the description of that feature
# MAGIC 2. Calls a preview of the feature to review a sample dataset

# COMMAND ----------

# Load the FeaturePackage ad_ground_truth_ctr_performance_7_days 
fp = tecton.get_feature_package('ad_ground_truth_ctr_performance_7_days')

fp.description

# COMMAND ----------

# View a preview of feature data
fp.preview()

# COMMAND ----------

# MAGIC %md
# MAGIC 🛑 **Three things to notice:** 
# MAGIC * Some feature logic may represent multiple features - for example, there are two features associated with ``'ad_ground_truth_ctr_performance_7_days'``. To account for this, Tecton names registered features as FeaturePackages.
# MAGIC * Using Tecton to register and manage your features allows for FeaturePackages to be reused and shared across your organization. 
# MAGIC * FeaturePackages have distinct names and be accessed via common methods. This allows for features to be referred to and used as objects of code.

# COMMAND ----------

# MAGIC %md ❗❗❗ When determining which existing features to use for your model, the Tecton Web UI can help answer important questions, including:
# MAGIC - Who created the feature, and when?
# MAGIC - What is the source data for this feature - is it from batch, streaming, or request-time data?
# MAGIC - What is the logic for the transformation?
# MAGIC - What are some summary statistics associated with this feature?
# MAGIC 
# MAGIC Once you've completed this quickstart, we recommend you review the Web UI to get a sense of what information is available there.

# COMMAND ----------

# MAGIC %md ## Conclusion
# MAGIC 
# MAGIC In this walkthrough we:
# MAGIC 1. Covered key Tecton concepts, including FeatureServices, FeaturePackages, and the Feature Library
# MAGIC 1. Generated training data using a FeatureService
# MAGIC 2. Served features at prediction through a productionized API
# MAGIC 3. Explored features from the Feature Library
# MAGIC 
# MAGIC ## What's next?
# MAGIC * Log into the Tecton Web UI. If a helpful reference, the tutorial in the documentation has a section on navigation.
# MAGIC * Begin Taking the Next Step! That's the extended part of our tutorial - where you create features and add new services.
# MAGIC 
# MAGIC ### Tecton Documentation
# MAGIC - <a href="https://docs.tecton.ai" target="_blank">Tecton Docs</a>
# MAGIC - <a href="https://s3-us-west-2.amazonaws.com/tecton.ai.public/documentation/tecton-py/index.html" target="_blank">Tecton Python SDK Docs</a>
