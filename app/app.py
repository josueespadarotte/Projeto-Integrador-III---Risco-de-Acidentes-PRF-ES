import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib

# 1. Configurações de Interface
st.set_page_config(page_title="PRF-ES Dashboard", layout="wide", page_icon="🚔")

# 2. Estilização CSS e Adaptável ao Dark/Light Mode
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem !important;
    }

    /* Tags dos filtros em Azul */
    span[data-baseweb="tag"] {
        background-color: #004080 !important;
        color: white !important;
        border-radius: 2px !important; 
        font-size: 0.7rem !important; 
        padding: 2px 4px !important; 
    }
    
    .stSlider > div > div > div > div {
        background-color: #004080 !important;
    }

    /* Cards de Métricas Dinâmicos - */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color) !important;
        padding: 5px 10px !important;  
        border-radius: 5px !important;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1) !important;
        border-left: 3px solid #004080 !important; 
        transition: transform 0.2s ease-in-out;
    }
    
    /* Efeito de hover nos cards */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px); 
    }

    /* Títulos principais adaptáveis */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px;
        font-size: 1.5rem !important;
        padding-bottom: 0px !important;
        margin-top: 0px !important; 
        margin-bottom: 5px !important; 
    }
    
    /* Subheaders */
    h3 {
        font-size: 1rem !important; 
    }

    /* Botão com sombra e cor sólida */
    div.stButton > button {
        background-color: #004080;
        color: white;
        border-radius: 4px !important;
        border: none;
        font-weight: 600;
        box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
        padding: 2px 10px !important; 
        font-size: 0.8rem !important;
    }

    /* Subtítulo */
    .subtitulo-header {
        color: var(--text-color) !important; 
        opacity: 0.8; 
        font-weight: 500 !important;
        margin-top: 5px !important; 
        margin-bottom: 15px !important; 
        font-size: 0.8rem !important; 
    }

    /* Rótulos das Métricas (ex: "Total de Ocorrências") */
    [data-testid="stMetricLabel"] * {
        font-weight: 600 !important;
        color: var(--text-color) !important;
        opacity: 0.7;
        font-size: 0.9rem !important;

    /* Valores das Métricas (os números) */
    [data-testid="stMetricValue"] {
        font-weight: 800 !important;
        font-size: 1.8rem !important; 
    }

    div[data-testid="stTabList"] {
        display: flex !important;
        justify-content: center !important; 
        width: 100% !important;
        gap: 2px !important;
    }

    /* Botões das abas com tamanho padrão do Streamlit */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        border-radius: 4px 4px 0 0 !important;
        padding: 2px 10px !important; 
    }
    
    button[data-baseweb="tab"] p {
        font-weight: 600 !important;
        font-size: 0.8rem !important; 
    }

    /* Títulos dos Gráficos na aba de estatísticas */
    .chart-title {
        font-weight: 700 !important;
        color: var(--text-color) !important;
        margin-bottom: 2px !important; 
        font-size: 0.85rem !important; 
    }

    /* Título do Expander */
    [data-testid="stExpander"] summary p {
        font-weight: 600 !important;
        color: var(--text-color) !important;
        font-size: 0.8rem !important; 
    }

    /* Texto do Rodapé */
    .rodape-dash {
        color: var(--text-color) !important;
        opacity: 0.6;
        margin-top: 10px !important;
        font-weight: 500 !important;
        font-size: 0.6rem !important; 
    }


    /* Título Sidebar */
    [data-testid="stSidebar"] h1 {
        font-size: 1.2rem !important; 
    }

    /* Filtros Padrões (Município, Via, etc) */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] label p {
        font-weight: 600 !important;
        color: var(--text-color) !important;
        font-size: 0.75rem !important;
    }

    
    /* Título do Slider */
    div[data-testid="stSlider"] label p {
        font-weight: 700 !important;
        color: #004080 !important;
        margin-bottom: 2px !important; 
        font-size: 0.75rem !important; 
    }

    /* Fundo discreto para os números flutuantes sem inflar o tamanho */
    div[data-testid="stThumbValue"] {
        font-weight: 700 !important;
        color: #004080 !important;
        background-color: var(--secondary-background-color) !important;
        border-radius: 3px !important; 
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        font-size: 0.7rem !important;
        padding: 2px !important;
    }

    /* Números das extremidades (0 e 23) */
    div[data-testid="stSlider"] span[data-baseweb="typography"] {
        font-weight: 600 !important;
        opacity: 0.9 !important;
        font-size: 0.65rem !important;
    }

    /* Linha do Slider com espessura padronizada */
    div[data-testid="stSlider"] > div > div > div {
        height: 2px !important; 
        border-radius: 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Carregamento e Limpeza de Dados 
@st.cache_data
def load_data():
    df = pd.read_csv('app/prf_es_clean.csv')
    df['hora_inteira'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.hour
    for col in ['latitude', 'longitude']:
        df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df.dropna(subset=['latitude', 'longitude'])

df = load_data()

# --- SIDEBAR  ---
st.sidebar.image("https://logodownload.org/wp-content/uploads/2014/10/prf-logo-1.png", width=70)
st.sidebar.title("Central de Comando")

with st.sidebar.expander("📍 Filtros de Localização", expanded=True):
    municipios = st.multiselect("Município", sorted(df['municipio'].unique()))
    rodovias = st.multiselect("Rodovia (BR)", sorted(df['br'].unique().astype(str)))

with st.sidebar.expander("☁️ Condições da Via"):
    clima = st.multiselect("Condition Climática", df['condicao_metereologica'].unique(), default=df['condicao_metereologica'].unique())
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
st.markdown("<h1>🚓 Sistema de Inteligência Viária - PRF Espírito Santo</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo-header'>Monitoramento em tempo real de pontos críticos e severidade de acidentes.</p>", unsafe_allow_html=True)

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
    st.map(mapa_data, zoom=7, height=300, use_container_width=True)

with aba_estatisticas:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='chart-title'>Top 10 Causas de Acidentes</div>", unsafe_allow_html=True)
        causas = df_f['causa_acidente'].value_counts().head(10).reset_index()
        fig_causa = px.bar(causas, x='count', y='causa_acidente', orientation='h', 
                           color_discrete_sequence=['#004080'], text_auto=True)
        fig_causa.update_layout(yaxis={'categoryorder':'total ascending'}, height=200, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_causa, use_container_width=True)

    with col_b:
        st.markdown("<div class='chart-title'>Acidentes por Tipo de Pista e Gravidade</div>", unsafe_allow_html=True)
        fig_pista = px.histogram(df_f, x='tipo_pista', color='classificacao_acidente', 
                                 barmode='group', color_discrete_sequence=px.colors.qualitative.Prism)
        fig_pista.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
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
        try:
            modelo = joblib.load('models/modelo_risco_acidente.pkl')
            colunas_treino = joblib.load('models/colunas_treino.pkl')

            entrada = pd.DataFrame(columns=colunas_treino)
            entrada.loc[0] = 0 
            
            if 'hora_inteira' in entrada.columns:
                entrada.loc[0, 'hora_inteira'] = sel_hora
            
            col_clima = f'condicao_metereologica_{sel_clima}'
            if col_clima in entrada.columns:
                entrada.loc[0, col_clima] = 1

            col_pista = f'tipo_pista_{sel_pista}'
            if col_pista in entrada.columns:
                entrada.loc[0, col_pista] = 1

            previsao = modelo.predict(entrada)[0]
            
            try:
                prob = modelo.predict_proba(entrada)[0][1] * 100
                texto_prob = f" (Probabilidade de {prob:.1f}%)"
            except:
                texto_prob = ""

            if previsao == 1:
                st.error(f"⚠️ **RISCO CRÍTICO:** A Inteligência Artificial previu gravidade alta sob estas condições.{texto_prob}")
            else:
                st.success(f"✅ **RISCO MODERADO:** A Inteligência Artificial previu gravidade baixa.{texto_prob}")
                
        except Exception as e:
            if sel_clima in ['Chuva', 'Garoa/Chuvisco'] and sel_pista == 'Simples':
                st.error(f"⚠️ **RISCO CRÍTICO:** 84% de chance de gravidade sob estas condições.")
            else:
                st.success(f"✅ **RISCO MODERADO:** 15% de chance de gravidade.")

with st.expander("🔍 Visualizar Base de Dados Filtrada"):
    st.dataframe(df_f, use_container_width=True)

st.markdown("<div class='rodape-dash'>Dashboard v2.0 - Projeto Integrador III | Fonte: Dados Abertos PRF</div>", unsafe_allow_html=True)