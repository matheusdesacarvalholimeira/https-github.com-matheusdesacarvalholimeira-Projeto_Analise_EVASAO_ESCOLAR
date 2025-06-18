import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from dash import Dash, dcc, html, Input, Output

# ===================== LEITURA DOS DADOS ===================== #
evasao = pd.read_csv("https://avadashstorage.blob.core.windows.net/dadospy/evasao_historica.csv?sp=r&st=2025-06-17T21:43:44Z&se=2025-06-20T05:43:44Z&sv=2024-11-04&sr=b&sig=R6rC0PECyae9CHMlNSBe%2FWZvWJroC2%2BQRkNALbLk%2FYg%3D")
ideb = pd.read_csv("https://avadashstorage.blob.core.windows.net/dadospy/indicadores_educacionais.csv?sp=r&st=2025-06-17T21:45:26Z&se=2025-06-20T05:45:26Z&sv=2024-11-04&sr=b&sig=SeM7s%2FnIvoDWxso5L19jOqttVeCozFbD2Y8zbuf8yjs%3D")
infra = pd.read_csv("https://avadashstorage.blob.core.windows.net/dadospy/infraestrutura_escolar_simulada.csv?sp=r&st=2025-06-17T21:46:23Z&se=2025-06-20T05:46:23Z&sv=2024-11-04&sr=b&sig=CXeS5N0MXSq1dkgb4acZv0weTyMwgz14wmGg3NjVyCQ%3D")
renda = pd.read_csv("https://avadashstorage.blob.core.windows.net/dadospy/renda_media_regiao.csv?sp=r&st=2025-06-17T21:47:52Z&se=2025-06-20T05:47:52Z&sv=2024-11-04&sr=b&sig=OZAM7s2RxeJ3jsgAZwsedWvkPFddeSbJ3OQ3Ulib%2FxQ%3D")

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

# ===================== PREPARAR BASE PARA MODELO ===================== #
evasao.columns = ['Ano', 'Dependencia_Administrativa', 'Taxa_Abandono']
ideb.columns = ['UF', 'Cod_Mun', 'Municipio', 'Rede', 'IDEB']
infra.columns = ['Curricular units 1st sem (enrolled)', 'Tuition fees up to date', 'Scholarship holder']
renda.columns = ['Ano', 'Regiao', 'Renda_Media']

df_renda_brasil = renda[renda['Regiao'] == 'brasil'].drop(columns='Regiao')

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

ideb = ideb[ideb['IDEB'].apply(is_number)]
ideb['IDEB'] = ideb['IDEB'].astype(float)
ideb['Dependencia_Administrativa'] = ideb['Rede'].apply(
    lambda x: 'pública' if x in ['estadual', 'pública', 'municipal'] else 'privada')
ideb_por_rede = ideb.groupby('Dependencia_Administrativa')['IDEB'].mean().reset_index()
ideb_por_rede.rename(columns={'IDEB': 'IDEB_Medio'}, inplace=True)

df = evasao.merge(df_renda_brasil, on='Ano', how='left')
df = df.merge(ideb_por_rede, on='Dependencia_Administrativa', how='left')
infra_mean = infra.mean()
infra_data = pd.DataFrame([infra_mean.values] * len(df), columns=infra_mean.index)
df = pd.concat([df.reset_index(drop=True), infra_data.reset_index(drop=True)], axis=1)

le = LabelEncoder()
df['Dependencia_Administrativa'] = le.fit_transform(df['Dependencia_Administrativa'])

X = df.drop(columns=['Taxa_Abandono'])
y = df['Taxa_Abandono']
model = RandomForestRegressor(random_state=42)
model.fit(X, y)
df['Predito'] = model.predict(X)

anos_futuros = [2025, 2026, 2027]
previsoes_futuras = []
renda_atual = df['Renda_Media'].mean()
ideb_atual = df['IDEB_Medio'].mean()
dependencia = le.transform(['pública'])[0]

for i, ano in enumerate(anos_futuros, start=1):
    renda_future = renda_atual * (1 + 0.03 * i)
    ideb_future = ideb_atual + (0.2 * i)
    input_data = pd.DataFrame({
        'Ano': [ano],
        'Dependencia_Administrativa': [dependencia],
        'Renda_Media': [renda_future],
        'IDEB_Medio': [ideb_future],
        'Curricular units 1st sem (enrolled)': [infra_mean[0]],
        'Tuition fees up to date': [infra_mean[1]],
        'Scholarship holder': [infra_mean[2]]
    })
    pred = model.predict(input_data)[0]
    previsoes_futuras.append({'Ano': ano, 'Evasao_Prevista': pred})
df_futuro = pd.DataFrame(previsoes_futuras)

# ===================== ESTILIZAÇÃO ===================== #

TITLE_STYLE = {
    'textAlign': 'center',
    'color': '#2c3e50',
    'font-family': 'Arial, sans-serif',
    'margin-bottom': '30px'
}

SECTION_TITLE_STYLE = {
    'color': '#34495e',
    'font-family': 'Arial, sans-serif',
    'border-bottom': '2px solid #2980b9',
    'padding-bottom': '8px',
    'margin-top': '40px',
    'margin-bottom': '20px',
    'font-weight': 'bold',
    'font-size': '24px'
}

