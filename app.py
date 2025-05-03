import streamlit as st
import pandas as pd
import plotly_express as px

# Título y descripción
st.set_page_config(page_title="Análisis de Vehículos Usados", layout="wide")
st.markdown("### 🚗 Análisis de Datos de Vehículos Usados")
st.write("Explora visualmente los patrones y tendencias en datos reales de ventas de vehículos usados.")

# Cargar datos
try:
    data = pd.read_parquet("data_limpia.parquet")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'data_limpia.parquet'. Asegúrate de incluirlo en el mismo repositorio.")
    st.stop()

# Histograma de Año del Modelo por Condición (con interactividad)
st.subheader("Distribución de Año del Modelo por Condición")
fig_year_condition = px.histogram(
    data,
    x="model_year",
    color="condition",
    title="Distribución de Año del Modelo Segmentado por Condición",
    labels={"model_year": "Año del Modelo", "condition": "Condición"},
    color_discrete_sequence=px.colors.qualitative.Prism
)
st.plotly_chart(fig_year_condition, use_container_width=True)

# --- Separador visual ---
st.markdown("---")

# Histograma comparativo de PRECIOS por MODELO de vehículo
st.subheader("Comparación de Precios por Modelo de Vehículo")

# Selección de modelos de vehículos
modelos = data['model'].dropna().unique()
modelo1 = st.selectbox("Selecciona modelo 1", sorted(modelos))
modelo2 = st.selectbox("Selecciona modelo 2", sorted(modelos), index=1)

# Filtrar datos por modelo de vehículo
df1 = data[data['model'] == modelo1]
df2 = data[data['model'] == modelo2]

# Crear histograma comparativo de PRECIOS por MODELO de vehículo
fig_comparativo = px.histogram(
    pd.concat([df1.assign(Modelo=modelo1), df2.assign(Modelo=modelo2)]),
    x="price",
    color="Modelo",
    barmode="overlay",
    nbins=50,
    title=f"Comparación de Precios: {modelo1} vs {modelo2}",
    color_discrete_sequence=["#FF4B4B", "#00BFFF"]
)

fig_comparativo.update_traces(opacity=0.6)
fig_comparativo.update_layout(xaxis_title="Precio", yaxis_title="Frecuencia")

st.plotly_chart(fig_comparativo, use_container_width=True)

# Gráfico de Dispersión: Precio vs. Kilometraje
st.subheader("Relación entre Precio y Kilometraje")
fig_scatter_price_odo = px.scatter(
    data,
    x="odometer",
    y="price",
    title="Gráfico de Dispersión: Precio vs. Kilometraje",
    labels={"odometer": "Kilometraje", "price": "Precio (USD)"},
    trendline="ols"  # Añade una línea de tendencia OLS para visualizar la correlación
)
st.plotly_chart(fig_scatter_price_odo, use_container_width=True)

# Nota explicativa sobre la correlación
st.markdown(
    """
    **Nota sobre la correlación:** En este gráfico, la tendencia general suele ser una **correlación negativa**, donde los puntos tienden a formar una diagonal descendente de izquierda a derecha. Esto significa que, **en general, a mayor kilometraje de un vehículo usado, menor suele ser su precio.**

    **¿Por qué se observa esta tendencia?**

    * **Desgaste y vida útil:** Un mayor kilometraje generalmente indica un mayor uso del vehículo, lo que implica un mayor desgaste de sus componentes (motor, transmisión, suspensión, etc.) y una menor vida útil restante esperada.
    * **Mayor necesidad de mantenimiento:** Los vehículos con más kilómetros recorridos suelen haber requerido y probablemente requerirán más mantenimiento y reparaciones, lo que disminuye su valor percibido.
    * **Percepción del mercado:** Los compradores suelen preferir vehículos con menos kilómetros, ya que los perciben como más nuevos y con menos problemas potenciales.

    La línea de tendencia azul en el gráfico ayuda a visualizar esta relación general. Sin embargo, es importante recordar que otros factores (como la marca, el modelo, la condición, el año, el historial de mantenimiento y la demanda del mercado) también influyen significativamente en el precio de un vehículo usado, por lo que no siempre se observa una correlación perfectamente lineal.
    """
)

# Box Plot del Precio por Condición
st.subheader("Distribución de Precios por Condición del Vehículo")
fig_box_condition_price = px.box(
    data,
    x="condition",
    y="price",
    title="Box Plot: Precio vs. Condición del Vehículo",
    labels={"condition": "Condición", "price": "Precio (USD)"},
    color="condition",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_box_condition_price, use_container_width=True)

# Explicación del Box Plot
st.markdown(
    """
    **¿Cómo leer este gráfico de caja?**

    Este gráfico muestra la distribución de los precios para cada condición del vehículo. Cada 'caja' y sus elementos nos dan información importante:

    * **La línea dentro de la caja:** Representa la **mediana**, que es el precio central. La mitad de los vehículos en esa condición tienen un precio inferior y la otra mitad superior a este valor.
    * **Los bordes de la caja (cuartiles):** El borde inferior de la caja indica el **primer cuartil** (25% de los precios son inferiores a este valor), y el borde superior indica el **tercer cuartil** (75% de los precios son inferiores a este valor). La altura de la caja (rango intercuartílico) muestra la dispersión del 50% central de los datos.
    * **Los 'bigotes' (líneas que se extienden desde la caja):** Indican el rango típico de precios. Los puntos que aparecen fuera de estos bigotes suelen considerarse **valores atípicos** (precios inusualmente altos o bajos para esa condición).

    Al observar este gráfico, puedes comparar rápidamente los rangos de precios típicos y la presencia de valores atípicos entre las diferentes condiciones de los vehículos.
    """
)
