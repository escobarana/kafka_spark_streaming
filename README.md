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

### 1. Count the number of words in real-time
Check out [word_count.py](exercises/a_spark_streaming_socket_source/word_count.py) and implement the pure
python function `transform`.
You will start a new terminal with an `ncat` listener as explained before. 
Count how many times each word appears in real-time.

### 2. Transform nested JSON files to flattened JSON files
Check out [file_streaming.py](exercises/b_spark_streaming_file_source/file_streaming.py) and implement the pure
python function `transform`.
Have a look at the JSON files in `resources > invoices-json`.
You can see that there are nested fields. We want to flatten those files so that there are no 
nested fields in the final JSON files.

### BONUS: Try to use Spark Structured Streaming on the exercises from the first day


## Getting started with Apache Kafka

Apache Kafka practice exercises mixed with Spark Structured Streaming

## Apache Kafka Set Up on Windows
Follow these instructions to set up Apache Kafka binaries and environment 
variables on Windows/x64 System: [Click Here](https://app.tango.us/app/workflow/Download-and-Configure-Apache-Kafka-on-Windows-x64-System-474eb2506acd494ebd5c94686ea610c2) 


### Prerequisites (if not already done)
Open a new terminal and make sure you're in the `kafka_spark_streaming` directory. Then, run:

```bash
pip install -r requirements.txt
```

This will install any dependencies you might need to run this project in your virtual environment.


## Exercises

### 


### 


### 



[Data Minded Academy]: https://www.dataminded.academy/
