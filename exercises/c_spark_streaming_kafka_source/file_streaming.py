import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from exercises.utils.invoice_schema import schema


def read(spark: SparkSession):
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "invoices") \
        .option("startingOffsets", "earliest") \
        .load()
    return df


def transform(input_df):
    explode_df = input_df.selectExpr("value.InvoiceNumber", "value.CreatedTime", "value.StoreID",
                                     "value.PosID", "value.CustomerType", "value.PaymentMethod", "value.DeliveryType",
                                     "value.DeliveryAddress.City",
                                     "value.DeliveryAddress.State", "value.DeliveryAddress.PinCode",
                                     "explode(value.InvoiceLineItems) as LineItem")

    flattened_df = explode_df \
        .withColumn("ItemCode", expr("LineItem.ItemCode")) \
        .withColumn("ItemDescription", expr("LineItem.ItemDescription")) \
        .withColumn("ItemPrice", expr("LineItem.ItemPrice")) \
        .withColumn("ItemQty", expr("LineItem.ItemQty")) \
        .withColumn("TotalValue", expr("LineItem.TotalValue")) \
        .drop("LineItem")

    return flattened_df


def sink(input_df):
    invoice_writer_query = input_df.writeStream \
        .format("json") \
        .queryName("Flattened Invoice Writer") \
        .outputMode("append") \
        .option("path", "output") \
        .option("checkpointLocation", "chk-point-dir") \
        .trigger(processingTime="1 minute") \
        .start()

    invoice_writer_query.awaitTermination()


if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("File Streaming Demo") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    # 1. [READ]
    kafka_df = read(spark)
    # Have a look at the schema
    # kafka_df.printSchema()

    # 1.1 Apply the schema to the kafka dataframe
    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))
    # Have a look at the schema
    # value_df.printSchema()

    # 2. [TRANSFORM]
    transformed_df = transform(value_df)

    # 3. [SINK]
    sink(transformed_df)

# Don't forget to check out the Spark UI at http://localhost:4040/jobs/
# Every time a new invoice is being produced in kafka, spark structured streaming will read it and flatten it.
# The output will appear at the 'output' folder, but you can also have a look at the Spark UI in your browser

# Don't forget to delete the chk-point-dir, kafka-logs and output directories once you're done.
