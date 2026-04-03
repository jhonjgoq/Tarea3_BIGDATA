from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, round, to_timestamp, avg, count 
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType
import logging

# Crear sesión Spark "RetailStreamingAnalysis"
spark = SparkSession.builder \
    .appName("RetailStreamingAnalysis") \
    .getOrCreate()
    
# Configura el nivel de log a WARN para reducir los mensajes INFO
spark.sparkContext.setLogLevel("WARN")

#Definir el esquema de los datos del Topic proveneientes de Kafka
schema = StructType([
    StructField("StockCode", StringType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("UnitPrice", DoubleType(), True),
    StructField("TotalPrice", DoubleType(), True),
    StructField("Country", StringType(), True),
    StructField("InvoiceDate", StringType(), True)
])

# Lectura de datos desde el Topic proveniente de Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ventas_online") \
    .load()
    
# De kafka (binary) pasan a string
df_value = df_kafka.selectExpr("CAST(value AS STRING)")

# Pasan de string a JSON estructurado y de JSON a columnas
df_json = df_value.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

#--------
# Convertir la columna InvoiceDate a formato fecha
df_json = df_json.withColumn(
    "InvoiceDate",
    to_timestamp("InvoiceDate", "yyyy-MM-dd HH:mm:ss")
)

##------------------------------------------
##Análisis 1: Ventas por país en tiempo real
#ventas_pais = df_json.groupBy("Country") \
#    .agg(round(sum("TotalPrice"), 2).alias("TotalSales"))
    
##------------------------------------------
##Análisis 2: Productos más vendidos
#top_productos = df_json.groupBy("StockCode") \
#    .agg(sum("Quantity").alias("TotalQuantity")) \
#    .orderBy(col("TotalQuantity").desc())
    
#------------------------------------------
#Análisis 3: Ventas por ventana de tiempo (cada 5 segundos)
ventas_tiempo = df_json \
    .withWatermark("InvoiceDate", "1 minute") \
    .groupBy(
        window("InvoiceDate", "5 seconds"),
        col("Country")
    ) \
    .agg(round(sum("TotalPrice"), 2).alias("Ventas"))
    
#------------------------------------------
# Salida de resultados en la consola
#query1 = ventas_pais.writeStream \
#    .outputMode("complete") \
#    .format("console") \
#    .start()

#query2 = top_productos.writeStream \
#    .outputMode("complete") \
#    .format("console") \
#    .start()
    
query3 = ventas_tiempo.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()
    
#------------------------------------------
#Mantener la ejecución
spark.streams.awaitAnyTermination()

