import findspark

findspark.init()
from pyspark.sql.functions import from_json, col, expr
from exercises.utils.invoice_schema import schema
from exercises.utils.kafka_commons import read, create_spark_session


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


if __name__ == "__main__":
    # 1. Create a Spark Session
    spark = create_spark_session(app_name="File Streaming Demo")

    # 2. Read the stream from the Kafka Topic
    # Note: For **debugging purposes** you might want to temporarily change 'readStream' by 'read' so you can
    # use value_df.show() and show the content of the dataframe as it won't be a streaming application.
    kafka_df = read(spark, "invoices")
    # Have a look at the schema
    # kafka_df.printSchema()

    # 3. Extract the value field from the Kafka Record and convert it to a DataFrame with the proper Schema
    value_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("value"))
    # Have a look at the schema
    # value_df.printSchema()
    # value_df.show()  # Don't forget to change readStream() by read()

    # TODO: Transform value_df to flatten JSON files
    # 4. [TRANSFORM]
    transformed_df = transform(value_df)

    # 5. Write the results - Flattened Invoice Writer
    invoice_writer_query = transformed_df \
        .writeStream \
        .format("json") \
        .queryName("Flattened Invoice Writer") \
        .outputMode("append") \
        .option("path", "output") \
        .option("checkpointLocation", "chk-point-dir") \
        .trigger(processingTime="1 minute") \
        .start()

    invoice_writer_query.awaitTermination()

# Don't forget to check out the Spark UI at http://localhost:4040/jobs/
# Every time a new invoice is being produced in kafka, spark structured streaming will read it and flatten it.
# The output will appear at the 'output' folder, but you can also have a look at the Spark UI in your browser

# Don't forget to delete the chk-point-dir, kafka-logs and output directories once you're done.
