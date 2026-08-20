import os
import duckdb
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_secret(key_name: str, default_value: str = "") -> str:
    val = os.getenv(key_name)
    if val is not None:
        return val
    if default_value == "":
        st.warning(f"Variable '{key_name} is not defined in the env. It will return an empty string.")
    else:
        st.info(f"Variable '{key_name}' not defined. Using default value: '{default_value}'")
        return default_value

load_dotenv()

st.set_page_config(
    page_title="SaaS Churn Analytics & AI Insights",
    page_icon="📊",
    layout="wide"
)

# ——— 1. DATABASE CONNECTION.
@st.cache_resource
def get_db_connection():
    token = get_secret("MOTHERDUCK_TOKEN")
    
    if token:
        conn = duckdb.connect(f"md:streaming_db?motherduck_token={token}")
        try:
            conn.execute("USE streaming_db;")
        except Exception:
            pass
    else:
        conn = duckdb.connect("dev.duckdb")
    return conn

try:
    conn = get_db_connection()
except Exception as e:
    st.error(f"Error connecting to the database: {e}")
    st.stop()


# ——— 2. DATA LOADING FROM DBT MARTS.
@st.cache_data(ttl=600)
def load_data():
    df_state = conn.query("SELECT * FROM gold.mart_churn_by_state").df()
    df_support = conn.query("SELECT * FROM gold.mart_support_calls_impact").df()
    return df_state, df_support

df_state, df_support = load_data()


# ——— 3. HEADER & KPIs.
st.title("📊 SaaS Churn Analytics & AI Executive Copilot")
st.markdown("End-to-end Analytics Pipeline built on **DuckDB + dbt + MotherDuck**, powered by AI for Churn Risk Detection.")

total_subs = int(df_state['total_subscriptions'].sum())
total_churned = int(df_state['churned_subscriptions'].sum())
overall_churn_rate = round((total_churned / total_subs) * 100, 2) if total_subs > 0 else 0
total_revenue = round(df_state['total_revenue_usd'].sum(), 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Subscriptions", f"{total_subs:,}")
col2.metric("Churned Subscriptions", f"{total_churned:,}")
col3.metric("Overall Churn Rate", f"{overall_churn_rate}%")
col4.metric("Total Annual Revenue", f"${total_revenue:,.2f}")

st.divider()


# ——— 4. INTERACTIVE VISUALIZATIONS.
df_support['churn_rate_pct'] = df_support['churn_rate_pct'].astype(float)
df_state['churn_rate_pct'] = df_state['churn_rate_pct'].astype(float)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🟥 Customer Support Calls vs. Churn Rate")
    fig_support = px.bar(
        df_support,
        x="number_of_support_calls",
        y="churn_rate_pct",
        labels={"number_of_support_calls": "Support Calls Count", "churn_rate_pct": "Churn Rate (%)"},
        color="churn_rate_pct",
        color_continuous_scale=[[0, '#FFC2C2'], [1, '#E60000']]
    )

    fig_support.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='outside',
        textfont=dict(color='#000000', size=11, family="Arial Black")
    )
 
    fig_support.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', size=11)
    )
    st.plotly_chart(fig_support, use_container_width=True)

with col_right:
    st.subheader("🟦 Churn Rate by Top 10 US States")
    top_states = df_state.head(10)
    fig_state = px.bar(
        top_states,
        x="state_code",
        y="churn_rate_pct",
        labels={"state_code": "State Code", "churn_rate_pct": "Churn Rate (%)"},
        color="churn_rate_pct",
        color_continuous_scale=[[0, '#E0F7FA'], [1, '#00B4D8']]
    )
  
    fig_state.update_traces(
        texttemplate='%{y:.1f}%',
        textposition='outside',
        textfont=dict(color='#000000', size=11, family="Arial Black")
    )

    fig_state.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#000000', size=11)
    )
    st.plotly_chart(fig_state, use_container_width=True)


# ——— 5. AI COPILOT: LLM EXECUTIVE INSIGHTS.
st.subheader("💻 AI Executive Insights Copilot")
st.write("Generates real-time strategic analysis based on data processed in the Gold layer.")

if st.button("🚀 Generate AI Executive Summary"):
    gemini_api_key = get_secret("GEMINI_API_KEY")
    
    if not gemini_api_key:
        st.warning("`GEMINI_API_KEY` not found. Please add it to your environment variables/secrets to enable AI.")
    else:
        with st.spinner("AI is analyzing churn patterns using Gemini, please wait a minute..."):
            try:
                client = genai.Client(api_key=gemini_api_key)
                
                prompt_data = f"Churn by State:\n{df_state.to_string(index=False)}\n\nSupport Calls Impact:\n{df_support.to_string(index=False)}"
                
                system_prompt = (
                    "You are a Chief Analytics Officer and SaaS customer retention expert. "
                    "Analyze the following processed support calls and churn rate data from the Gold Marts. "
                    "Provide a concise executive report with 3 key insights and 1 actionable business recommendation."
                )
                
                user_prompt = f"Data Warehouse Marts:\n\n{prompt_data}"
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.3
                    )
                )
                
                st.success("Analysis Completed!")
                st.markdown("### 📋 AI Executive Summary")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error calling AI API: {e}")


# Custom css
st.markdown("""
    <style>
    /* White background */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }

    /* Highlighted AI Button Style */
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

    /* Hover effect for button */
    div.stButton > button:hover {
        background-color: #CC0000 !important;
        color: #FFFFFF !important;
        border-color: #880000 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 14px rgba(204, 0, 0, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)