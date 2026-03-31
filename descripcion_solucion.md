# Práctica BIG DATA Tarea 3
+ **Tarea 3: Análisis de datos Batch y Streaming con Apache Spark y Apache Kafka**
+ **Autor: Jhon Jairo Gomez Quijano**
+ **Grupo: 58**
+ **Curso: Big Data UNAD**

## Descripción de la solución - Procesamiento Batch con Apache Spark y Apache Hadoop

### Paso 1. Carga de datos empleando sistema HDFS
1. El proceso inicia con la creación de una sesión de Apache Spark, la cual permite el procesamiento distribuido de grandes volúmenes de datos.
2. se realiza la carga del dataset *online_retail.csv* desde el sistema de archivos distribuido HDFS. Se utiliza el formato CSV con encabezados y se habilita la inferencia automática de tipos de datos para facilitar el análisis inicial.

---

### Paso 2. Selección de variables relevantes
Con el objetivo de optimizar el rendimiento del procesamiento y enfocar el análisis en variables clave, se realiza una selección de columnas relevantes:

| Columna | Descripción | Tipo de dato |
| :--- | :--- | :--- |
| `StockCode` | Identificador del producto | Numérico (Entero) |  
| `Quantity` | Cantidad de unidades vendidas | Numérico (Entero) |  
| `UnitPrice` | Precio unitario del producto | Numérico (Decimal) | 
| `InvoiceDate` | Fecha de la transacción (fecha de la factura) | Texto (string) | 
| `Country` | País del cliente (donde se gestionó la transacción) | Texto (string) | 

Esta reducción permite trabajar únicamente con los datos necesarios para el análisis de ventas e inventario.

---

### Paso 3. Análisis de calidad de datos
Se realiza una verificación de valores nulos en cada una de las columnas seleccionadas. Este paso permite identificar posibles inconsistencias en el dataset y evaluar la calidad de los datos antes de aplicar transformaciones.

- Se contabiliza por columna la ocurrencia de valores nulos (`NaN`)
- El dataset `online_retail.csv` para las columnas `StockCode`, `Quantity`, `UnitPrice`, `InvoiceDate` y `Country` no evidencia valores nulos.
- Nota: El dataset `online_retail.csv` en las columnas descartadas `Description` y `CustomerID` evidencia la ocurrencia de valores nulos `NaN`. 
- Como el análisis descarta las columnas `Description` y `CustomerID` con valores nulos, entonces no se ejecuta un mecanismo de tratamiento de valores nulos.      

---

### Paso 4. Limpieza de datos
Se implementan filtros para mejorar la calidad de la información:

- Se eliminan registros con valores no positivos en la columna `Quantity`, puesto que los valores negativos o nulos representan devoluciones o ajustes en las operaciones de comercio electrónico.
- Se eliminan registros con valores no positivos en la columna `UnitPrice`, puesto que los valores negativos o nulos no representan transacciones comerciales válidas en las operaciones de comercio electrónico.

Adicionalmente, se realiza una comparación del número de registros antes y después de la limpieza para evidenciar el impacto del proceso.

---

### Paso 5. Transformación de datos
Se aplican diversas transformaciones para completar el dataset:
   
#### Paso 5.1 Conversión de fecha
La columna **InvoiceDate**, originalmente en formato texto, se convierte a tipo fecha (timestamp), lo que permite realizar análisis temporales.
- **Transformacion_1:** Convertir los datos en la columna `InvoiceDate` con las fechas de tipo string en un formato de Marca de Tiempo `timestampType`

#### Paso 5.2 Variables derivadas de tiempo
Se generan nuevas columnas (segmentando la información temporal) para analizar el comportamiento de las ventas en diferentes niveles de granularidad temporal.
- **Transformacion_2:** Definir nuevas columnas `Year`, `Month` y `Day` para segmentar en datos atómicos los datos en la columna `InvoiceDate`. 
- Lo que permite agrupar los registros en función de las distintas categorías de tiempo segmentadas beneficiando la identificación de patrones.

#### Paso 5.3 Cálculo de ingresos
Se crea la variable **TotalPrice**, calculada como:

> TotalPrice = Quantity × UnitPrice

Este indicador representa el valor total de cada transacción y es fundamental para el análisis financiero.
- **Transformacion_3:** Definir la columna derivada `TotalPrice` desde el producto de las columnas `Quantity` y `UnitPrice` para obtener el valor total de la venta por cada registro.
- **Resultado de la transformación:** Organiza el nuevo dataframe con una versión segmentada y ampliada de los datos.
---

### Paso 6. Análisis exploratorio de datos (EDA)

#### Paso 6.1 Productos más vendidos
Se agrupan los datos por la columna `StockCode` y se calcula la suma total de unidades vendidas columna `Quantity`, permitiendo identificar los productos con mayor demanda.

---

#### Paso 6.2 Ventas por país
Se agrupan las ventas por la columna `Country` y se calcula el total de ingresos generados por cada país sumando los valores de la columna `TotalPrice`. Este análisis permite identificar mercados clave y segmentación geográfica.

---

### 6.3 Ventas por periodo de tiempo
Se realiza una agregación por las columnas `Year` y `Month` para analizar el comportamiento temporal de las ventas sumando la columna `TotalPrice` por cada agrupación temporal. Este análisis permite identificar tendencias, estacionalidad y variaciones en la demanda.

---

### Paso 7. Insight principal
Se identifica el producto con mayor volumen de ventas, lo cual representa un indicador clave para la toma de decisiones en la gestión de inventarios.

Este resultado permite priorizar productos estratégicos y anticipar necesidades de abastecimiento.

---

### Paso 8. Visualización y monitoreo
Los resultados del procesamiento se visualizan directamente en consola mediante el uso de funciones como `show()`.

Adicionalmente, se habilita una pausa en la ejecución del programa para permitir el acceso a la interfaz gráfica de `Spark UI`, donde es posible monitorear el rendimiento del procesamiento, tareas ejecutadas y uso de recursos.

---

### Conclusión técnica
El procesamiento batch implementado permite analizar el comportamiento histórico de las ventas, identificar productos de alta demanda y entender patrones de consumo.

Estos resultados constituyen la base para complementar el análisis con procesamiento en tiempo real mediante tecnologías como Apache Kafka y Spark Streaming.