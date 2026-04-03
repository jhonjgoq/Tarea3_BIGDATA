# Práctica BIG DATA Tarea 3
+ **Tarea 3: Análisis de datos Batch y Streaming con Apache Spark y Apache Kafka**
+ **Autor: Jhon Jairo Gomez Quijano**
+ **Grupo: 58**
+ **Curso: Big Data UNAD**

## Instrucciones de ejecución de la solución Tarea 3 BIG DATA
### Índice de contenidos: Procesamiento de datos por lotes (Batch)
1. [Elementos de la práctica BIG DATA Tarea 3](#elementos-de-la-práctica-big-data-tarea-3)
2. [Dataset (objeto de estudio) información](#dataset-objeto-de-estudio-información)
3. [Requisitos preliminares (Obtención de Dataset online_retailcsv)](#requisitos-preliminares-obtención-de-dataset-online_retailcsv)
4. [Iniciar servicios de Hadoop y cargar el dataset al sistema HDFS](#iniciar-servicios-de-hadoop-y-cargar-el-dataset-al-sistema-hdfs)
5. [Instrucciones de ejecución del script Tarea3_batchpy (Análisis con Apache Spark)](#instrucciones-de-ejecución-del-script-tarea3_batchpy-análisis-con-apache-spark)

### Índice de contenidos: Procesamiento de datos por lotes (Batch)
1. [Requisitos preliminares de instalación y configuración (Spark Kafka y Streaming)](#requisitos-preliminares-de-instalación-y-configuración-spark-kafka-y-streaming)
2. [Instrucciones de ejecución del procesamiento de datos en tiempo real integrando Kafka y Streaming en Spark](#instrucciones-de-ejecución-del-procesamiento-de-datos-en-tiempo-real-integrando-kafka-y-streaming-en-spark)
---

## Elementos de la práctica BIG DATA Tarea 3 
- Máquina Virtual (Oracle VirtualBox)
	- Nombre máquina: BIGDATA
	- Descripción: Ubuntu Server 22.04.05 LTS
	- Usuarios creados en la máquina virtual:
	
		| Nombre usuario | Password |
		| :--- | :--- | 
		| vboxuser | bigdata |
		| hadoop | hadoop |
		
- Sobre la máquina virtual BIGDATA:
	- Se ejecuta una instalación de Java, PIP3, Hadoop, Spark, Kafka.
	
- Sofware PuTTY Release 0.83 ejecutándose en Windows
	- Descarga URL: https://www.chiark.greenend.org.uk/~sgtatham/putty/
		
	- Se conecta vía SSH usando la IP de la máquina virtual BIGDATA, lo que permite extender la terminal Linux de la máquina virtual BIGDATA a una sesión remota PuTTY en Windows. 

--- 
## Dataset (objeto de estudio) información

+ Tema: comercio electrónico (ventas minorístas en línea y transacciones de clientes) 
+ Fuente: obtenido en la Web de Kaggle
+ URL: https://www.kaggle.com/datasets/thedevastator/online-retail-sales-and-customer-data/data
	
+ Última actualización: 2023/12/21
+ Dataset nombre: Online Retail Sales and Customer Data
+ Dataset autor: Szafraniec Marc
+ Dataset file: online_retail.csv

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
## Requisitos preliminares (Obtención de Dataset online_retail.csv)  
  
En la práctica se usa Jupyter Notebook desde Windows para descargar el dataset, luego empleando una carpeta compartida entre Windows y la máquina virtual BIGDATA se tranfiere el dataset `online_retail.csv` al directorio `/home/hadoop/` para iniciar el análisis de datos históricos (Batch) usando Hadoop y Spark. Para conseguir esto seguir las siguientes indicaciones: 
- En terminal PowerShell se instala el paquete Python de kagglehub

```powershell
pip install kagglehub
```
- Se inicia Jupyter Notebook desde PowerShell

```powershell
jupyter notebook
```
- En una sesión notebook de Jupyter usando Python se importa la librería kagglehub y se descarga el dataset

```python
import kagglehub
path = kagglehub.dataset_download("thedevastator/online-retail-sales-and-customer-data")
print("Path to dataset files:", path)
```
Como resultado se tiene que la descarga del dataset (online_retail.csv) está almacenada en el siguiente directorio:\
`C:\Users\TuUsuario\.cache\kagglehub\datasets\thedevastator\online-retail-sales-and-customer-data\versions\1`\ \
**Nota:** el nombre del usuario (TuUsuario) varía según la configuración de usuario de Windows.
		
- Se crea una carpeta compartida entre Windows y la máquina virtual BIGDATA desde PowerShell
	
    ```powershell
    mkdir C:\Users\TuUsuario\Documents\comp_bigdata
    ```
**Nota:** el nombre del usuario (TuUsuario) varía según la configuración de usuario de Windows.\
	
- Con la máquina virtual BIGDATA apagada, desde Oracle VirtualBox se configura la carpeta compartida con los siguientes pasos:
	+ Clic en la máquina virtual BIGDATA
	+ Clic en `Configuración` => `Carpetas compartidas` => `Añadir nueva carpeta`
	+ En la ventana emergente configurar las siguientes opciones:
		+ Ruta de carpeta: `C:\Users\TuUsuario\Documents\comp_bigdata`
		+ Nombre de carpeta: `comp_bigdata`
		+ Clic en Automontar
		+ Clic en Aceptar
- Se copia el Dataset (online_retail.csv) a la carpeta compartida desde la ruta de descarga con la siguiente instrucción en PowerShell:
	
    ```powershell
    cp C:\Users\TuUsuario\.cache\kagglehub\datasets\thedevastator\online-retail-sales-and-customer-data\versions\1\online_retail.csv C:\Users\TuUsuario\Documents\comp_bigdata\
    ```
	**Nota:** el nombre del usuario (TuUsuario) varía según la configuración de usuario de Windows.\
- Se requiere instalar `virtualbox-guest-utils` en la máquina virtual BIGDATA para tener un punto de montaje de la carpeta compartida configurada.\
	Por defecto el punto de montaje de la carpeta compartida en la máquina virtual BIGDATA es: `/media/sf_comp_bigdata`
			
- Iniciar la máquina virtual BIGDATA desde Oracle VirtualBox
	- Ingresar con usuario: `vboxuser` y password: `bigdata`
	- Sincronizar y actualizar lista de paquetes (password: `bigdata`)
	<br> </br>
    ```bash
    sudo apt update
    ```
	- Instalar el paquete virtualbox-guest-utils (password: `bigdata`)
	<br> </br>
    ```bash
    sudo apt install virtualbox-guest-utils
    ```
	- Se requiere reiniciar la máquina virtual BIGDATA
	<br> </br>
    ```bash
    sudo reboot
    ```
	
- Después del reinicio de la máquina virtual BIGDATA	
	- Ingresar con usuario: `vboxuser` y password: `bigdata`
	- Agregar el usuario `hadoop` al grupo `vboxsf` para garantizar los permisos de acceso a la carpeta compartida `/media/sf_comp_bigdata`. La contraseña de superusuario es password: `bigdata`
	<br> </br>
    ```bash
    sudo usermod -aG vboxsf hadoop
    ```
	- Agregar el usuario `vboxuser` al grupo `vboxsf` para garantizar los permisos de acceso a la carpeta compartida `/media/sf_comp_bigdata`. La contraseña de superusuario es password: `bigdata`
	<br> </br>
    ```bash
    sudo usermod -aG vboxsf vboxuser
    ```
	- Se requiere reiniciar la máquina virtual BIGDATA
	<br> </br>
    ```bash
    sudo reboot
    ```
- Se verifica el proceso accediendo desde la terminal de la máquina virtual BIGDATA al ditrectorio `/media/sf_comp_bigdata` donde se puede visualizar el dataset `online_retail.csv` con la siguiente instrucción.
	
    ```bash
    ls /media/sf_comp_bigdata/
    ```
---

## Iniciar servicios de Hadoop y cargar el dataset al sistema HDFS 

- **Paso 0.** En la terminal de la máquina virtual BIGDATA verificar en la terminal la IP asignada con el siguiente comando:
	
    ```bash 
    hostname -I
    ```
	Ejemplo: se tiene como respuesta la `IP = 192.168.0.17`\
	**Nota:** Usar la IP para iniciar sesión en PuTTY mediante SSH
		
- **Paso 1.** Iniciar una sesión PuTTY desde el ejecutable
	- En la ventana `PuTTY Configuration` agregar la IP de la máquina virtual BIGDATA en el campo Hosst Name
		- Para esta práctica se configuró `Host Name (or IP address): 192.168.0.17`
		- Nota: la IP varía según la configuración de la máquina virtual BIGDATA.
	- Cuando se inicia la terminal de la sesión PuTTY se configura el usuario hadoop para identificar la terminal remota 
		- `login as: hadoop`
		- `password: hadoop`
	- Tras el inicio de la sesión en PuTTY de la terminal `hadoop@BIGDATA` se ubica el dataset `online_retail.csv` en la ruta `/media/sf_comp_bigdata/` el cual define el punto de montaje de la carpeta compartida.
		
        ```bash
        ls /media/sf_comp_bigdata/
        ```
		Resultado en la terminal: `online_retail.csv`
	- Copiar el dataset `online_retail.csv` de la carptea compartida a la carpeta `/home/hadoop`
		
        ```bash
        cp /media/sf_comp_bigdata/online_retail.csv /home/hadoop/
        ```
		Se verifica que se ha copiado de forma exitosa con el comando
		
        ```bash
        ls /home/hadoop/
        ```
		Debe presentarse como resultado el listado el dataset: `online_retail.csv`\
		   
- **Paso 2.** Se inician los servicios del clúster de Hadoop en la sesión de PuTTY `hadoop@BIGDATA` 
	- En la terminal se incian los servicios Hadoop con la siguiente instrucción.
		
        ```bash
        start-all.sh
        ```
	- Se confirma que los servicios están activos con el siguiente comando.
		
        ```bash
        jps
        ```
	- Como respuesta exitosa en la terminal se deben mostrar el siguiente listado de servicios activos.
		- DataNode
		- SecondaryNameNode
		- NameNode
		- ResourceManager
		- NodeManager
		
	- **Alternativa gráfica:** para confirmar que Hadoop está activo se accede a Hadoop UI desde el navegador web usando 
		- la IP de la máquina virtual BIGDATA, para esta práctica se uso `IP: 192.168.0.17`
		- el puerto 9870
		- Configuración de la URL: http://192.168.0.17:9870
		- Si se observa en el navegador `Overview 'localhost:9000' (active)` se comprueba que el proceso es exitoso.
	
- **Paso 3.** Creación del directorio `Tarea3` y agregación del dataset `online_retail.csv` en el sistema de almacenamiento distribuido HDFS. 
	- Se crea desde la terminal sesión de PuTTY `hadoop@BIGDATA` el directorio Tarea3 en el sistema HDFS
		
        ```bash
        hdfs dfs -mkdir /Tarea3
        ```
	- Se mueve el dataset `online_retail.csv` descargado y copiado hacia el directorio HDFS creado `/Tarea3`
		
        ```bash
        hdfs dfs -put /home/hadoop/online_retail.csv /Tarea3/
        ```
	- Se valida que el dataset (online_retail.csv) este en la lista de archivos HDFS
		
        ```bash
        hdfs dfs -ls /Tarea3
        ```
	- Como resultado se debe tener algo simialar a:
		
		```bash
		-rw-r--r--   1 hadoop supergroup   49543683 2026-03-29 04:18 /Tarea3/online_retail.csv
		```
	- **Alternativa gráfica:** validación desde el navegador web
		- Se accede a la interfaz gráfica de Hadoop usando el puerto 9870
		- Se ingresa la URL: http://IP:9870 Por ejemplo: URL: http://192.168.0.17:9870
		- En la interfaz gráfica se navega por `Utilities` => `Browse the file system`
		- Como resultado:
			- Se observa en Browse Directory la lista de directorios HDFS creados con atributos Permission, Owner, Group, Size, Last Modified, Replication, Block Size, Name
		- Clic en directorio Tarea3 (ver atributo Name) para ver su contenido donde se ubica el dataset `online_retail.csv`
		
	- **Importante:** Para el análisis (Batch con Apache Spark)siguiente la sesión en PuTTY `hadoop@BIGDATA` se mantiene activa en segundo plano (no se cierra la sesión PuTTY).

---

## Instrucciones de ejecución del script Tarea3_batch.py (Análisis con Apache Spark)
  
- **Paso 1.** Iniciar una sesión PuTTY desde el ejecutable putty.exe con el usuario `vboxuser`
	- En la ventana PuTTY Configuration agregar la IP de la máquina virtual BIGDATA en el campo Host Name (or IP address)
		- Para la práctica se uso `Host Name: 192.168.0.17`
	- Configurar en la terminal la sesión PuTTY el usuario `vboxuser` 
		- `login as: vboxuser`
		- `password: bigdata`
		
- **Paso 2.** Construcción y Ejecución del script Python `Tarea3_batch.py` para el análisis histórico de los datos. 
	- En la sesión de la terminal vboxuser@BIGDATA se crea el script `Tarea3_batch.py` empleando el editor de texto `nano` como sigue:
	<br> </br>
    ```bash
    nano Tarea3_batch.py
    ```
	Nota: el editor nano crea un archivo Python vacío.
		   
	- El código fuente en el script `Tarea3_batch.py` se copia y se pega en el editor `nano` abierto en PuTTY.
		- Copiar código fuente del script en el repositorio GitHub llamado [Tarea3_batch.py](./Tarea3_batch.py) 
		- Pegar con clic derecho sobre el editor nano.
		- Se usa la combinación CTRL + X para guardar datos y confirmar el nombre del script.
		- Se usa la combinación CTRL + O para cerrar el editor nano.
		   
	- Se ejecuta el script `Tarea3_batch.py` con el código fuente del análisis Batch
	
    ```bash
    python3 Tarea3_batch.py
    ```
	- Salida del script: en la terminal se presenta los resultados del análisis.
		   
	- Nota: al final del script se observa una línea que permite pausar la ejecución en curso duarante 60 segundos. Lo que permite navegar en la interfaz gráfico de Apache Spark. Debido a que en 
	- Nota: Apache Spark UI solo es accesible mientras el script Tarea3_batch.py](./Tarea3_batch.py) está en ejecución.
	   
	- Se accede a la interfaz gráfica de Apache Spark usando el puerto 4040
		- Se ingresa la URL: http://IP:4040 Por ejemplo: URL: http://192.168.0.17:4040
		- En la interfaz gráfica se navega por 
		
		
## Requisitos preliminares de instalación y configuración (Spark Kafka y Streaming)
  
- **Paso 1.** Se inicia una sesión de terminal remota con PuTTY con las siguientes configuraciones:
  
  - Host Name (or IP address) = `IP de la máquina virtual BIGDATA`\
  Para esta práctica se utiliza `IP = 192.168.0.17`
  - Login as: `vboxuser`
  - Password: `bigdata`
  - Se obtiene una sesión PuTTY identificada por `vboxuser@BIGDATA`
  
- **Paso 2.** Instalaciones requeridas para iniciar el servidor Kafka
  
  - En la terminal `vboxuser@BIGDATA` instalar el paquete `kafka-python`
  
    ```bash
    pip3 install kafka-python
    ```
  
	Nota: se puede comprobar la instalación de `kafka-python` con el siguiente comando bash
  
    ```bash
    pip3 list | grep kafka-python
    ```
  
  - Se procede a descargar la distribución binaria de Apache Kafka versión 3.9.2 desde la URL: https://downloads.apache.org/kafka/3.9.2/kafka_2.12-3.9.2.tgz con la siguiente instrucción en la terminal bash de la sesión PuTTY.
  
    ```bash
    wget -c https://downloads.apache.org/kafka/3.9.2/kafka_2.12-3.9.2.tgz
    ```
  
  Nota: la descarga se almacena en el directorio actual de trabajo de la terminal, para comprobar que el paquete de binarios `kafka_2.12-3.9.2.tgz` se encuentra basta ejecutar
  
    ```bash
    ls -lh kafka_2.12-3.9.2.tgz 
    ```
  
  Como respuesta positiva se debe visualizar los siguiente en la terminal
  
    ```bash
    -rw-rw-r-- 1 vboxuser vboxuser 117M Feb 22 05:17 kafka_2.12-3.9.2.tgz
    ```
  
  - Se procede a desempaquetar los binarios de Apache Kafka versión 3.9.2 descomprimiendo como sigue
    
      ```bash
      tar -xzf kafka_2.12-3.9.2.tgz 
      ```
  
  Como resultado se crea un nuevo directorio llamado `kafka_2.12-3.9.2`
  
  - Ahora se debe mover con permisos de super usuario la carpeta `kafka_2.12-3.9.2` a la ruta `/opt` para este caso al mover se renobra el directorio como `Kafka`
    
      ```bash
      sudo mv kafka_2.12-3.9.2 /opt/Kafka
      ```
	Nota: no olvidar que la contraseña de super usuario es password: `bigdata`
	
## Instrucciones de ejecución del procesamiento de datos en tiempo real integrando Kafka y Streaming en Spark
	
**Resumen del flujo operacional de Streaming para Big Data**
	
| Paso | Proceso | Descripción |
| :--- | :--- | :--- |	
| 1 | `Zookeeper` | coordina o gestionar el estado del clúster |
| 2 | `Kafka` | inicia el motor de mensajería |
| 3 | `Topic` | crea el canal o almacén de mensajes |
| 4 | `Producer` | envía datos al Topic |
| 5 | `Consumer` | lee los datos del Topic |
	
- **Paso 1.** **Iniciar servicios ZooKeeper**
   
  Se requiere iniciar el servidor ZooKeeper en segundo plano para gestionar el estado del clúster, configuraciones e identificar que servidores (brokers) están activos. Dentro del directorio `/opt/Kafka/bin` se debe iniciar el script `zookeeper-server-start.sh` para encender los servicios, y dentro del directorio `/opt/Kafka/config/` se debe iniciar las configuraciones registradas en `zookeeper.properties`. 	
  
    ```bash
    sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &
    ```
  
  Nota: cuando los procesos de la terminal han concluido se requiere pulsar la tecla Intro para que aparezca de nuevo el prompt de la terminal.
	
- **Paso 1.2.** **Verificar servicios activos de ZooKeeper**
  
  Para verificar que los servicios iniciados por `zookeeper-server-start.sh` están activos se debe verificar que el proceso interno de Zookeper denominado `QuorumPeerMain` está activo se usa `jps` como sigue en bash.
  	
    ```bash
    sudo jps
    ```
	
  Resultado ejemplo en la terminal después de aplicar `sudo jps`, donde `QuorumPeerMain` garantiza que ZooKeeper está activo:
  
    ```bash
    vboxuser@BIGDATA:~$ sudo jps
    2144 Jps
    1721 QuorumPeerMain
    ```
  **Nota:** esperar al menos 10 segundos antes de iniciar los servicios del servidor Kafka
  <br> </br>
---
  
- **Paso 2.** **Iniciar el servidor Kafka**
  
  Se requiere iniciar el servidor (Broker) de Kafka en segundo plano para activar el servicio del motor de mensajería. Dentro del directorio `/opt/Kafka/bin` se debe iniciar el script `kafka-server-start.sh` para encender el servicio Kafka, y dentro del directorio `/opt/Kafka/config/` se debe iniciar las configuraciones registradas en `server.properties`.
  
    ```bash
    sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
    ```
  
- **Paso 2.1.** **Verificar servicios activos de Kafka**
  
  Para verificar que los servicios iniciados por `kafka-server-start.sh` están activos se debe verificar que el proceso interno de Kafka denominado `Kafka` está activo se usa `jps` como sigue en bash.
  
    ```bash
    sudo jps
    ```
  
  Resultado ejemplo en la terminal después de aplicar `sudo jps`, permite confirmar que `QuorumPeerMain` y `Kafka` están activos:
  
    ```bash
    vboxuser@BIGDATA:~$ sudo jps
    4050 QuorumPeerMain
    4963 Jps
    4493 Kafka
    ```
  
  Nota: cuando los procesos de la terminal han concluido se requiere pulsar la tecla Intro para que aparezca de nuevo el prompt de la terminal.
  <br> </br>
---  
  
- **Paso 3.** **Creación del Topic**\
  Se requiere construir el canal de comunicación por donde viajan los datos
    - `--create --topic ventas_online` crea una bandeja de entrada de mensajes llamado `ventas_online`
    - `--bootstrap-server localhost:9092` especifica la dirección del servidor kafka que debe conectarse para crear el Topic `ventas_online`
    - `--partitions 1` particiones que debe crear Kafka para procesar los datos en paralelo. 
    - `--replication-factor 1` especifica el número de copias de seguridad de los datos. La asignación depende del número de servidores (Broker). 
  
  Con la instrucción a continuación en bash se construye el almacen de mensajes
  
    ```bash
    /opt/Kafka/bin/kafka-topics.sh --create \
    --topic ventas_online \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
    ```
  
  Para comprobar que el Topic `ventas_online` ha sido creado se ejecuta en la terminal el siguiente comando:
  
    ```bash
    /opt/Kafka/bin/kafka-topics.sh --describe \
    --topic ventas_online \
    --bootstrap-server localhost:9092
    ```
  
  Como resultado se presenta una descripción detallada del Topic, por ejemplo:
  
    ```bash
    vboxuser@BIGDATA:~$ /opt/Kafka/bin/kafka-topics.sh --describe --topic ventas_online --bootstrap-server localhost:9092
    Topic: ventas_online    TopicId: 5irB-iuPSKOrf6tDlKhuXw PartitionCount: 1      ReplicationFactor: 1     Configs:
    Topic: ventas_online    Partition: 0    Leader: 0       Replicas: 0    Isr: 0   Elr: N/A        LastKnownElr: N/A
    ```
  <br> </br>
---
  
- **Paso 4.** **Producer:** generación de datos simulados envíados al **Topic**
  
  - **Preliminares:** **Creación del diccionario de datos** que referencia la simulación de datos aleatorios de ventas online desde un archivo JSON.
  
  Tomando como referencia el dataset `online_retail.csv` objeto de estudio obtenido de la carpeta compartida con punto de montaje `/media/sf_comp_bigdata/`, el cual, tenemos una copia en el directorio `/home/vboxuser/`.
  
  Se procede a generar un diccionario con los valores únicos de las columnas `StockCode`, `UnitPrice` y `Country` para referenciar la simulación de un generador de datos aleatorios de ventas online que toma como elementos de dominio las listas con los valores únicos de cada columna. Sin embargo, se tienen las siguientes consideraciones:
  
  - Las columnas `StockCode` de código de inventario y `UnitPrice` precio unitario por producto de inventario están relacionadas.
  
  - Las columnas `StockCode` y `UnitPrice` en el archivo JSON se relacionan mediante la estructura clave-valor (key-value) `{StockCode: UnitPrice}`, por ejemplo:
  
    ```json
    {
      "1234A": 9.45,
      "2344B": 25.67
    }
    ```
  
  - Para la columna `Country` se genera una lista de los valores únicos, por ejemplo:
  
    ```json
    ["unit Kingdom", "France", "Germany"]
    ```
  
  - En la terminal de la sesión PuTTY `vboxuser@BIGDATA` se requiere instalar el paquete `Pandas` para generar el diccionario que referencia la simulación de datos aleatorios de ventas online.
  
    ```bash
    pip3 install pandas
    ```
  
  - Copiar el dataset `online_retail.csv` contenido en la carpeta compartida de la máquina virtual con punto de montaje `/media/sf_comp_bigdata/` empleando el siguiente comando:
  
    ```bash
    cp /media/sf_comp_bigdata/online_retail.csv /home/vboxuser/
    ```
   
  - Con el editor de `nano` crear el script `generar_metadata.py` generador del dicionario `metadata_onlineretail.json` en la sesión PuTTY `vboxuser@BIGDATA` usando el comando:
  
    ```bash
    nano generar_metadata.py
    ```
  
  - Copiar el siguiente código fuente Python dentro del editor `nano` y se guarda con `CTRL + O` => Pulsar tecla Intro => cerrar el editor nano con `CTRL + X`.
  
    ```python
    # Generador del diccionario referencia de la simulación de ventas online
    
    import pandas as pd
    import json
    
    # Directorio donde se encuentra el dataset online_retail.csv
    path = '/home/vboxuser/online_retail.csv'
    
    # Carga del dataset como dataframe
    df = pd.read_csv(path, encoding='ISO-8859-1')
    
    # Limpieza de valores nulos
    df = df.dropna(subset=['StockCode', 'UnitPrice', 'Country'])
    
    # Limpieza que preserva valores positivos
    df = df[df['UnitPrice'] > 0]
    
    #Extraer valores únicos del dataframe
    metadata = {
        "price_by_stockcode": df.groupby('StockCode')['UnitPrice'].mean().round(2).to_dict(),
        "countries": df['Country'].unique().tolist()
    }
    
    # Guardar archivo json
    with open('metadata_onlineretail.json', 'w') as f:
        json.dump(metadata, f)
    
    print("Archivo metadata_onlineretail.json generado correctamente")
    ```
  
  - Al ejecutar el script `generar_metadata.py` se generará el archivo `metadata_onlineretail.json` partiendo del dataset `online_retail.csv`.
  
    ```bash
    python3 generar_metadata.py
    ```
  
  - **Ejecución de simulador de Ventas Online** soportado en el script `Tarea3_kafka_producer.py`
  
  Una vez que se ha creado el archivo `metadata_onlineretail.json` se procede a ejecutar el script [Tarea3_kafka_producer.py](./Tarea3_kafka_producer.py) para iniciar la generación de datos.
  
  El script [Tarea3_kafka_producer.py](./Tarea3_kafka_producer.py) genera los siguientes campos:
    
	- `StockCode`: toma aleatoriamente una clave del diccionario en el archivo `metadata_onlineretail.json` generado por el script `generar_metadata.py`
    - `Quantity`: generado aleatoriamente entre el intervalo de 1 a 10 productos.
    - `UnitPrice`: referencia su asignación en el valor que se corresponde con la clave asignada para `StockCode`.
    - `TotalPrice`: resulta del producto de `Quantity` y `UnitPrice`.
    - `Country`: toma aleatoriamente un elemento de la lista `countries` contenida en el diccionario `metadata_onlineretail.json`.
    - `InvoiceDate`: asigna la fecha y hora del sistema (formato string) en el instante de generación continua de datos.
  
  Nota: la ejecución del script [Tarea3_kafka_producer.py](./Tarea3_kafka_producer.py) requiere estrictamente de la generación del archivo JSON llamado `metadata_onlineretail.json`.
  
  Se crea el script en la terminal empleando el editor de texto `nano` con la siguiente instrucción:
  
    ```bash
	nano Tarea3_kafka_producer.py
	```
  
  Una vez abierto, se procede a copiar el contenido del archivo [Tarea3_kafka_producer.py](./Tarea3_kafka_producer.py) en el editor `nano`. Para pegar se realiza clic derecho sobre el editor `nano` en la terminal, luego con `CTRL + O` se guarda el script y se sale del editor con la combinación de teclas `CTRL + X`.
  
  **Iniciar la simulación**
  
  Para iniciar la generación continua de datos se ejecuta en la terminal PuTTY `vboxuser@BIGDATA` el siguiente comando:
  
    ```bash
    python3 Tarea3_kafka_producer.py
    ```
  
  Nota: el script [Tarea3_kafka_producer.py](./Tarea3_kafka_producer.py) envia al almacén de datos (Topic `ventas_online`) los datos simulados en formato JSON.
  
  La sesión de la terminal PuTTY donde se ejecutó el script `Tarea3_kafka_producer.py` se mantiene ejecutándose sin cerrarla para simular que se están generando transacciones de ventas online en tiempo real.
  
  Nota: para finalizar la ejecución del script `Tarea3_kafka_producer.py` use la combinación de teclas `CTRL + C`.
  <br> </br>
---  
- **Paso 5.** **Consumer:** lectura de datos simulados desde el **Topic**
  
  - Iniciar una nueva sesión de terminal remota PyTTY con la siguiente configuración:
    - Host Name (or IP address): IP de la máquina virtual. Para esta práctica, como ejemplo se usa `IP: 192.168.0.17`
    - Login as: `vboxuser`
	- Password: `bigdata`
  
  - Crear un nuevo script Python empleando el editor nano con el nombre `Tarea3_streaming_consumer.py` con la siguiente instrucción.
  
    ```bash
    nano Tarea3_streaming_consumer.py
    ```
  
  - Se copia el contenido del archivo [Tarea3_streaming_consumer.py](./Tarea3_streaming_consumer.py) dentro del editor `nano`, luego se procede a guardar con la combinación de teclas `CTRL + O` y se cierra el editor con `CTRL + X`.
  
  **Lectura de datos en tiempo real desde el Topic**
    
  - Ahora se debe iniciar la aplicación de Spark Structured Streaming empleando el script Python [Tarea3_streaming_consumer.py](./Tarea3_streaming_consumer.py), la cual, lee el archivo JSON que recibe el almacén de datos Topic `ventas_online`.
  
    En esta etapa se formaliza el procesamiento en tiempo real incorporando las siguientes dependencias necesarias para cumplir la integración de Streaming con Kafka.
  
    - `spark-submit`: permite lanzar una aplicación a un clúster de Spark para gestionar recursos y dependencias.
    - `--packages`: especifica a Spark que debe descargar automáticamente dependencias externas necesarias desde Maven Central en la integración.
    - `spark-sql-kafka-0-10`: es el conector	específico que permite a Spark Structured Streaming pueda leer los datos de Kafka.
	- `2.12`: referencia la versión de Scala con la que se realiza la compilación.
	- `3.5.8`: especifica la versión de Spark que se está utilizando.
	- Nota: para identificar la versión de Spark y Scala se puede consultar en la terminal bash como sigue:
        
	  ```bash
      spark-submit --version
      ```
    Como resultado ejemplo de la consulta se puede visualizar:
      ```bash
	  vboxuser@BIGDATA:~$ spark-submit --version
      Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /___/ .__/\_,_/_/ /_/\_\   version 3.5.8
          /_/
        
      Using Scala version 2.12.18, OpenJDK 64-Bit Server VM, 11.0.30
      Branch HEAD
      Compiled by user runner on 2026-01-12T04:16:44Z
      Revision 5a48a37b2dbd7b51e3640cd1d947438459556cc6
      Url https://github.com/apache/spark
      Type --help for more information.
	  ```
  
  - Para ejecutar el procesamiento de datos en tiempo real con Spark Structured Streaming empleando el script [Tarea3_streaming_consumer.py](./Tarea3_streaming_consumer.py) en la terminal se introduce el siguiente comando: 	
        
	```bash
	spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8 Tarea3_streaming_consumer.py
	```
  
- **Paso 5.** **Monitoreo del rendimiento y estados del proceso**
  
  Después de ejecutar la aplicación de Spark Structured Streaming, Apache Spark habilita automáticamente una interfaz web de monitoreo accesible a través del puerto `4040`.
  
  Se debe acceder a la interfaz gráfica Spark UI desde el navegador web ingresando con la IP de la máquina virtual BIGDATA y el puerto 4040.
  
    - http://<IP_DE_LA_MAQUINA>:4040
  
    - Ejemplo aplicado: `http://192.168.1.10:4040`  
  
  **Nota**: La interfaz web de Spark UI proporciona información en tiempo real sobre la ejecución de la aplicación:
  
  - `Jobs`: muestra los trabajos ejecutados por Spark mediante los estados (completado, en ejecución, fallido).
  
  - `Stages`: presenta como se dividen los jobs en etapas, lo cual es útil para analizar el rendimiento y los tiempos de ejecución.
  
  - `Tasks`: presenta estadísticas de uso de CPU y procesos en paralelo.  
  
  - `Structured Streaming`: 
  
  - `Storage`: presenta el uso de memoria y uso de psersistencia de datos.
  
  - `Environment`: presenta las configuraciones de Spark y las variables del sistema.  