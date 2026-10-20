#include <WiFi.h>
#include <PubSubClient.h>

// Configurações do Wi-Fi
const char* ssid = "Munzlinger";
const char* password = "Valentino2020";

// Configurações do MQTT (Usando um broker público gratuito)
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;

// Broket público - usaremos o mosquitto
const char* topico_temp = "unoesc/grupo1/granja/temperatura";
const char* topico_ventoinha = "unoesc/grupo1/granja/ventoinha";

// O LED embutido do ESP32 vai simular a ventoinha (Pino 2)
const int pinoVentoinha = 2;

WiFiClient espClient;
PubSubClient client(espClient);

long tempoAnterior = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando na rede: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado! IP: ");
  Serial.println(WiFi.localIP());
}

// Função executada quando uma mensagem MQTT chega (Comando do Python)
void callback(char* topic, byte* payload, unsigned int length) {
  String mensagem = "";
  for (int i = 0; i < length; i++) {
    mensagem += (char)payload[i];
  }
  
  Serial.print("Mensagem recebida no tópico [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(mensagem);

  // Se o Python mandou ligar, liga o LED (Ventoinha). Se não, desliga.
  if (mensagem == "ON") {
    digitalWrite(pinoVentoinha, HIGH);
    Serial.println("-> AÇÃO: Ventoinha LIGADA!");
  } else if (mensagem == "OFF") {
    digitalWrite(pinoVentoinha, LOW);
    Serial.println("-> AÇÃO: Ventoinha DESLIGADA!");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    // ID do cliente aleatório
    String clientId = "ESP32Client-";
    clientId += String(random(0, 1000));
    
    if (client.connect(clientId.c_str())) {
      Serial.println("Conectado!");
      // Assina o tópico para ouvir os comandos da ventoinha
      client.subscribe(topico_ventoinha);
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(pinoVentoinha, OUTPUT);
  digitalWrite(pinoVentoinha, LOW); // Garante que começa desligado

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long tempoAtual = millis();
  // A cada 5 segundos envia uma temperatura simulada
  if (tempoAtual - tempoAnterior > 5000) {
    tempoAnterior = tempoAtual;

    // SIMULAÇÃO DO SENSOR: Gera temperatura aleatória entre 25.0 e 35.0
    float temperaturaSimulada = 25.0 + (random(0, 100) / 10.0);
    
    String tempString = String(temperaturaSimulada);
    Serial.print("Enviando temperatura: ");
    Serial.print(tempString);
    Serial.println(" °C");
    
    // Publica no MQTT
    client.publish(topico_temp, tempString.c_str());
  }
}