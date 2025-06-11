from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower

# 1. Criar sessão Spark
spark = SparkSession.builder \
    .appName("LimpezaDeDados") \
    .getOrCreate()

# 2. Carregar dados CSV
caminho_csv = "dados.csv"  # Substitua pelo caminho do seu arquivo
df = spark.read.csv(caminho_csv, header=True, inferSchema=True)

# 3. Visualizar estrutura e primeiras linhas
print(">>> Esquema do DataFrame:")
df.printSchema()

print(">>> Primeiras linhas:")
df.show(5)

# 4. Remover linhas com valores nulos
df = df.dropna()

# 5. Remover duplicatas
df = df.dropDuplicates()

# 6. Padronizar nomes: trim (remover espaços) + lower (tudo minúsculo)
df = df.withColumn("nome", lower(trim(col("nome"))))

# 7. Converter tipos, se necessário
df = df.withColumn("idade", col("idade").cast("integer"))

# 8. Filtrar dados inválidos (ex: idade negativa)
df = df.filter(col("idade") > 0)

# 9. Visualizar resultado
print(">>> Após limpeza:")
df.show()

# 10. Salvar resultado
df.write.csv("dados_limpos.csv", header=True, mode="overwrite")

# 11. Encerrar Spark
spark.stop()