SLIDER_LABEL_STYLE = {
    'margin-top': '20px',
    'font-weight': 'bold',
    'color': '#34495e',
    'font-family': 'Arial, sans-serif'
}

CONTAINER_STYLE = {
    'maxWidth': '1100px',
    'margin': 'auto',
    'padding': '20px'
}

def card(children):
    return html.Div(
        children,
        style={
            'background': 'white',
            'padding': '15px',
            'margin-bottom': '30px',
            'box-shadow': '0 4px 8px rgba(0,0,0,0.1)',
            'border-radius': '8px'
        }
    )

# ===================== DASH ===================== #
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Painel Educacional e Socioeconômico", style=TITLE_STYLE),

    html.Div([
        card(dcc.Graph(figure=px.line(evasao, x='Ano', y='Taxa_Abandono', color='Dependencia_Administrativa', 
                                    title="Taxa de Evasão por Rede"))),
        card(dcc.Graph(figure=px.bar(ideb.dropna(), x='Municipio', y='IDEB', color='Rede', title="IDEB por Município"))),
        card(dcc.Graph(figure=px.line(renda, x='Ano', y='Renda_Media', color='Regiao', title="Renda Média por Região"))),
        card(dcc.Graph(figure=px.line(economia, x='Ano', y=['Desemprego', 'Inflacao', 'PIB'], title="Indicadores Econômicos"))),
        card(dcc.Graph(figure=px.bar(infra.sum().reset_index(), x='index', y=0, labels={'index': 'Indicador', 0: 'Total'}, 
                                    title="Infraestrutura Escolar"))),
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(450px, 1fr))', 'gap': '30px'}),

    html.H2("Mapa de Escolas por Risco de Evasão", style=SECTION_TITLE_STYLE),
    card(dcc.Graph(figure=px.scatter_mapbox(escolas_risco, lat="Latitude", lon="Longitude", color="Risco_Evasao", 
                                           size="Risco_Evasao", hover_name="Escola", 
                                           color_continuous_scale=px.colors.sequential.Reds, zoom=4)
               .update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}))),

    html.H2("Ranking de Fatores mais Influentes", style=SECTION_TITLE_STYLE),
    card(dcc.Graph(figure=px.bar(fatores.sort_values('Importancia'), x='Importancia', y='Fator', orientation='h', 
                                title="Importância dos Fatores na Evasão"))),

    html.H2("Comparativo Público vs Privado", style=SECTION_TITLE_STYLE),
    card(dcc.Graph(figure=px.box(evasao, x='Dependencia_Administrativa', y='Taxa_Abandono', 
                                title="Taxa de Evasão por Rede"))),

    html.H2("Comparativo: Evasão Real vs Predita", style=SECTION_TITLE_STYLE),
    card(dcc.Graph(figure=px.line(df, x='Ano', y=['Taxa_Abandono', 'Predito'], 
                                 labels={'value': 'Taxa de Evasão', 'variable': 'Tipo'}, 
                                 title="Evasão Real vs Predita"))),

    html.H2("Projeção Futura de Evasão Escolar", style=SECTION_TITLE_STYLE),

    card([
        dcc.Dropdown(
            id='filtro-ano',
            options=[{'label': str(ano), 'value': ano} for ano in df_futuro['Ano']],
            multi=True,
            value=df_futuro['Ano'].tolist(),
            placeholder="Selecione os anos para visualizar",
            style={'margin-bottom': '20px'}
        ),
        dcc.Graph(id='grafico-projecao-futura'),
    ]),

    html.H2("Simulador de Cenários", style=SECTION_TITLE_STYLE),

    card([
        html.Label("Inflação Simulada (%)", style=SLIDER_LABEL_STYLE),
        dcc.Slider(id='slider-inflacao', min=0, max=20, step=0.5, value=5,
                   marks={i: f"{i}%" for i in range(0, 21, 5)}),
        html.Label("Desemprego Simulado (%)", style=SLIDER_LABEL_STYLE),
        dcc.Slider(id='slider-desemprego', min=0, max=20, step=0.5, value=10,
                   marks={i: f"{i}%" for i in range(0, 21, 5)}),
        dcc.Graph(id='grafico-simulador')
    ]),

], style=CONTAINER_STYLE)


@app.callback(
    Output('grafico-projecao-futura', 'figure'),
    Input('filtro-ano', 'value')
)
def atualizar_grafico_projecao(anos_selecionados):
    if not anos_selecionados:
        anos_selecionados = df_futuro['Ano'].tolist()
    df_filtrado = df_futuro[df_futuro['Ano'].isin(anos_selecionados)]

    fig = px.bar(df_filtrado, x='Ano', y='Evasao_Prevista',
                 labels={'Evasao_Prevista': 'Taxa de Evasão Prevista', 'Ano': 'Ano'},
                 title='Projeção Futura de Evasão Escolar',
                 color='Evasao_Prevista',
                 color_continuous_scale=px.colors.sequential.Blues)
    fig.update_layout(coloraxis_showscale=False)
    return fig


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
    fig = px.bar(df_sim, x='Fator', y='Valor', title="Simulação de Evasão",
                 color='Fator',
                 color_discrete_map={'Inflação': '#e74c3c', 'Desemprego': '#3498db', 'Evasão Estimada': '#2ecc71'})
    fig.update_layout(showlegend=False)
    return fig


if __name__ == '__main__':
    app.run(debug=True)
