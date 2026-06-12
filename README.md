# Projeto-Integrador-III - Risco-de-Acidentes-PRF-ES

Este projeto (Projeto Integrador III) visa analisar dados abertos da Polícia Rodoviária Federal referentes a acidentes no estado do Espírito Santo. O foco é identificar os principais causadores de acidentes, rodovias mais perigosas e implementar um modelo de Machine Learning capaz de prever se um acidente tem probabilidade de ser grave/fatal dadas certas condições de via e clima.

## 🎥 Demonstração do Projeto

Sistema desenvolvido para análise de acidentes da PRF no Espírito Santo.

[🔗 Assista a demonstração no YouTube](https://www.youtube.com/watch?v=GtDiVeV_Ixs)

## Funcionalidades
- **Filtros Dinâmicos:** Filtre os dados do painel por Município, Rodovia, Condição Climática, Tipo de Pista e Faixa Horária.
- **Exportação de Dados:** Possibilidade de baixar um arquivo `.csv` apenas com os dados filtrados diretamente pela barra lateral da interface.
- **Métricas em Tempo Real (KPIs):** Visualização rápida através de cards informativos do Total de Ocorrências, Vítimas Fatais, Acidentes Graves e Índice de Letalidade.
- **Mapa de Calor Geográfico:** Concentração interativa de ocorrências no ES utilizando geolocalização (Lat/Lon).
- **Análise Estatística Avançada:** Gráficos interativos (Plotly) para Top 10 Causas de Acidentes.
- **Simulador de Risco de Acidentes (IA):** Integração de um modelo preditivo (Random Forest balanceado) para classificar o nível de risco e a probabilidade de gravidade do acidente com base na entrada do utilizador.
- **Transparência da IA (Explainable AI):** Gráfico interativo de *Feature Importance* que demonstra claramente quais fatores (clima, pista, causa, hora) mais influenciam as decisões preditivas do modelo de Machine Learning.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Manipulação de Dados:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (Random Forest), XGBoost, Joblib
- **Visualização de Dados:** Plotly (Gráficos Interativos), Matplotlib, Seaborn
- **Aplicação Web:** Streamlit, HTML/CSS customizado

## Estrutura do Repositório
- `/app`: Código fonte principal do Dashboard Streamlit (`app.py`).
- `/data`: Contém as bases de dados brutas e limpas (`prf_es_clean.csv`).
- `/models`: Modelos de classificação exportados (`modelo_risco_acidente.pkl`) e mapeamento de variáveis de treino (`colunas_treino.pkl`).
- `/notebooks`: Notebooks Jupyter com a Análise Exploratória (`02_eda.ipynb`) e treino/validação dos modelos Random Forest e XGBoost (`03_modelagem.ipynb`).

## Como executar o projeto

Clone o repositório
```bash
  git clone https://github.com/josueespadarotte Projeto-Integrador-III---Risco-de-Acidentes-PRF-ES
```
Acesse o diretório do projeto

```bash
  cd Projeto-Integrador-III---Risco-de-Acidentes-PRF-ES
```

Crie um ambiente virtual
```bash
python -m venv venv
```
Ative o ambiente virtual
```bash
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows
```

Instale as dependências
```bash
 pip install -r requirements.txt
```

Execute a aplicação Streamlit
```bash
 streamlit run app/app.py
```

## Acessar a Aplicação
http://localhost:8501

## Alunos

- Anna Luiza Tamanini
- Josué Espadarotte
- Laisa de Sousa Camilo
- Mikaelly Cardoso
- Victória Sofia S Teixeira
