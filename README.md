# Building solid streaming data pipelines with Apache Kafka and Spark Structured Streaming

📚 A course brought to you by the [Data Minded Academy].

## Context

These are the exercises used in the course *Data Pipeline Part 2 at DSTI*.  
The course has been developed by instructors at Data Minded. The
exercises are meant to be completed in the lexicographical order determined by
name of their parent folders. That is, exercises inside the folder `b_foo`
should be completed before those in `c_bar`, but both should come after those
of `a_foo_bar`.

## Course objectives

- Introduce good data engineering practices.
- Illustrate modular and easily testable data transformation pipelines using
  PySpark.
- Illustrate PySpark concepts, like lazy evaluation, caching & partitioning.
  Not limited to these three though.

## Intended audience

- People working with (Py)Spark Structured Streaming and Apache Kafka or soon to be working with it.
- Familiar with Python functions, variables and the container data types of
  `list`, `tuple`, `dict`, and `set`.

## Approach

Lecturer first sets the foundations right for Python development and
gradually builds up to Apache Kafka and Spark Structured Streaming data pipelines.

There is a high degree of participation expected from the students: they
will need to write code themselves and reason on topics, so that they can
better retain the knowledge.

Note: this course is not about writing the best streaming pipelines possible. There are
many ways to skin a cat, in this course we show one (or sometimes a few), which
should be suitable for the level of the participants.

## Getting started with Spark Structured Streaming

## Spark Set Up on Windows
Follow these instructions to set up JDK 11, Hadoop WinUtils, Spark binaries and environment 
variables on Windows/x64 System: [Click Here](https://app.tango.us/app/workflow/Setting-up-JDK--Hadoop-WinUtils--Spark-binaries-and-environment-variables-on-Windows-x64-System-ce23bd438117424c87009b2ac1fc82bd) 


## Getting started with Spark Structured Streaming 

Spark Structured Streaming practice exercises

### Prerequisites
Open a new terminal and make sure you're in the `kafka_spark_streaming` directory. Then, run:

```bash
pip install -r requirements.txt
```

This will install any dependencies you might need to run this project in your virtual environment.

You will also need to download [nmap](https://nmap.org/download.html) for Windows.

To use `nmap`, start a new terminal and type `ncat -lk 9999` to start the listener. 
You can send text to port 9999 just by typing in the same terminal.


## Exercises

### Count the number of words in real-time
Check out [word_count.py](exercises/a_spark_streaming_socket_source/word_count.py) and implement the pure
python function `transform`.
You will start a new terminal with an `ncat` listener as explained before. 
Count how many times each word appears in real-time.

### Transform nested JSON files to flattened JSON files
Check out [file_streaming.py](exercises/b_spark_streaming_file_source/file_streaming.py) and implement the pure
python function `transform`.
Have a look at the JSON files in `resources > invoices-json`.
You can see that there are nested fields. We want to flatten those files so that there are no 
nested fields in the final JSON files.

### BONUS 1: Repeat the previous exercise but using the parquet files format instead of JSON. Adapt anything you need in your code
### BONUS 2: Try to use Spark Structured Streaming on the exercises from the first day


## Getting started with Apache Kafka

Apache Kafka practice exercises mixed with Spark Structured Streaming

## Apache Kafka Set Up on Windows
Follow these instructions to set up Apache Kafka binaries and environment 
variables on Windows/x64 System: [Click Here](https://app.tango.us/app/workflow/Download-and-Configure-Apache-Kafka-on-Windows-x64-System-474eb2506acd494ebd5c94686ea610c2) 

**IMPORTANT: Add Spark SQL Kafka package to your Spark Defaults** `C:\spark3\conf` folder, `spark-defaults.conf` file:

spark.jars.packages                org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4


### Prerequisites (if not already done)
Open a new terminal and make sure you're in the `kafka_spark_streaming` directory. Then, run:

```bash
pip install -r requirements.txt
```

This will install any dependencies you might need to run this project in your virtual environment.


## Exercises

### Transform nested JSON files to flattened JSON files
Check out [a_file_streaming.py](exercises/c_spark_streaming_kafka_source/a_file_streaming.py) and implement the pure
python function `transform`.

Read the invoices, that are being sent through kafka in real-time, with Spark Structured Streaming and flatten the nested JSONs


### Log notifications back to Kafka cluster
Check out [b_sink.py](exercises/c_spark_streaming_kafka_source/b_sink.py) and implement the pure
python function `transform`.

We want a new topic to log notifications. Each notification message produced to that topic will have the following JSON schema:
- InvoiceNumber
- value
  - CustomerCardNo 
  - CustomerCardNo 
  - TotalAmount 
  - TotalAmount
  - EarnedLoyaltyPoints
  - TotalAmount * 0.2

The  column named `EarnedLoyaltyPoints` is a new column that you have to create, it will have the value of the result of `TotalAmount * 0.2`

### Multi query
Check out [c_multi_query.py](exercises/c_spark_streaming_kafka_source/c_multi_query.py) and implement the pure
python function `transform`.


## Extra information:
In the `resources` folder you will find all the input data (JSON, CSV, parquet files) you need to do the exercises.

The `utils` folder contains the `catalog.py` file which was also used during the first class with the Spark DataFrame API
but this time adapted for Spark Structured Streaming. `invoice_schema.py` is the invoice schema of the messages written
to the kafka topic. Under `kafka_scripts` you will find all the necessary scripts to start kafka (zookeeper, server, 
create topics, start producer, start consumer).

[Data Minded Academy]: https://www.dataminded.academy/
