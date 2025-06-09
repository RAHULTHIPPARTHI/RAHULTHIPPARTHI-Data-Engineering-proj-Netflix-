# Databricks notebook source
# MAGIC %md
# MAGIC ### DLT Notebook - Gold Layer

# COMMAND ----------

looktables_rules = {
    "rule1": "show_id is NOT NULL"
}

# COMMAND ----------

@dlt.table(
    name = "gold_netflixdirectors"
)
@dlt.expect_all_or_drop(looktables_rules)
def myfunc():
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdl1.dfs.core.windows.net/netflix_directors")
    return df


# COMMAND ----------

@dlt.table(
    name = "gold_netflixcast"
)
@dlt.expect_all_or_drop(looktables_rules)
def myfunc():
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdl1.dfs.core.windows.net/netflix_cast")
    return df

# COMMAND ----------

@dlt.table(
    name = "gold_netflixcoutries"
)
@dlt.expect_all_or_drop(looktables_rules)
def myfunc():
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdl1.dfs.core.windows.net/netflix_countries")
    return df

# COMMAND ----------

@dlt.table(
    name = "gold_netflixcategory"
)
@dlt.expect_or_drop("rule1", "show_id is NOT NULL")
def myfunc():
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdl1.dfs.core.windows.net/netflix_category")
    return df

# COMMAND ----------

@dlt.table

def gold_stg_netflixtitles():
    
    df = spark.readStream.format("delta").load("abfss://silver@netflixprojdl1.dfs.core.windows.net/netflix_titles")
    return df

# COMMAND ----------

from pyspark.sql.functions import lit

# COMMAND ----------

@dlt.table

def gold_trns_netflixtitles():
    df = spark.readStream.table("LIVE.gold_stg_netflixtitles")
    df = df.withColumn("newflag",lit(1))
    return df

# COMMAND ----------

masterdata_rules = {
    "rule1": "newflag is NOT NULL",
    "rule2": "show_id is NOT NULL"     
 }

# COMMAND ----------

@dlt.table

@dlt.expect_all_or_drop(masterdata_rules)
def gold_netflixtitles():

    df = spark.readStream.table("LIVE.gold_trns_netflixtitles")
    
    return df