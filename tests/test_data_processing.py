import pytest
from pyspark.sql.functions import col, trim, lower
from pyspark.sql import SparkSession

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("PySparkUnitTest").getOrCreate()

def test_remocao_de_nulos_e_duplicados(spark):
    dados = [
        (" João ", 20),
        ("Maria", None),
        (" João ", 20),
        (None, 18)
    ]
    colunas = ["nome", "idade"]

    df = spark.createDataFrame(dados, colunas)

    df = df.dropna()
    df = df.dropDuplicates()

    for col_name, dtype in df.dtypes:
        if dtype == 'string':
            df = df.withColumn(col_name, lower(trim(col(col_name))))

    resultado = df.collect()
    nomes = [row['nome'] for row in resultado]

    assert len(resultado) == 1
    assert nomes[0] == "joão"
    assert resultado[0]['idade'] == 20

def test_conversao_coluna_idade(spark):
    dados = [
        ("Lucas", "18"),
        ("Ana", "abc"),    
        ("Pedro", "-5"),
        ("Maria", None)
    ]
    colunas = ["nome", "idade"]

    df = spark.createDataFrame(dados, colunas)

    with pytest.raises(Exception):
        for col_name, dtype in df.dtypes:
            if dtype == 'string' and col_name == 'idade':
                df = df.withColumn(col_name, col(col_name).cast("integer"))
        df = df.filter(col("idade") > 0)
        df.collect()
