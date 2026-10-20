import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

# ================= Configurações =================
MQTT_BROKER = "test.mosquitto.org" 
MQTT_PORT = 1883
TOPICO_TEMP = "unoesc/grupo1/granja/temperatura"
TOPICO_VENTOINHA = "unoesc/grupo1/granja/ventoinha"

# MySQL
DB_HOST = "localhost" 
DB_USER = "root" 
DB_PASSWORD = "root" 
DB_NAME = "granja_db"

# Tenta conectar no banco
try:
    conexao = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conexao.cursor()
    print("Conectado ao MySQL com sucesso!")
except Exception as e:
    print(f"Erro ao conectar no banco: {e}")
    conexao = None

# ================= Funções MQTT =================
def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao Broker MQTT com código de resultado {rc}")
    client.subscribe(TOPICO_TEMP)
    print(f"Inscrito no tópico: {TOPICO_TEMP}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    hora_atual = datetime.now().strftime("%H:%M:%S")
    
    try:
        temperatura = float(payload)
        print(f"\n[{hora_atual}] Temperatura recebida: {temperatura}°C")
        
        # 1. Salvar no Banco de Dados
        if conexao and conexao.is_connected():
            sql = "INSERT INTO leituras_temperatura (temperatura) VALUES (%s)"
            cursor.execute(sql, (temperatura,))
            conexao.commit()
            print("  -> Salvo no Banco de Dados.")
        
        # 2. Regra de Negócio (Ação Distribuída)
        if temperatura > 30.0:
            print("  -> ALERTA: Acima de 30°C! Mandando comando para LIGAR ventoinha.")
            client.publish(TOPICO_VENTOINHA, "ON")
        else:
            print("  -> Temperatura ideal. Mandando comando para DESLIGAR ventoinha.")
            client.publish(TOPICO_VENTOINHA, "OFF")
            
    except ValueError:
        print("Erro: Payload não é um número válido.")

# ================= Execução =================
cliente_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
cliente_mqtt.on_connect = on_connect
cliente_mqtt.on_message = on_message

print("Conectando ao broker...")
# Adicionado keepalive maior para evitar quedas rápidas
cliente_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)

# Inicia o loop infinito para escutar mensagens
cliente_mqtt.loop_forever()