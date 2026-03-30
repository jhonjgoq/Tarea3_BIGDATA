---
# Práctica BIG DATA Tarea 3
+ **Tarea 3: Análisis de datos Batch y Streaming con Apache Spark y Apache Kafka**
+ **Autor: Jhon Jairo Gomez Quijano**
+ **Grupo: 58**
+ **Curso: Big Data UNAD**

## Instrucciones de ejecución de la solución Análisis (Batch) de datos históricos usando Hadoop HDFS y Apache Spark
---
## Elementos de la práctica: 
- Máquina Virtual (Oracle VirtualBox)
	- Nombre máquina: BIGDATA
	- Descripción: Ubuntu Server 22.04.05 LTS
	- Usuarios creados en la máquina virtual:
		- nameuser_1: vboxuser		password: bigdata
		- nameuser_2: hadoop    	password: hadoop
	
- Sofware PuTTY Release 0.83
	- Fuente URL: https://www.chiark.greenend.org.uk/~sgtatham/putty/
		
	- Se conecta vía SSH usando la IP de la máquina virtual BIGDATA
	- para iniciar una sesión PuTTY de la terminal remota Linux
		
	- Se ejecuta una instalación previa de Java, PIP3, Hadoop, Spark, Kafka sobre la máquina virtual BIGDATA.

--- 
## Dataset (objeto de estudio) información

+ Tema: comercio electrónico (ventas minorístas en línea y transacciones de clientes) 
+ Fuente: obtenido en la Web de Kaggle
+ URL: https://www.kaggle.com/datasets/thedevastator/online-retail-sales-and-customer-data/data
	
+ Última actualización: 2023/12/21
+ Dataset nombre: Online Retail Sales and Customer Data
+ Dataset autor: Szafraniec Marc
+ Dataset file: online_retail.csv
	
---
## Requisitos preliminares (Obtención de Dataset online_retail.csv)  
	
### Descripción  
En la práctica se usa Jupyter Notebook desde Windows para descargar el dataset
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

	- Como resultado se tiene que la descarga está almacenada en el directorio
		Directorio de descarga:
		C:\Users\TuUsuario\.cache\kagglehub\datasets\thedevastator\online-retail-sales-and-customer-data\versions\1
		Nota: el nombre del usuario (TuUsuario) varía según la configuración de usuario de Windows.
		
	- Se configura una carpeta compartida entre Windows y la máquina virtual BIGDATA
		1. Se crea un directorio para usar como carpeta compartida
			C:\Users\TuUsuario\Documents\comp_bigdata
		2. Con la máquina virtual apagada en Oracle VirtualBox se accede a:
			Clic en la máquina virtual BIGDATA
			Configuración => Carpetas compartidas => Añadir nueva carpeta
			Ruta de carpeta: C:\Users\TuUsuario\Documents\comp_bigdata
			Nombre de carpeta: comp_bigdata
			Clic en Automontar
			Clic en Aceptar
	- Se copia el Dataset (online_retail.csv) a la carpeta compartida
		Ruta origen C:\Users\TuUsuario\.cache\kagglehub\datasets\thedevastator\online-retail-sales-and-customer-data\versions\1 
		Ruta destino C:\Users\TuUsuario\Documents\comp_bigdata
		
	- Nota: Se requiere instalar virtualbox-guest-utils en la máquina virtual
		BIGDATA para tener un punto de montaje de la carpeta compartida configurada.
	- Nota: Por defecto el punto de montaje de la carpeta compartida en Linux Ubuntu Server es
		>> /media/sf_comp_bigdata
			
	- Iniciar la máquina virtual BIGDATA desde Oracle VirtualBox
		Ingresar con usuario: vboxuser y password: bigdata
		1. Sincronizar y actualizar lista de paquetes
		>> sudo apt update
		>> password: bigdata
		2. Instalar el paquete virtualbox-guest-utils
		>> sudo apt install virtualbox-guest-utils
		3. Se requiere reiniciar la máquina virtual BIGDATA
		>> sudo reboot
		
	- Después del reinicio de la máquina virtual BIGDATA	
		1. Ingresar con usuario: vboxuser y password: bigdata
		2. Agregar el usuario (hadoop) al grupo vboxsf para tener permisos
		   y poder acceder desde el usuario (hadoop) a la carpeta compartida (/media/sf_comp_bigdata)
		   En la terminal ejecutar:
		   >> sudo usermod -aG vboxsf hadoop
		   >> password: bigdata
		Nota: se asignan permisos de acceso al usuario hadoop a la carpeta compartida 
		para poder acceder al Dataset (/media/sf_comp_bigdata/online_retail.csv)
		
