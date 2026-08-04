import os
import duckdb
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from groq import Groq

def get_secret(key_name: str, default_value: str = "") -> str:
  val = os.getenv(key_name)
  if val:
      return val
  
  try:
      if key_name in st.secrets:
          return st.secrets[key_name]
  except Exception:
      pass
      
  return default_value

load_dotenv()

st.set_page_config(
    page_title="SaaS Churn Analytics & AI Insights",
    page_icon="📊",
    layout="wide"
)

# --- 1. CONEXIÓN A MOTHERDUCK / DUCKDB ---
@st.cache_resource
def get_db_connection():
  token = get_secret("MOTHERDUCK_TOKEN")
  
  if token:
      conn = duckdb.connect(f"md:streaming_db?motherduck_token={token}")
  else:
      conn = duckdb.connect("dev.duckdb")
  return conn

try:
    conn = get_db_connection()
except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")
    st.stop()

# --- 2. CARGA DE DATOS DESDE LOS MARTS DE DBT ---
@st.cache_data(ttl=600)
def load_data():
    df_state = conn.query("SELECT * FROM gold.mart_churn_by_state").df()
    df_support = conn.query("SELECT * FROM gold.mart_support_calls_impact").df()
    return df_state, df_support

df_state, df_support = load_data()

# --- 3. ENCABEZADO Y KPIS PRINCIPALES ---
st.title("📊 SaaS Churn Analytics & AI Executive Copilot")
st.markdown("Pipeline analítico sobre **DuckDB + dbt + MotherDuck**, potenciado con IA para detección de riesgo de Churn.")

total_subs = int(df_state['total_subscription'].sum())
total_churned = int(df_state['churned_subscriptions'].sum())
overall_churn_rate = round((total_churned / total_subs) * 100, 2) if total_subs > 0 else 0
total_revenue = round(df_state['total_revenue_usd'].sum(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Suscripciones Totales", f"{total_subs:,}")
col2.metric("Suscripciones Canceladas", f"{total_churned:,}")
col3.metric("Tasa Global de Churn", f"{overall_churn_rate}%")
col4.metric("Ingreso Anual Total", f"${total_revenue:,.2f}")

st.divider()

# --- 4. VISUALIZACIONES INTERACTIVAS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📉 Impacto de Llamadas a Soporte en el Churn")
    fig_support = px.bar(
        df_support,
        x="number_of_support_calls",
        y="churn_rate_pct",
        text="churn_rate_pct",
        labels={"number_of_support_calls": "Llamadas a Soporte", "churn_rate_pct": "% Churn"},
        color="churn_rate_pct",
        color_continuous_scale=[[0, '#FFC2C2'], [1, '#E60000']]
    )

    fig_support.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(color='#000000', size=11, family="Arial Black")
    )
 
    fig_support.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', size=11),
        xaxis=dict(title_font=dict(color='#000000', size=11), tickfont=dict(color='#000000', size=11)),
        yaxis=dict(title_font=dict(color='#000000', size=11), tickfont=dict(color='#000000', size=11))
    )
    st.plotly_chart(fig_support, use_container_width=True)

with col_right:
    st.subheader("🗺️ Tasa de Churn por Estado Top 10")
    top_states = df_state.head(10)
    fig_state = px.bar(
        top_states,
        x="state_code",
        y="churn_rate_pct",
        text="churn_rate_pct",
        labels={"state_code": "Estado", "churn_rate_pct": "% Churn"},
        color="churn_rate_pct",
        color_continuous_scale=[[0, '#E0F7FA'], [1, '#00B4D8']]
    )
  
    fig_state.update_traces(
        texttemplate='%{text:.1f}%', 
        textposition='outside',
        textfont=dict(color='#000000', size=11, family="Arial Black")
    )

    fig_state.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', size=11),
        xaxis=dict(title_font=dict(color='#000000', size=11), tickfont=dict(color='#000000', size=11)),
        yaxis=dict(title_font=dict(color='#000000', size=11), tickfont=dict(color='#000000', size=11))
    )
    st.plotly_chart(fig_state, use_container_width=True)

# --- 5. AI COPILOT: RESUMEN EJECUTIVO CON LLM ---
st.subheader("💻 AI Executive Insights Copilot")
st.write("Genera un análisis estratégico en tiempo real basado en los datos procesados en la capa Gold.")

if st.button("🚀 Generar Resumen Ejecutivo con IA"):
    groq_api_key = get_secret("GROQ_API_KEY")
    
    if not groq_api_key:
        st.warning("⚠️ No se encontró la `GROQ_API_KEY`. Agrégala a tu archivo .env para habilitar la IA.")
    else:
        with st.spinner("La IA está analizando los patrones de churn en DuckDB..."):
            try:
                client = Groq(api_key=groq_api_key)
                
                prompt_data = df_support.to_string(index=False)
                
                system_prompt = (
                    "Sos un Chief Analytics Officer y experto en retención para plataformas SaaS."
                    "Analizá los siguientes datos procesados de llamadas a soporte y su tasa de churn."
                    "Proporcioná un informe ejecutivo claro con 3 puntos clave y 1 recomendación accionable de negocio."
                )
                
                user_prompt = f"Datos del Data Warehouse (Marts):\n\n{prompt_data}"
                
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3
                )
                
                st.success("Analysis Completed!")
                st.markdown("### 📋 Resumen Ejecutivo de la IA")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error al llamar a la API de la IA: {e}")


# --- DISEÑO EXTRA ---
st.markdown("""
    <style>
    /* Fondo blanco general */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }

    /* ESTILO PARA EL BOTÓN DE LA IA (Destacado) */
    div.stButton > button {
        background-color: #E60000 !important;
        color: #FFFFFF !important;
        border: 2px solid #B30000 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        padding: 10px 24px !important;
        box-shadow: 0px 4px 10px rgba(230, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    /* Efecto al pasar el cursor sobre el botón */
    div.stButton > button:hover {
        background-color: #CC0000 !important;
        color: #FFFFFF !important;
        border-color: #880000 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 14px rgba(204, 0, 0, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)