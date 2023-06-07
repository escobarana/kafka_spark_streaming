import findspark

findspark.init()
from pyspark.sql.functions import from_json, col, expr
from exercises.utils.invoice_schema import schema
from exercises.utils.kafka_commons import read, create_spark_session


def get_notification_dataframe(input_df):
    return input_df.select("value.InvoiceNumber", "value.CustomerCardNo", "value.TotalAmount") \
        .withColumn("EarnedLoyaltyPoints", expr("TotalAmount * 0.2"))


def transform(input_df):
    # return notification_df.selectExpr("InvoiceNumber as key", "to_json(struct(*)) as value")
    return input_df.selectExpr("InvoiceNumber as key",
                               """to_json(named_struct(
                               'CustomerCardNo', CustomerCardNo,
                               'TotalAmount', TotalAmount,
                               'EarnedLoyaltyPoints', TotalAmount * 0.2)) as value""")


if __name__ == "__main__":
    # 1. Create a Spark Session
    spark = create_spark_session(app_name="File Streaming Demo")

    # 2. Read the stream from the Kafka Topic
    # Note: For **debugging purposes** you might want to temporarily change 'readStream' by 'read' so you can
    # use value_df.show() and show the content of the dataframe as it won't be a streaming application.
    kafka_df = read(spark, "invoices")

    # 3. Extract the value field from the Kafka Record and convert it to a DataFrame with the proper Schema
    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))
    # value_df.printSchema()
    # value_df.show()  # Don't forget to change readStream() by read()

    # TODO: Create a Notification DataFrame using the value_df and send it to Kafka
    # 4. [TRANSFORM]
    notification_df = get_notification_dataframe(input_df=value_df)
    # notification_df.show()  # Don't forget to change readStream() by read()

    # TODO: Transform notification_df to send key-value pair. Key is a string and value a JSON document
    # 5.
    kafka_target_df = transform(input_df=notification_df)

    # 6. Write to Kafka Topic the key-value notification record
    notification_writer_query = kafka_target_df \
        .writeStream \
        .queryName("Notification Writer") \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "notifications") \
        .outputMode("append") \
        .option("checkpointLocation", "chk-point-dir") \
        .start()

    notification_writer_query.awaitTermination()

# Don't forget to check out the Spark UI at http://localhost:4040/jobs/
# Every time a new invoice is being produced in kafka, spark structured streaming will read it and flatten it.
# The output will appear at the 'output' folder, but you can also have a look at the Spark UI in your browser

# Don't forget to delete the chk-point-dir, kafka-logs and output directories once you're done.
