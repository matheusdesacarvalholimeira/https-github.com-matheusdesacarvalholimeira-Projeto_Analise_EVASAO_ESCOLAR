import os
import logging
from logging.handlers import TimedRotatingFileHandler
import mfa_check

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower
from dotenv import load_dotenv

os.makedirs('logs', exist_ok=True)

log_file = os.path.join('logs', 'data_processing.log')

log_handler = TimedRotatingFileHandler(
    log_file,
    when='midnight',        
    interval=1,
    backupCount=30,         
    encoding='utf-8'
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Também mostra no console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Começo da execução
logger.info("Início da execução do script data_processing.py")

# Carregar o .env
load_dotenv()
BASE_DIR = os.getenv('PROJECT_BASE_PATH')

if BASE_DIR is None:
    logger.error("A variável PROJECT_BASE_PATH não está definida no .env!")
    raise Exception("A variável PROJECT_BASE_PATH não está definida no arquivo .env!")

# 1. Criar sessão Spark
spark = SparkSession.builder \
    .appName("LimpezaDeDadosMultipla") \
    .getOrCreate()

# 2. Lista com nomes das bases
arquivos = [
    "evasao_historica.csv",
    "indicadores_educacionais.csv",
    "renda_media_regiao.csv",
    "indicadores_socioeconomicos.csv",
    "infraestrutura_escolar_simulada.csv"
]

# Caminhos de entrada e saída
caminho_entrada = os.path.join(BASE_DIR, 'projeto_pyspark', 'data', 'raw')
caminho_saida = os.path.join(BASE_DIR, 'projeto_pyspark', 'data', 'processado')

logger.info(f"Caminho de entrada: {caminho_entrada}")
logger.info(f"Caminho de saída: {caminho_saida}")

# 4. Processar cada arquivo
for nome_arquivo in arquivos:
    try:
        logger.info(f"Processando: {nome_arquivo}")

        # 4.1. Carregar CSV
        df = spark.read.csv(os.path.join(caminho_entrada, nome_arquivo), header=True, inferSchema=True)

        # 4.2. Mostrar esquema e amostra
        df.printSchema()
        df.show(3)

        # 4.3. Limpeza
        df = df.dropna()
        df = df.dropDuplicates()

        for col_name, dtype in df.dtypes:
            if dtype == 'string':
                df = df.withColumn(col_name, lower(trim(col(col_name))))

        if 'idade' in df.columns:
            df = df.withColumn("idade", col("idade").cast("integer"))
            df = df.filter(col("idade") > 0)

        logger.info(f"{nome_arquivo} processado com sucesso. Linhas finais: {df.count()}")

        # 4.5. Salvar o resultado
        output_path = os.path.join(caminho_saida, nome_arquivo.replace(".csv", ""))
        df.write.csv(output_path, header=True, mode="overwrite")

        logger.info(f"{nome_arquivo} salvo em: {output_path}")

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo {nome_arquivo}: {str(e)}", exc_info=True)

# 5. Encerrar sessão Spark
spark.stop()
logger.info("Execução finalizada com sucesso.")
