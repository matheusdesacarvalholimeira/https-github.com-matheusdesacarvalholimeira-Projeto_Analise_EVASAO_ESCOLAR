import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# ===================== LEITURA DOS DADOS ===================== #
evasao = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\evasao_historica.csv')
ideb = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\indicadores_educacionais.csv')
infra = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\infraestrutura_escolar_simulada.csv')
renda = pd.read_csv(r'C:\Users\User\Documents\projeto_eva\Projeto_Analise_EVAS-O_ESCOLAR\projeto_pyspark\data\predic\renda_media_regiao.csv')

fatores = pd.DataFrame({
    'Fator': ['Renda', 'Infraestrutura', 'IDEB', 'Desemprego', 'Inflação'],
    'Importancia': [0.35, 0.25, 0.20, 0.15, 0.05]
})

escolas_risco = pd.DataFrame({
    'Escola': ['Escola A', 'Escola B', 'Escola C'],
    'Latitude': [-23.55, -22.90, -19.92],
    'Longitude': [-46.63, -43.20, -43.94],
    'Risco_Evasao': [0.8, 0.6, 0.9]
})

economia = pd.DataFrame({
    'Ano': [2020, 2021, 2022],
    'Desemprego': [14.1, 13.2, 11.0],
    'Inflacao': [4.5, 10.1, 5.8],
    'PIB': [1.1, 4.6, 2.9]
})

evasao.columns = ['Ano', 'Dependencia', 'Taxa']
ideb.columns = ['UF', 'Cod_Mun', 'Municipio', 'Rede', 'IDEB']
infra.columns = ['Matriculados_1S', 'Mensalidade_OK', 'Bolsistas']
renda.columns = ['Ano', 'Regiao', 'Renda']

# ========== DASH APP ==========
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Painel Educacional e Socioeconômico", style={'textAlign': 'center'}),

    dcc.Graph(
        figure=px.line(evasao, x='Ano', y='Taxa', color='Dependencia',
                       title="Taxa de Evasão por Rede")
    ),

    dcc.Graph(
        figure=px.bar(ideb.dropna(), x='Municipio', y='IDEB', color='Rede',
                      title="IDEB por Município")
    ),

    dcc.Graph(
        figure=px.line(renda, x='Ano', y='Renda', color='Regiao',
                       title="Renda Média por Região")
    ),

    dcc.Graph(
        figure=px.line(economia, x='Ano', y=['Desemprego', 'Inflacao', 'PIB'],
                       title="Indicadores Econômicos")
    ),

    dcc.Graph(
        figure=px.bar(infra.sum().reset_index(), x='index', y=0,
                      labels={'index': 'Indicador', 0: 'Total'},
                      title="Infraestrutura Escolar")
    ),

    html.H2("Mapa de Escolas por Risco de Evasão"),
    dcc.Graph(
        figure=px.scatter_mapbox(
            escolas_risco,
            lat="Latitude",
            lon="Longitude",
            color="Risco_Evasao",
            size="Risco_Evasao",
            hover_name="Escola",
            color_continuous_scale=px.colors.sequential.Reds,
            zoom=4
        ).update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    ),

    html.H2("Ranking de Fatores mais Influentes"),
    dcc.Graph(
        figure=px.bar(fatores.sort_values('Importancia'), x='Importancia', y='Fator', orientation='h',
                      title="Importância dos Fatores na Evasão")
    ),

    html.H2("Comparativo Público vs Privado"),
    dcc.Graph(
        figure=px.box(evasao, x='Dependencia', y='Taxa',
                      title="Taxa de Evasão por Rede")
    ),

    html.H2("Simulador de Cenários"),
    html.Label("Inflação Simulada (%)"),
    dcc.Slider(id='slider-inflacao', min=0, max=20, step=0.5, value=5,
               marks={i: f"{i}%" for i in range(0, 21, 5)}),

    html.Label("Desemprego Simulado (%)"),
    dcc.Slider(id='slider-desemprego', min=0, max=20, step=0.5, value=10,
               marks={i: f"{i}%" for i in range(0, 21, 5)}),

    dcc.Graph(id='grafico-simulador')
])

@app.callback(
    Output('grafico-simulador', 'figure'),
    Input('slider-inflacao', 'value'),
    Input('slider-desemprego', 'value')
)
def simular_evasao(inflacao, desemprego):
    evasao_estimada = 0.1 * inflacao + 0.2 * desemprego
    df_sim = pd.DataFrame({
        'Fator': ['Inflação', 'Desemprego', 'Evasão Estimada'],
        'Valor': [inflacao, desemprego, evasao_estimada]
    })
    return px.bar(df_sim, x='Fator', y='Valor', title="Simulação de Evasão")

# ========== EXECUTAR ==========
if __name__ == '__main__':
    app.run(debug=True)