# Databricks notebook source
var = dbutils.jobs.taskValues.get(taskKey="weedaylookup",key="weekoutput")

# COMMAND ----------

print(var)