from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower

# 1. Criar sessão Spark
spark = SparkSession.builder \
    .appName("LimpezaDeDadosMultipla") \
    .getOrCreate()

# 2. Lista com nomes das bases (sem caminhos)
arquivos = [
    "evasao_historica.csv",
    "indicadores_educacionais.csv",
    "renda_media_regiao.csv",
    "indicadores_socioeconomicos.csv",
    "infraestrutura_escolar_simulada.csv"
]

# 3. Caminhos absolutos (ajustados para seu projeto)
caminho_entrada = "/home/matheus/Documents/https-github.com-matheusdesacarvalholimeira-Projeto_Analise_EVASAO_ESCOLAR/projeto_pyspark/data/raw/"
caminho_saida = "/home/matheus/Documents/https-github.com-matheusdesacarvalholimeira-Projeto_Analise_EVASAO_ESCOLAR/projeto_pyspark/data/"

# 4. Processar cada arquivo
for nome_arquivo in arquivos:
    print(f"\n>>> Processando: {nome_arquivo}")

    # 4.1. Carregar CSV
    df = spark.read.csv(caminho_entrada + nome_arquivo, header=True, inferSchema=True)

    # 4.2. Exibir esquema e amostra
    df.printSchema()
    df.show(3)

    # 4.3. Limpeza
    df = df.dropna()
    df = df.dropDuplicates()

    # Padroniza todas as colunas tipo string: tira espaços e coloca minúsculo
    for col_name, dtype in df.dtypes:
        if dtype == 'string':
            df = df.withColumn(col_name, lower(trim(col(col_name))))

    # Exemplo de tratamento específico: se tiver coluna 'idade'
    if 'idade' in df.columns:
        df = df.withColumn("idade", col("idade").cast("integer"))
        df = df.filter(col("idade") > 0)

    # 4.4. Mostrar preview após limpeza
    print(f">>> {nome_arquivo} após limpeza:")
    df.show(3)

    # 4.5. Salvar no diretório processado
    df.write.csv(caminho_saida + nome_arquivo.replace(".csv", ""), header=True, mode="overwrite")

# 5. Encerrar sessão Spark
spark.stop()
