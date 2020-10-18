from pyspark.sql import SparkSession


def spark_session():
    spark = SparkSession.builder.master("local[*]").appName("etl").getOrCreate()
    return spark
