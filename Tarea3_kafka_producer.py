import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Carga de diccionario de datos con los valores únicos de
# las columnas {'StockCodes':'UnitPrices'}, 'Countries'
with open('metadata_onlineretail.json', 'r') as f:
    data_ref = json.load(f)

stock_list = list(data_ref['price_by_stockcode'].keys())
countries = data_ref['countries']

# Función que toma aleatoriamente valores de la lista data_ref
# data_ref apunta al json de con los datos 'StockCodes', 'UnitPrices', 'Countries' 
def generar_venta_aleatoria():
    stock = random.choice(stock_list)
    quantity = random.randint(1, 10)
    price = float(data_ref['price_by_stockcode'][stock])
    country = random.choice(countries)
    return {
       "StockCode": stock,
       "Quantity": quantity,
       "UnitPrice": price,
       "TotalPrice": round(quantity * price, 2),
       "Country": country,
       "InvoiceDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Configurar el producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Generación continua de datos
print("Iniciando simulación de ventas envío de datos a Topic Kafka\n")

try:
    while True:
        transaccion = generar_venta_aleatoria()
        try: 
            producer.send('ventas_online', value=transaccion) #Envía al Topic ventas_online
            producer.flush() # garantiza que el mensaje se envía de inmediato sin acumularse en el buffer
            print(f"Enviado: {transaccion}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
        time.sleep(0.5) # cada medio segundo envía una venta
except KeyboardInterrupt:
    print("Simulación detenida")