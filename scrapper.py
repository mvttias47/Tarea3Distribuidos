from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from confluent_kafka import Producer
import time
import json
import datetime

def delivery_report(err, msg):
    """Callback function for Kafka producer to report delivery status"""
    if err is not None:
        print(f'Error al entregar mensaje: {err}')
    else:
        print(f'Mensaje entregado a {msg.topic()} [{msg.partition()}] en offset {msg.offset()}')

# Configuración del productor de Kafka
def crear_productor_kafka():
    return Producer({
        'bootstrap.servers':'localhost:9093'
    })

# Crear productor de Kafka
producer = crear_productor_kafka()

# Configuración de Selenium
options = Options()
options.add_argument("--start-maximized") 
service = Service("/snap/bin/geckodriver") 
driver = webdriver.Firefox(service=service, options=options)

try:
    driver.get("https://www.waze.com/live-map")

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder]'))
    )

    search_box.send_keys("Santiago, Chile")
    time.sleep(1)
    search_box.send_keys(Keys.RETURN) 

    time.sleep(10)

    incidents = []  

    while True: 
        try:
            incident_elements = driver.find_elements(By.CLASS_NAME, 'leaflet-marker-icon')

            for element in incident_elements:
                try:
                    incident_type = element.get_attribute('class')
                    position = element.get_attribute('style')
                    
                    # Crear objeto de incidente
                    incident = {
                        'type': incident_type,
                        'position': position,
                        'timestamp': datetime.datetime.now().isoformat()
                    }
                    
                    # Enviar a Kafka
                    #producer.produce(
                        #topic='waze-incidents',
                        #key=str(datetime.datetime.now().timestamp()),
                        #value=json.dumps(incident),
                        #callback=delivery_report
                    #)
                    kafka_data =  json.dumps(incident).encode('utf-8')  
                    producer.produce('waze-incidents', value=kafka_data)
                    
                    producer.flush()  # Asegura que el mensaje sea enviado
                    print(f"Evento de compra enviado a Kafka con éxito.")
                    
                    incidents.append(incident)
                except Exception as e:
                    print("Error al procesar un elemento:", e)

            break  
        except Exception as e:
            print("Error al intentar capturar incidentes:", e)
            time.sleep(2)

    # Hacer flush final para asegurar que todos los mensajes sean enviados
    producer.flush()

    # Guardar también en archivo JSON como respaldo
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f'incidentes_{timestamp}.json'

    with open(file_name, 'w') as f:
        json.dump(incidents, f, indent=4)

    print(f"Se han guardado {len(incidents)} incidentes en Kafka y en el archivo '{file_name}'.")

except Exception as e:
    print("Ocurrió un error:", e)
    print("HTML actual de la página:")
    print(driver.page_source)

finally:
    print("Script ejecutado. Manteniendo la ventana abierta...")
    time.sleep(60)
    driver.quit()
