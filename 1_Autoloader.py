# Databricks notebook source
# MAGIC %md
# MAGIC # Incremental Data Loading Using Autoloader

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA NETFLIX_CATALOG.NET_SCHEMA;

# COMMAND ----------

checkpoint_location = "abfss://silver@netflixprojdl1.dfs.core.windows.net/checkpoint"

# COMMAND ----------

df = spark.readStream\
    .format("cloudFiles")\
    .option("cloudFiles.format","csv")\
    .option("cloudFiles.schemaLocation",checkpoint_location)\
    .load("abfss://raw@netflixprojdl1.dfs.core.windows.net")

# COMMAND ----------

display(df)

# COMMAND ----------

df.writeStream\
    .option("checkpointLocation", checkpoint_location)\
    .trigger(availableNow=True)\
    .start("abfss://bronze@netflixprojdl1.dfs.core.windows.net/netflix_titles")