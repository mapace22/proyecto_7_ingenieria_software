import streamlit as st
import pandas as pd
import plotly_express as px

st.title("Análisis de Datos de Vehículos Usados")
st.write("Esta aplicación muestra un análisis exploratorio de un conjunto de datos de vehículos usados en Estados Unidos.")

try:
    data = pd.read_parquet('data_limpia.parquet')
except FileNotFoundError:
    st.error("No se encontró el archivo 'data_limpia.parquet'. Asegúrate de que esté en la misma carpeta que app.py.")
    st.stop()

st.header("Visualizaciones Interactivas")

hist_button = st.button('Construir histograma del odómetro')

if hist_button:
    st.write('Creando un histograma para la columna odómetro')
    fig_hist = px.histogram(data, x="odometer")
    st.plotly_chart(fig_hist, use_container_width=True)

scatter_button = st.button('Construir gráfico de dispersión (precio vs. año)')

if scatter_button:
    st.write('Creando un gráfico de dispersión para precio vs. año')
    fig_scatter = px.scatter(data, x="model_year", y="price")
    st.plotly_chart(fig_scatter, use_container_width=True)
    