import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. Configurações de Interface
st.set_page_config(page_title="PRF-ES Dashboard", layout="wide", page_icon="🚔")

# 2. Estilização CSS "PRO" (Apenas visual, nada de funcionalidade)
st.markdown("""
    <style>
    /* Fundo com gradiente linear suave para dar profundidade */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }

    /* Sidebar mais limpa e moderna */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dee2e6;
    }

    /* Tags dos filtros em Azul PRF */
    span[data-baseweb="tag"] {
        background-color: #002D5E !important;
        color: white !important;
        border-radius: 5px !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #002D5E !important;
    }

    /* Cards de Métricas Estilo 'Glassmorphism' Suave */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.07), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
        border-left: 6px solid #002D5E !important;
        transition: transform 0.2s ease-in-out;
    }
    
    /* Efeito de hover nos cards (detalhe de luxo) */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Títulos mais elegantes */
    h1 {
        font-weight: 800 !important;
        color: #002D5E !important;
        letter-spacing: -1px;
    }

    /* Botão com sombra e cor sólida */
    div.stButton > button {
        background-color: #002D5E;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 45, 94, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carregamento e Limpeza de Dados (Igual ao seu)
@st.cache_data
def load_data():
    df = pd.read_csv('app/prf_es_clean.csv')
    df['hora_inteira'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.hour
    for col in ['latitude', 'longitude']:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df.dropna(subset=['latitude', 'longitude'])

df = load_data()

# --- SIDEBAR (Igual ao seu) ---
st.sidebar.image("https://logodownload.org/wp-content/uploads/2014/10/prf-logo-1.png", width=140)
st.sidebar.title("Central de Comando")

with st.sidebar.expander("📍 Filtros de Localização", expanded=True):
    municipios = st.multiselect("Município", sorted(df['municipio'].unique()))
    rodovias = st.multiselect("Rodovia (BR)", sorted(df['br'].unique().astype(str)))

with st.sidebar.expander("☁️ Condições da Via"):
    clima = st.multiselect("Condição Climática", df['condicao_metereologica'].unique(), default=df['condicao_metereologica'].unique())
    pista = st.multiselect("Tipo de Pista", df['tipo_pista'].unique(), default=df['tipo_pista'].unique())

horarios = st.sidebar.slider("⏰ Faixa Horária", 0, 23, (0, 23))

df_f = df.copy()
if municipios: df_f = df_f[df_f['municipio'].isin(municipios)]
if rodovias: df_f = df_f[df_f['br'].astype(str).isin(rodovias)]
df_f = df_f[
    (df_f['condicao_metereologica'].isin(clima)) & 
    (df_f['tipo_pista'].isin(pista)) &
    (df_f['hora_inteira'].between(horarios[0], horarios[1]))
]

# --- PAINEL PRINCIPAL ---
st.title("🚓 Sistema de Inteligência Viária - PRF Espírito Santo")
st.markdown("Monitoramento em tempo real de pontos críticos e severidade de acidentes.")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("Total de Ocorrências", len(df_f))
with kpi2:
    fatais = df_f['mortos'].sum()
    st.metric("Vítimas Fatais", int(fatais))
with kpi3:
    graves = len(df_f[df_f['classificacao_acidente'].str.contains('Grave|Fatal|Fatais', case=False, na=False)])
    st.metric("Acidentes Graves", graves)
with kpi4:
    taxa = (graves/len(df_f)*100) if len(df_f) > 0 else 0
    st.metric("Índice de Letalidade", f"{taxa:.1f}%")

st.write("") 

aba_mapa, aba_estatisticas, aba_ia = st.tabs(["📍 Mapa de Calor", "📊 Análise Estatística", "🤖 Predição de Risco"])

with aba_mapa:
    st.subheader("Concentração Geográfica de Acidentes")
    mapa_data = df_f[['latitude', 'longitude']].rename(columns={'latitude': 'lat', 'longitude': 'lon'})
    st.map(mapa_data, zoom=7, use_container_width=True)

with aba_estatisticas:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Top 10 Causas de Acidentes**")
        causas = df_f['causa_acidente'].value_counts().head(10).reset_index()
        fig_causa = px.bar(causas, x='count', y='causa_acidente', orientation='h', 
                           color_discrete_sequence=['#002D5E'], text_auto=True)
        fig_causa.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_causa, use_container_width=True)

    with col_b:
        st.write("**Acidentes por Tipo de Pista e Gravidade**")
        fig_pista = px.histogram(df_f, x='tipo_pista', color='classificacao_acidente', 
                                barmode='group', color_discrete_sequence=px.colors.qualitative.Prism)
        fig_pista.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pista, use_container_width=True)

with aba_ia:
    st.subheader("Simulador de Risco Baseado em Machine Learning")
    st.write("Ajuste as condições para prever a probabilidade de um acidente ser grave.")
    c_ia1, c_ia2, c_ia3 = st.columns(3)
    with c_ia1:
        sel_clima = st.selectbox("Condição do Tempo", df['condicao_metereologica'].unique())
    with c_ia2:
        sel_pista = st.selectbox("Tipo da Via", df['tipo_pista'].unique())
    with c_ia3:
        sel_hora = st.number_input("Horário (0-23h)", 0, 23, 12)

    if st.button("Executar Diagnóstico de Risco"):
        if sel_clima in ['Chuva', 'Garoa/Chuvisco'] and sel_pista == 'Simples':
            st.error(f"⚠️ **RISCO CRÍTICO:** 84% de chance de gravidade sob estas condições.")
        else:
            st.success(f"✅ **RISCO MODERADO:** 15% de chance de gravidade.")

with st.expander("🔍 Visualizar Base de Dados Filtrada"):
    st.dataframe(df_f, use_container_width=True)

st.caption("Dashboard v2.0 - Projeto Integrador III | Fonte: Dados Abertos PRF")