# Projeto-Integrador-III - Risco-de-Acidentes-PRF-ES

Este projeto (Projeto Integrador III) visa analisar dados abertos da Polícia Rodoviária Federal referentes a acidentes no estado do Espírito Santo. O foco é identificar os principais causadores de acidentes, rodovias mais perigosas e implementar um modelo de Machine Learning capaz de prever se um acidente tem probabilidade de ser grave/fatal dadas certas condições de via e clima.

## 🎥 Demonstração do Projeto

Sistema desenvolvido para análise de acidentes da PRF no Espírito Santo.

[🔗 Assista a demonstração no YouTube:](https://youtu.be/7HDAW45lSng)

## Funcionalidades
- **Análise Estatística e EDA:** Identificação de horários de pico, tipos de pista mais propensos a acidentes e top causas.
- **Mapa de Calor:** Concentração geográfica de ocorrências no ES.
- **Simulador de Risco de Acidentes (IA):** Integração de um modelo preditivo (Random Forest) para classificar o risco do acidente com base na condição climática e do tipo de via.

## Tecnologias Utilizadas
- **Linguagem:** Python
- **Manipulação de Dados:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn (Random Forest), XGBoost, Joblib
- **Visualização:** Matplotlib, Seaborn, Plotly
- **Aplicação Web:** Streamlit

## Estrutura do Repositório
- `/data`: Contém as bases de dados brutas e limpas (`prf_es_clean.csv`).
- `/notebooks`: Notebooks Jupyter com a Análise Exploratória (`02_eda.ipynb`) e treinamento dos modelos (`03_modelagem.ipynb`).
- `/models`: Modelos exportados e variáveis de treino (`.pkl`).
- `/app`: Código fonte do Dashboard Streamlit (`app.py`).

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
