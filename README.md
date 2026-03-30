# Práctica BIG DATA Tarea 3
+ **Tarea 3: Análisis de datos Batch y Streaming con Apache Spark y Apache Kafka**
+ **Autor: Jhon Jairo Gomez Quijano**
+ **Grupo: 58**
+ **Curso: Big Data UNAD**

# Análisis de ventas en comercio electrónico 
---
## Problema: 
- Identificar patrones de demanda de productos que permita apoyar las decisiones del proceso de gestión del inventario
			
## Tecnologías:
- Apache Hadoop HDFS
- Apache Spark
- Python librería (SparkSession)  
- Python interfaz (PySpark)
- Apache Kafka
	
--- 
## Dataset (objeto de estudio)
- Tema: comercio electrónico (ventas minorístas en línea y transacciones de clientes) 
- Fuente: obtenido en la Web de Kaggle
- URL: https://www.kaggle.com/datasets/thedevastator/online-retail-sales-and-customer-data/data
	
- Última actualización: 2023/12/21
- Dataset nombre: Online Retail Sales and Customer Data
- Dataset autor: Szafraniec Marc
- Dataset file: online_retail.csv

| Columna | Descripción | Tipo de dato |
| :--- | :--- | :--- |
| `InvoiceNo` | Identifica unívocamente cada transacción. | Numérico (Entero) |
| `StockCode` | Referencia el código de inventario asignado a cada producto. | Alfanumérico |
| `Description` | Describe de forma corta el producto. | Texto |
| `Quantity` | Especifica la cantidad de productos vendidos por transacción. | Numérico (Entero) |
| `InvoiceDate` | Presenta la fecha y hora de la ejecución de la compra (transacción aprobada). | Fecha/Hora |
| `UnitPrice` | Referencia el precio unitario del producto asociado a la transacción. | Numérico (Decimal) |
| `CustomerID` | Especifica el número identificador único del cliente que realiza la transacción. | Numérico (Entero) |
| `Country` | Identifica el país donde el cliente realiza la compra. | Texto |	

--- 

## Estructura del proyecto
A continuación, se presenta una descripción de los script creados para ejecutar el análisis del dataset (online_retail.csv)
| Script | Descripción |
| :--- | :--- |
| Tarea3_batch.py | Análisis datos históricos (Batch) con Apache Spark y Hadoop HDFS |
| kafka_producer.py | Generador de datos aleatorios que alimenta el análisis en tiempo real (Streaming) |
| Tarea3_streaming.py | Análisis de procesamiento en tiempo real (Streaming) con Apache Spark y Apache Kafka |
	
---
## Ejecución de la solución
- Ver archivo: instrucciones_ejecucion.md
	
--- 
## Descripción técnica del análisis
- Ver archivo: descripcion_solucion.md