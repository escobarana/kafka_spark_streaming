import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from exercises.utils.invoice_schema import schema

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Multi Query Demo") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .getOrCreate()

    kafka_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "invoices") \
        .option("startingOffsets", "earliest") \
        .load()

    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))

    notification_df = value_df.select("value.InvoiceNumber", "value.CustomerCardNo", "value.TotalAmount") \
        .withColumn("EarnedLoyaltyPoints", expr("TotalAmount * 0.2"))

    kafka_target_df = notification_df.selectExpr("InvoiceNumber as key", "to_json(struct(*)) as value")

    notification_writer_query = kafka_target_df \
        .writeStream \
        .queryName("Notification Writer") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "notifications") \
        .outputMode("append") \
        .option("checkpointLocation", "chk-point-dir/notify") \
        .start()

    explode_df = value_df.selectExpr("value.InvoiceNumber", "value.CreatedTime", "value.StoreID",
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

    invoice_writer_query = flattened_df.writeStream \
        .format("json") \
        .queryName("Flattened Invoice Writer") \
        .outputMode("append") \
        .option("path", "output") \
        .option("checkpointLocation", "chk-point-dir/flatten") \
        .start()

    spark.streams.awaitAnyTermination()

# Don't forget to check out the Spark UI at http://localhost:4040/jobs/
# Every time a new invoice is being produced in kafka, spark structured streaming will read it and flatten it.
# The output will appear at the 'output' folder, but you can also have a look at the Spark UI in your browser

# Don't forget to delete the chk-point-dir, kafka-logs and output directories once you're done.
