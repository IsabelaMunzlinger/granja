import streamlit as st
import mysql.connector
import pandas as pd
import time

# Configuração da página da web
st.set_page_config(page_title="Dashboard Granja", layout="centered")

st.title("🐔 Dashboard de Monitoramento - Grupo 1")
st.write("Acompanhamento em tempo real da temperatura da granja.")

# Função para conectar no banco e puxar as últimas 20 leituras
def buscar_dados():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="granja_db"
        )
        # Puxa os últimos 20 registros
        query = "SELECT id, temperatura, data_hora FROM leituras_temperatura ORDER BY id DESC LIMIT 20"
        df = pd.read_sql(query, conexao)
        conexao.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar no banco de dados: {e}")
        return pd.DataFrame()

# Carrega os dados
df = buscar_dados()

if not df.empty:
    # Pega o dado mais recente (o primeiro da lista)
    temp_atual = df.iloc[0]['temperatura']
    hora_atual = df.iloc[0]['data_hora'].strftime("%H:%M:%S")

    # Criação do alerta visual e indicativo do status da ventoinha
    st.subheader("Status em Tempo Real")
    if temp_atual > 30.0:
        st.error(f"🔥 **ALERTA DE CALOR!** \n\nTemperatura atual: **{temp_atual}°C** \n\nAção Automática: **VENTOINHA LIGADA**")
    else:
        st.success(f"✅ **TEMPERATURA IDEAL** \n\nTemperatura atual: **{temp_atual}°C** \n\nAção Automática: **VENTOINHA DESLIGADA**")
    
    st.write(f"*Última atualização: {hora_atual}*")

    # Criação do Gráfico de Linha
    st.subheader("Histórico Recente de Temperatura")
    
    # Inverte os dados para o gráfico ir do mais antigo (esquerda) pro mais novo (direita)
    df_grafico = df.iloc[::-1].set_index('data_hora')
    st.line_chart(df_grafico['temperatura'])
    
else:
    st.warning("Nenhum dado encontrado no banco de dados. Verifique se o backend está rodando.")

# Faz a página recarregar automaticamente a cada 3 segundos
time.sleep(3)
st.rerun()