---
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
	
--- 
## Estructura del proyecto
- Tarea3_batch.py -> análisis datos históricos (Batch) con Apache Spark
- kafka_producer.py -> generador de datos aleatorios que alimenta el análisis en tiempo real (Streaming)
- Tarea3_streaming.py -> análisis de procesamiento en tiempo real (Streaming) con Spark y Kafka
	
---
## Ejecución de la solución
- Ver archivo: instrucciones_ejecucion.md
	
--- 
## Descripción técnica
- Ver archivo: descripcion_solucion.md