# Descripción de la solución - Procesamiento Batch con Apache Spark y Apache Hadoop

## Paso 1. Carga de datos empleando sistema HDFS
	1. El proceso inicia con la creación de una sesión de Apache Spark, la cual permite el procesamiento distribuido de grandes volúmenes de datos.
	2. se realiza la carga del dataset *online_retail.csv* desde el sistema de archivos distribuido HDFS. Se utiliza el formato CSV con encabezados y se habilita la inferencia automática de tipos de datos para facilitar el análisis inicial.

---

## 2. Selección de variables relevantes
Con el objetivo de optimizar el rendimiento del procesamiento y enfocar el análisis en variables clave, se realiza una selección de columnas relevantes:

- **StockCode**: Identificador del producto  
- **Quantity**: Cantidad de unidades vendidas  
- **UnitPrice**: Precio unitario del producto  
- **InvoiceDate**: Fecha de la transacción  
- **Country**: País del cliente  

Esta reducción permite trabajar únicamente con los datos necesarios para el análisis de ventas e inventario.

---

## 3. Análisis de calidad de datos
Se realiza una verificación de valores nulos en cada una de las columnas seleccionadas. Este paso permite identificar posibles inconsistencias en el dataset y evaluar la calidad de los datos antes de aplicar transformaciones.

---

## 4. Limpieza de datos
Se implementan filtros para mejorar la calidad de la información:

- Se eliminan registros con valores no positivos en **Quantity**, ya que representan devoluciones o ajustes.
- Se eliminan registros con valores no positivos en **UnitPrice**, ya que no representan transacciones comerciales válidas.

Adicionalmente, se realiza una comparación del número de registros antes y después de la limpieza para evidenciar el impacto del proceso.

---

## 5. Transformación de datos
Se aplican diversas transformaciones para enriquecer el dataset:

### 5.1 Conversión de fecha
La columna **InvoiceDate**, originalmente en formato texto, se convierte a tipo fecha (timestamp), lo que permite realizar análisis temporales.

### 5.2 Variables derivadas de tiempo
Se generan nuevas columnas:
- **Year**
- **Month**
- **Day**

Estas variables permiten analizar el comportamiento de las ventas en diferentes niveles de granularidad temporal.

### 5.3 Cálculo de ingresos
Se crea la variable **TotalPrice**, calculada como:

> TotalPrice = Quantity × UnitPrice

Este indicador representa el valor total de cada transacción y es fundamental para el análisis financiero.

---

## 6. Análisis exploratorio de datos (EDA)

### 6.1 Productos más vendidos
Se agrupan los datos por **StockCode** y se calcula la suma total de unidades vendidas, permitiendo identificar los productos con mayor demanda.

---

### 6.2 Ventas por país
Se agrupan las ventas por **Country** y se calcula el total de ingresos generados por cada país. Este análisis permite identificar mercados clave y segmentación geográfica.

---

### 6.3 Ventas por periodo de tiempo
Se realiza una agregación por **Year** y **Month** para analizar el comportamiento temporal de las ventas. Este análisis permite identificar tendencias, estacionalidad y variaciones en la demanda.

---

## 7. Insight principal
Se identifica el producto con mayor volumen de ventas, lo cual representa un indicador clave para la toma de decisiones en la gestión de inventarios.

Este resultado permite priorizar productos estratégicos y anticipar necesidades de abastecimiento.

---

## 8. Visualización y monitoreo
Los resultados del procesamiento se visualizan directamente en consola mediante el uso de funciones como `show()`.

Adicionalmente, se habilita una pausa en la ejecución del programa para permitir el acceso a la interfaz gráfica de **Spark UI**, donde es posible monitorear el rendimiento del procesamiento, tareas ejecutadas y uso de recursos.

---

## Conclusión técnica
El procesamiento batch implementado permite analizar el comportamiento histórico de las ventas, identificar productos de alta demanda y entender patrones de consumo.

Estos resultados constituyen la base para complementar el análisis con procesamiento en tiempo real mediante tecnologías como Apache Kafka y Spark Streaming.