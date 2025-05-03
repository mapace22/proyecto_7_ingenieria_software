import streamlit as st
import pandas as pd
import plotly_express as px

st.title("Análisis de Datos de Vehículos Usados")
st.write("Esta aplicación muestra un análisis exploratorio de un conjunto de datos de vehículos usados en Estados Unidos.")

try:
    data = pd.read_parquet('data_limpia.parquet')
except FileNotFoundError:
    st.error("No se encontró el archivo 'data_limpia.parquet'. Asegúrate de que esté en la misma carpeta.")
    st.stop()

st.header("Distribución de Precios de Vehículos")
st.write("Este gráfico muestra la distribución de precios de los vehículos en el conjunto de datos.")
fig_price = px.histogram(data, x='price', title='Distribución de Precios')
st.plotly_chart(fig_price)

st.header("Distribución de Años de Modelo")
st.write("Este gráfico muestra la distribución de los años de modelo de los vehículos.")
fig_year = px.histogram(data, x='model_year', title='Distribución de Años de Modelo')
st.plotly_chart(fig_year)

st.header("Top 10 Modelos de Vehículos")
st.write("Este gráfico muestra los 10 modelos de vehículos más frecuentes.")
model_counts = data['model'].value_counts().nlargest(10).reset_index()
model_counts.columns = ['model', 'count']
fig_models = px.bar(model_counts, x='model', y='count', title='Top 10 Modelos')
st.plotly_chart(fig_models)
