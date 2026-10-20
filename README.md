# Sistema Distribuído de Monitorização de Temperatura (Granja)

Este repositório contém a implementação prática do Projeto Integrador para a disciplina de Comunicação de Dados e Aplicações Distribuídas. O sistema realiza a monitorização simulada de temperatura de uma granja utilizando uma arquitetura distribuída com IoT (ESP32), mensageria (MQTT), processamento em Backend (Python), persistência de dados (MySQL) e uma interface de visualização em tempo real (Streamlit).

## 🏗️ Arquitetura e Fluxo de Dados

O projeto aplica os conceitos de sistemas distribuídos separados em responsabilidades distintas:

1. **Origem (Edge/IoT):** Um ESP32 simula a leitura de um sensor de temperatura (DHT22).
2. **Comunicação (Envio):** O ESP32 atua como cliente e publica os dados via Wi-Fi num Broker MQTT público (`test.mosquitto.org`).
3. **Processamento (Backend):** O script `backend.py` assina o tópico MQTT, recebe a temperatura, guarda o histórico no banco de dados MySQL e aplica a regra de negócio (se a temperatura ultrapassar 30°C).
4. **Comunicação (Retorno):** O backend publica uma mensagem de comando (`ON` ou `OFF`) de volta no Broker MQTT.
5. **Ação:** O ESP32 recebe o comando via MQTT e aciona a "ventoinha" (representada pelo LED embutido na placa).
6. **Interface:** O `dashboard.py` consome os dados do MySQL e exibe um painel de monitorização em tempo real para o utilizador final.

## 📂 Estrutura do Repositório

* `leitura_dados/` (ou ficheiro `.ino`): Código C++ para o microcontrolador ESP32 rodar no Arduino IDE.
* `backend.py`: Script Python responsável pela ligação MQTT, regra de acionamento e inserção no banco de dados.
* `dashboard.py`: Aplicação web interativa em Streamlit para visualização dos dados e estado do sistema.

## ⚙️ Pré-requisitos e Instalação

Para correr este projeto localmente, vais precisar de:

* **Hardware:** Placa de desenvolvimento ESP32 e cabo USB.
* **Banco de Dados:** Servidor MySQL.
* **Software:** Python 3.x e Arduino IDE.

### 1. Configuração do Banco de Dados
Cria o banco de dados e a tabela executando o seguinte script SQL no teu MySQL:

```sql
CREATE DATABASE granja_db;
USE granja_db;

CREATE TABLE leituras_temperatura (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura FLOAT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Configuração do Python
Abra o terminal e instale as bibliotecas necessárias para o backend e para o dashboard:

```bash
pip install paho-mqtt mysql-connector-python streamlit pandas
```
### 3. Configuração do ESP32
1. Abra o código fonte do ESP32 na Arduino IDE.
2. Certifique-se de ter a biblioteca `PubSubClient` (por Nick O'Leary) instalada.
3. Altere as variáveis `ssid` e `password` com as credenciais da sua rede Wi-Fi.
4. Conecte o ESP32 ao computador e faça o upload do código.

## 🚀 Como Executar

O sistema distribuído requer que as partes funcionem simultaneamente:

1. **Inicie o IoT:** Ligue o ESP32. Você pode monitorar a conexão com o Wi-Fi e os envios de temperatura abrindo o Monitor Serial da Arduino IDE (baud rate `115200`).
2. **Inicie o Backend:** Abra um terminal na pasta do projeto e execute:
   ```bash
   python backend.py
   ```
   *Você verá no terminal as temperaturas sendo recebidas e os comandos sendo enviados de volta ao ESP32.*
3. **Inicie o Dashboard:** Abra um **novo** terminal na mesma pasta e execute:
   ```bash
   streamlit run dashboard.py
   ```
   *Uma aba será aberta automaticamente no seu navegador exibindo o gráfico em tempo real.*

## 👥 Autores
* Isabela Cristina Munzlinger
* Isabela Fernandes
* Marcos Eduardo Ribas
* Vitor Bruno Chiamulera
