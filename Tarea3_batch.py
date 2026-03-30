# Importar librería necesaria para el análisis
from pyspark.sql import SparkSession, functions as F

# Iniciar sesión en Spark
spark = SparkSession.builder.appName('RetailBatchAnalysis').getOrCreate()

# Ruta de dataset almacenado en HDFS
file_path = 'hdfs://localhost:9000/Tarea3/online_retail.csv'

# Definición del dataframe usando la ruta del dataset
df = spark.read.format('csv')\
    .option('header', 'true')\
    .option('inferSchema', 'true')\
    .load(file_path)

# Estructura del dataset
print("Esquema del dataset")
df.printSchema()

#------------------------------------------------------------------------
# Selección de columnas relevantes del análisis

print("Se acota las columnas del análisis")
df = df.select(
    "StockCode","Quantity","UnitPrice","InvoiceDate","Country"
)

print("Primeras filas del dataframe")
df.show(10)

#------------------------------------------------------------------------
# Limpieza de datos 

# Limpieza_1: identificación de valores nulos Conteo por columna
print("Conteo valores nulos por columna")

df.select([
    F.count(F.when(F.col(c).isNull(), c)).alias(c) 
    for c in df.columns
]).show()

# Limpieza_2: Filtro que descarta devoluciones (no positivos en Quantity)
#             Filtro que descarta registros sin valor comercial (no positivos en UnitPrice)
print("Limpieza de datos")

df_clean = df.filter(
    (F.col("Quantity") > 0) & # elimina devoluciones
    (F.col("UnitPrice") > 0) # elimina registros sin valor comercial
)

# Estadísticas_básicas_1: Comparacion de registros antes y despues de la limpieza
print("\nCantidad de registros antes de la limpieza: ", df.count())
print("Cantidad registros despues de la limpieza: ", df_clean.count())
print("\n")

# Estadísticas_básicas_2: resumen estadístico general
df_clean.summary().show()

#------------------------------------------------------------------------
# Transformaciones del Dataset
print("Transformaciones: columnas derivadas Year, Month, Day, TotalPrice")

# Transformacion_1: Convertir fecha string en tipo de dato fecha
df_clean = df_clean.withColumn(
    "InvoiceDate", F.to_timestamp("InvoiceDate", "M/d/yyyy H:mm")
)

# Transformacion_2: Definición de variables derivadas de tiempo (YEAR, MONTH, DAY)
df_clean = df_clean.withColumn("Year", F.year("InvoiceDate")) \
                   .withColumn("Month", F.month("InvoiceDate")) \
                   .withColumn("Day", F.dayofmonth("InvoiceDate"))

# Transformacion_3: Definición de variable TotalPrice
df_clean = df_clean.withColumn(
    "TotalPrice",
    F.round(F.col("Quantity") * F.col("UnitPrice"), 2)
)
# Resultado de transformacion
df_clean.show(5)

#------------------------------------------------------------------------ 
# Analisis_1: Productos más vendidos

print("Productos más vendidos")

top_products = df_clean.groupBy("StockCode") \
    .agg(F.sum("Quantity").alias("TotalQuantity")) \
    .orderBy(F.col("TotalQuantity").desc())

top_products.show(10)

#------------------------------------------------------------------------ 
# Analisis_2: Total ventas agrupado por país

print("Ventas por pais")

sales_by_country = df_clean.groupBy("Country") \
    .agg(F.round(F.sum("TotalPrice"), 2).alias("TotalSales")) \
    .orderBy(F.col("TotalSales").desc())

sales_by_country.show(10)

#------------------------------------------------------------------------ 
# Analisis_3: Total de ingresos de ventas por mes
print("Ventas por mes")

sales_by_month = df_clean.groupBy("Year", "Month") \
    .agg(F.round(F.sum("TotalPrice"), 2).alias("MonthlySales")) \
    .orderBy("Year", "Month")

sales_by_month.show(12)

#------------------------------------------------------------------------ 
#INSIGHT CLAVE
print("Producto con mayor demanda")

top_product = top_products.limit(1)
top_product.show()

#------------------------------------------------------------------------ 
# Pausa de 60 segundos para visualizar Spark UI
import time
time.sleep(60)