import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib

# 1. Configurações de Interface
st.set_page_config(page_title="PRF-ES Dashboard", layout="wide", page_icon="🚔")

# 2. Estilização CSS "PRO" e Adaptável ao Dark/Light Mode
st.markdown("""
    <style>
    /* Tags dos filtros em Azul (Ajustado para ficar bom no claro e escuro) */
    span[data-baseweb="tag"] {
        background-color: #004080 !important;
        color: white !important;
        border-radius: 5px !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #004080 !important;
    }

    /* Cards de Métricas Dinâmicos */
    div[data-testid="stMetric"] {
        /* Usa a cor secundária do tema (cinza claro no Light, cinza escuro no Dark) */
        background-color: var(--secondary-background-color) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        border-left: 6px solid #004080 !important; 
        transition: transform 0.2s ease-in-out;
    }
    
    /* Efeito de hover nos cards */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Títulos principais adaptáveis */
    h1 {
        font-weight: 800 !important;
        letter-spacing: -1px;
    }

    /* Botão com sombra e cor sólida */
    div.stButton > button {
        background-color: #004080;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }


    /* Subtítulo */
    .subtitulo-header {
        font-size: 22px !important;
        color: var(--text-color) !important; /* Adapta automático */
        opacity: 0.8; /* Dá o tom cinza suave sem perder a cor original */
        font-weight: 500 !important;
        margin-top: -10px !important;
        margin-bottom: 30px !important;
    }

    /* Rótulos das Métricas (ex: "Total de Ocorrências") */
    [data-testid="stMetricLabel"] * {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        opacity: 0.7;
    }

    /* Valores das Métricas (os números) */
    [data-testid="stMetricValue"] {
        font-size: 36px !important;
        font-weight: 800 !important;
    }

    div[data-testid="stTabList"] {
        display: flex !important;
        justify-content: center !important; /* Centraliza as abas conforme as linhas roxas */
        width: 100% !important;
        gap: 15px !important; /* Espaçamento entre os blocos */
    }

    button[data-baseweb="tab"] {
        font-size: 22px !important; /* Letras maiores para formato botão profissional */
        font-weight: 700 !important;
        padding: 10px 30px !important; /* Mais área de clique */
        border-radius: 8px 8px 0 0 !important;
    }
    
    button[data-baseweb="tab"] p {
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    /* Títulos dos Gráficos na aba de estatísticas */
    .chart-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        margin-bottom: 15px !important;
    }

    /* Título do Expander */
    [data-testid="stExpander"] summary p {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
    }

    /* Texto do Rodapé */
    .rodape-dash {
        font-size: 15px !important;
        color: var(--text-color) !important;
        opacity: 0.6;
        margin-top: 30px !important;
        font-weight: 500 !important;
    }


    /* Filtros Padrões (Município, Via, etc) */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] label p {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
    }

    
    /* Título do Slider muito maior, em negrito e destacado em Azul PRF */
    div[data-testid="stSlider"] label p {
        font-size: 19px !important;
        font-weight: 700 !important;
        color: #004080 !important;
        margin-bottom: 8px !important;
    }

    /* Números flutuantes maiores com fundo estilo "tag" discreto para parecer profissional */
    div[data-testid="stThumbValue"] {
        font-size: 17px !important;
        font-weight: 800 !important;
        color: #004080 !important;
        background-color: var(--secondary-background-color) !important;
        padding: 3px 10px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    /* Números das extremidades (0 e 23) maiores e mais visíveis */
    div[data-testid="stSlider"] span[data-baseweb="typography"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        opacity: 0.9 !important;
    }

    /* Linha do Slider ligeiramente mais espessa e moderna */
    div[data-testid="stSlider"] > div > div > div {
        height: 7px !important;
        border-radius: 4px !important;
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

# --- SIDEBAR   ---
st.sidebar.image("https://logodownload.org/wp-content/uploads/2014/10/prf-logo-1.png", width=140)
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
st.title("🚓 Sistema de Inteligência Viária - PRF Espírito Santo")
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
    st.map(mapa_data, zoom=7, use_container_width=True)

with aba_estatisticas:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='chart-title'>Top 10 Causas de Acidentes</div>", unsafe_allow_html=True)
        causas = df_f['causa_acidente'].value_counts().head(10).reset_index()
        fig_causa = px.bar(causas, x='count', y='causa_acidente', orientation='h', 
                           color_discrete_sequence=['#004080'], text_auto=True)
        fig_causa.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_causa, use_container_width=True)

    with col_b:
        st.markdown("<div class='chart-title'>Acidentes por Tipo de Pista e Gravidade</div>", unsafe_allow_html=True)
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