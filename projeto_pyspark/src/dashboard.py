import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Diretório base dos arquivos (não está sendo usado aqui, mas pode ajudar a organizar)
DATA_DIR = './data'

# ===================== LEITURA DOS DADOS ===================== #
evasao = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\evasao_historica.csv')
ideb = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\indicadores_educacionais.csv')
infra = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\infraestrutura_escolar_simulada.csv')
renda = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\renda_media_regiao.csv')

# Como o dataframe 'economia' não foi carregado, vamos criar um exemplo
economia = pd.DataFrame({
    'Ano': [2020, 2021, 2022],
    'Desemprego': [14.1, 13.2, 11.0],
    'Inflacao': [4.5, 10.1, 5.8],
    'PIB': [1.1, 4.6, 2.9]
})

# ===================== LIMPEZA BÁSICA ===================== #
evasao.columns = ['Ano', 'Dependencia', 'Taxa']
ideb.columns = ['UF', 'Cod_Mun', 'Municipio', 'Rede', 'IDEB']
infra.columns = ['Matriculados_1S', 'Mensalidade_OK', 'Bolsistas']
renda.columns = ['Ano', 'Regiao', 'Renda']

# ===================== APP DASH ===================== #
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Painel Educacional e Socioeconômico", style={'textAlign': 'center'}),

    dcc.Graph(
        figure=px.line(
            evasao.sort_values('Ano'),
            x='Ano', y='Taxa', color='Dependencia',
            title="Taxa de Evasão Escolar ao Longo dos Anos"
        )
    ),

    dcc.Graph(
        figure=px.bar(
            ideb.dropna(subset=['IDEB']),
            x='Municipio', y='IDEB', color='Rede',
            title="IDEB por Município"
        )
    ),

    dcc.Graph(
        figure=px.line(
            renda.sort_values('Ano'),
            x='Ano', y='Renda', color='Regiao',
            title="Renda Média por Região"
        )
    ),

    dcc.Graph(
        figure=px.line(
            economia,
            x='Ano',
            y=['Desemprego', 'Inflacao', 'PIB'],
            title="Indicadores Econômicos"
        )
    ),

    dcc.Graph(
        figure=px.bar(
            infra.sum().reset_index(),
            x='index', y=0,
            labels={'index': 'Indicador', 0: 'Total'},
            title="Infraestrutura Escolar (Simples)"
        )
    )
])

if __name__ == '__main__':
    app.run(debug=True)