#--------------------------------------------------------------------------------------------------
# INSTRUCCIONES PARA INICIAR LA SESION EN PuTTY

Paso 0. En la terminal de la máquina virtual BIGDATA verificar en la terminal 
		la IP asignada a la máquina virtual BIGDATA con el siguiente comando:
		>> hostname -I
		En este ejemplo se tiene como respuesta la IP = 192.168.0.17
		Nota: Usar la IP para iniciar sesión en PuTTY mediante SSH
		
Paso 1. Iniciar una sesión PuTTY desde el ejecutable
		1. En la ventana PuTTY Configuration agregar la IP de la máquina virtual 
		   Ubuntu Server en el campo Host Name (or IP address)
		   Por ejemplo, para la práctica actual se uso IP = 192.168.0.17
		2. Configurar en la terminal de la sesión PuTTY el usuario hadoop 
		>> login as: hadoop
		>> password: hadoop
		3. En la sesión de la terminal hadoop@BIGDATA
		   se puede encontrar el dataset (online_retail.csv) en la siguiente 
		   ruta (punto de montaje de la carpeta compartida)
		   >> ls /media/sf_comp_bigdata/
		   Resultado en la terminal >> online_retail.csv
		4. Copiar el Dataset (online_retail.csv) de la carptea compartida a 
		   la carpeta /home/hadoop
		   >> cp /media/sf_comp_bigdata/online_retail.csv /home/hadoop/
		   Se verifica que se ha copiado de forma exitosa con el comando
		   >> ls /home/hadoop/
		   debe presentarse en el listado el dataset (online_retail.csv)

# INSTRUCCIONES INICIAR SERVICIOS EN CLUSTER HADOOP
		   
Paso 2.	Se inician los servicios del clúster de Hadoop
		>> start-all.sh
		Se confirma los servicios activos con el siguiente comando
		>> jps
		Como respuesta exitosa en la terminal se deben mostrar los servicios
		- DataNode
		- SecondaryNameNode
		- NameNode
		- ResourceManager
		- NodeManager
		
		Nota: para confirmar que Hadoop está activo se accede a la interfaz gráfica
		desde el navegador web usando 
		>> la IP de la máquina virtual BIGDATA
		>> el puerto 9870
		Por ejemplo, para la práctica actual se implementó 
		URL: http://192.168.0.17:9870
		Si se observa en el navegador 
		Overview 'localhost:9000' (active)
		el proceso es exitoso.

# INSTRUCCIONES	AGREGAR DATASET AL SISTEMA DE ALMACENAMIENTO DISTRIBUIDO HDFS DE DATOS MASIVOS
	
