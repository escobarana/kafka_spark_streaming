import findspark

findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from exercises.utils.catalog import load_frame_from_catalog


def read(spark: SparkSession):
    return load_frame_from_catalog(spark=spark, format="json", dataset_name="invoices_json")


# TODO: Transform the input JSON files to flatten the nested fields and write the final JSON
#  files in the output folder
def transform(input_df):
    explode_df = input_df.selectExpr("InvoiceNumber", "CreatedTime", "StoreID", "PosID",
                                     "CustomerType", "PaymentMethod", "DeliveryType", "DeliveryAddress.City",
                                     "DeliveryAddress.State",
                                     "DeliveryAddress.PinCode", "explode(InvoiceLineItems) as LineItem")

    flattened_df = explode_df \
        .withColumn("ItemCode", expr("LineItem.ItemCode")) \
        .withColumn("ItemDescription", expr("LineItem.ItemDescription")) \
        .withColumn("ItemPrice", expr("LineItem.ItemPrice")) \
        .withColumn("ItemQty", expr("LineItem.ItemQty")) \
        .withColumn("TotalValue", expr("LineItem.TotalValue")) \
        .drop("LineItem")

    return flattened_df


def sink(transformed_df):
    invoice_writer_query = transformed_df.writeStream \
        .format("json") \
        .queryName("Flattened Invoice Writer") \
        .outputMode("append") \
        .option("path", "output") \
        .option("checkpointLocation", "chk-point-dir") \
        .trigger(processingTime="1 minute") \
        .start()

    invoice_writer_query.awaitTermination()


def main():
    spark = SparkSession \
        .builder \
        .appName("File Streaming") \
        .master("local[3]") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .config("spark.sql.streaming.schemaInference", "true") \
        .getOrCreate()

    # 1. [READ] from the input folder the JSON files
    input_df = read(spark)
    # input_df.printSchema()

    # 2. [TRANSFORM] get flattened dataframe
    transformed_df = transform(input_df)

    # 3. [SINK] to output folder
    sink(transformed_df)


if __name__ == "__main__":
    main()
