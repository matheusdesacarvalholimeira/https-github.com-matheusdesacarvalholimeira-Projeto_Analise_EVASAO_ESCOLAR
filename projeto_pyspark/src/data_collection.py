import pandas as pd

# --- 1. Carregar bases com tratamento adequado ---

try:
    alunos = pd.read_csv('data.csv', delimiter=';')
    print("Base de alunos carregada.")
except Exception as e:
    print(f"Erro ao carregar 'data.csv': {e}")
    alunos = pd.DataFrame()

try:
    abandono = pd.read_csv('AbandonoEscolar_RendaMedia_2013_2023.csv', delimiter=',')
    print("Base de abandono escolar carregada.")
except Exception as e:
    print(f"Erro ao carregar 'AbandonoEscolar_RendaMedia_2013_2023.csv': {e}")
    abandono = pd.DataFrame()

# AQUI: pula 4 linhas iniciais inúteis que aparecem antes do cabeçalho real
try:
    ideb = pd.read_csv('Divulgacao_Anos_Finais_Municipios_2017.csv', delimiter=',', skiprows=4)
    print("Base IDEB/SAEB carregada.")
except Exception as e:
    print(f"Erro ao carregar 'Divulgacao_Anos_Finais_Municipios_2017.csv': {e}")
    ideb = pd.DataFrame()

# --- 2. Taxa de evasão histórica ---
if not abandono.empty:
    try:
        evasao_historica = abandono.groupby(['Ano', 'Dependencia_Administrativa'])['Taxa_Abandono'].mean().reset_index()
        print("\nTaxa de evasão histórica:")
        print(evasao_historica.head())
        evasao_historica.to_csv('evasao_historica.csv', index=False)
    except Exception as e:
        print(f"Erro ao processar evasão histórica: {e}")

# --- 3. IDEB e SAEB com colunas corrigidas ---
if not ideb.empty:
    try:
        col_base = ['Sigla da UF', 'Código do Município', 'Nome do Município', 'Rede']
        col_ideb = [col for col in ideb.columns if 'IDEB' in col.upper()]
        col_saeb = [col for col in ideb.columns if 'SAEB' in col.upper()]
        col_aprov = [col for col in ideb.columns if 'Aprovação' in col]

        all_cols = col_base + col_ideb + col_saeb + col_aprov
        ideb_info = ideb[all_cols]
        print("\nIDEB / SAEB / Taxa de aprovação:")
        print(ideb_info.head())
        ideb_info.to_csv('indicadores_educacionais.csv', index=False)
    except Exception as e:
        print(f"Erro ao processar IDEB/SAEB: {e}")

# --- 4. Renda média por região ---
if not abandono.empty:
    try:
        renda_media = abandono.groupby(['Ano', 'Regiao'])['Renda_Media'].mean().reset_index()
        print("\nRenda média por região e ano:")
        print(renda_media.head())
        renda_media.to_csv('renda_media_regiao.csv', index=False)
    except Exception as e:
        print(f"Erro ao processar renda média: {e}")

# --- 5. Indicadores socioeconômicos ---
if not alunos.empty:
    try:
        socioeco_cols = [col for col in alunos.columns if 'Unemployment' in col or 'GDP' in col or 'Inflation' in col]
        socioeco = alunos[socioeco_cols]
        print("\nIndicadores socioeconômicos dos alunos (amostra):")
        print(socioeco.head())
        socioeco.to_csv('indicadores_socioeconomicos.csv', index=False)
    except Exception as e:
        print(f"Erro ao processar dados socioeconômicos: {e}")

# --- 6. Infraestrutura escolar simulada ---
if not alunos.empty:
    try:
        infraestrutura_cols = [
            'Curricular units 1st sem (enrolled)',
            'Tuition fees up to date',
            'Scholarship holder'
        ]
        infraestrutura = alunos[infraestrutura_cols]
        print("\nInfraestrutura escolar (dados simulados com base nos campos disponíveis):")
        print(infraestrutura.head())
        infraestrutura.to_csv('infraestrutura_escolar_simulada.csv', index=False)
    except Exception as e:
        print(f"Erro ao processar infraestrutura escolar simulada: {e}")