Paso 3.	Creación del directorio Tarea3 y agregación del dataset en el sistema HDFS 
		1. Se crea la directorio Tarea3 en el sistema HDFS
		>> hdfs dfs -mkdir /Tarea3
		2. Se mueve el dataset descargado (online_retail.csv) en el directorio Tarea3
		>> hdfs dfs -put /home/hadoop/online_retail.csv /Tarea3/
		Se valida que el dataset (online_retail.csv) este en la lista de archivos HDFS
		>> hdfs dfs -ls /Tarea3
		Como resultado se debe tener algo simialar a:
		-rw-r--r--   1 hadoop supergroup   49543683 2026-03-29 04:18 /Tarea3/online_retail.csv
		
		Alternativa de validación desde el navegador web
		- Se accede a la interfaz gráfica de Hadoop usando el puerto 9870
		- Se ingresa la URL: http://IP:9870
		  Por ejemplo: URL: http://192.168.0.17:9870
		- En la interfaz gráfica se navega por 
			Utilities => Browse the file system
		- Como resultado
		  Se observa en Browse Directory la lista de directorios HDFS creados con atributos 
		  Permission, Owner, Group, Size, Last Modified, Replication, Block Size, Name
		- Clic en directorio Tarea3 (ver atributo Name) para ver su contenido
		- Se visualiza el Dataset (online_retail.csv) agregado.
		
		Nota: La sesión en PuTTY con usuario hadoop se mantiene activa en segundo 
		plano mientras se ejecuta el análisis en otra sesión PuTTY con Apache Spark

#--------------------------------------------------------------------------------------------------
# INSTRUCCIONES DE USO DEL SCRIPT Tarea3_batch.py (Análisis con APACHE SPARK)

Paso 1. Iniciar una sesión PuTTY desde el ejecutable putty.exe
		1. En la ventana PuTTY Configuration agregar la IP de la máquina virtual BIGDATA con 
		   Ubuntu Server en el campo Host Name (or IP address)
		   Por ejemplo, para la práctica actual se uso IP = 192.168.0.17
		2. Configurar en la terminal de la sesión PuTTY el usuario vboxuser 
		>> login as: vboxuser
		>> password: bigdata
		
Paso 2. Construcción y Ejecución del Script Python
		En la sesión de la terminal vboxuser@BIGDATA se crea el script Python
		1. En la terminal con el editor de texto nano se crea el archivo 
		   (script) Tarea3_batch.py con la siguiente instrucción en la terminal
		   >> nano Tarea3_batch.py
		   Nota: el editor nano crea un archivo Python vacío
		   
		2. El código fuente del script (Tarea3_batch.py) compartido en el repositorio GitHub
		   se copia y se pega en el editor nano abierto en PuTTY. Y se ejecuta los siguientes pasos
		   >> Copiar código fuente del script en el repositorio GitHub llamado (Tarea3_batch.py) 
		   >> Pegar con clic derecho sobre la sesión del editor nano
		   >> Se usa la combinación CTRL + X para guardar datos
		   >> Se usa la combinación CTRL + O para cerrar el editor nano
		
		3. Se procede a verificar en la ruta /home/vboxuser/ la existencia del script
		   con el código fuente del análisis de datos histórico Batch. En la terminal
		   se ejecuta el siguiente comando para ver el listado de archivos:
		   >> ls /home/vboxuser/
		   Entre el listado de resultados debe estar (Tarea3_batch.py)
		   
		4. Se ejecuta el script (Tarea3_batch.py) con el código fuente del análisis Batch
		   ejecutando el siguiente comando
		   >> python3 Tarea3_batch.py
		   
		   Resultado: en la terminal se presenta los resultados del análisis.
		   
		   Nota: al final del script se observa una línea que permite mantener 
		   la ejecución en curso duarante 60 segundos.
		   
		   Nota: Esto se realiza para obtener tiempo extra 60 segundos para 
		   navegar en la interfaz gráfico de Apache Spark. Debido a que en 
		   Apache Spark UI solo es accesible para navegar mientras que script 3
		   permanezca en ejecución.
		   
		5. El acceso a la interfaz gráfica Apache Spark UI se debe realizar mientras se ejecuta
		   el script (Tarea3_batch.py) con el análisis histórico de los datos referenciados en el 
		   dataset (online_retail.csv) almacenado el el sistema HDFS en el directorio Tarea3.
		   
		   - Se accede a la interfaz gráfica de Hadoop usando el puerto 4040
		   - Se ingresa la URL: http://IP:4040
		   Por ejemplo: URL: http://192.168.0.17:4040
		   - En la interfaz gráfica se navega por 