import findspark

findspark.init()
from pyspark.sql.functions import from_json, col, expr
from exercises.utils.invoice_schema import schema
from exercises.utils.kafka_commons import read, create_spark_session


def transform_flatten_reports(input_df):
    explode_df = input_df.selectExpr("value.InvoiceNumber", "value.CreatedTime", "value.StoreID",
                                     "value.PosID", "value.CustomerType", "value.PaymentMethod", "value.DeliveryType",
                                     "value.DeliveryAddress.City",
                                     "value.DeliveryAddress.State", "value.DeliveryAddress.PinCode",
                                     "explode(value.InvoiceLineItems) as LineItem")

    output_df = explode_df \
        .withColumn("ItemCode", expr("LineItem.ItemCode")) \
        .withColumn("ItemDescription", expr("LineItem.ItemDescription")) \
        .withColumn("ItemPrice", expr("LineItem.ItemPrice")) \
        .withColumn("ItemQty", expr("LineItem.ItemQty")) \
        .withColumn("TotalValue", expr("LineItem.TotalValue")) \
        .drop("LineItem")

    return output_df


def get_notification_df_transformed(input_df):
    notification_df = input_df.select("value.InvoiceNumber", "value.CustomerCardNo", "value.TotalAmount") \
        .withColumn("EarnedLoyaltyPoints", expr("TotalAmount * 0.2"))

    output_df = notification_df.selectExpr("InvoiceNumber as key", "to_json(struct(*)) as value")
    return output_df


if __name__ == "__main__":
    # --- START COMMON FOR BOTH REQUIREMENTS ---

    # 1. Create a Spark Session
    spark = create_spark_session(app_name="Multi Query Demo")

    # 2. Read the stream from the Kafka Topic
    # Note: For **debugging purposes** you might want to temporarily change 'readStream' by 'read' so you can
    # use value_df.show() and show the content of the dataframe as it won't be a streaming application.
    kafka_df = read(spark, "invoices")
    # Have a look at the schema
    # kafka_df.printSchema()

    # 3. Extract the value field from the Kafka Record and convert it to a DataFrame with the proper Schema
    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))

    # --- END COMMON FOR BOTH REQUIREMENTS ---

    # TODO: 4.A - Notification requirement
    kafka_target_df = get_notification_df_transformed(value_df)

    # TODO: 4.A.1 - Notification Writer
    notification_writer_query = kafka_target_df \
        .writeStream \
        .queryName("Notification Writer") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "notifications") \
        .outputMode("append") \
        .option("checkpointLocation", "chk-point-dir/notify") \
        .start()

    # TODO: 4.B - Flattened reports requirement
    flattened_df = transform_flatten_reports(value_df)

    # TODO: 4.B.1 - Flattened Invoice Writer
    invoice_writer_query = flattened_df.writeStream \
        .format("json") \
        .queryName("Flattened Invoice Writer") \
        .outputMode("append") \
        .option("path", "output") \
        .option("checkpointLocation", "chk-point-dir/flatten") \
        .start()

    # ¡IMPORTANT!: Each query should have a **unique** checkpointLocation !!!
    # 5. Wait for any of the queries to terminate
    spark.streams.awaitAnyTermination()

# Don't forget to check out the Spark UI at http://localhost:4040/jobs/
# Every time a new invoice is being produced in kafka, spark structured streaming will read it and flatten it.
# The output will appear at the 'output' folder, but you can also have a look at the Spark UI in your browser

# Don't forget to delete the chk-point-dir, kafka-logs and output directories once you're done.
