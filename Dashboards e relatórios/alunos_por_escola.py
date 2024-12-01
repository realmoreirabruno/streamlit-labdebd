import streamlit as st
import pandas as pd
import mysql.connector 
import matplotlib.pyplot as plt

def get_connection():
    # Salvar o certificado `ca.pem` em um arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(st.secrets["database"]["ssl_cert"].encode("utf-8"))
        ssl_cert_path = tmp_file.name

    # Criar conexão usando os secrets e o certificado SSL
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        port=st.secrets["DB_PORT"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_NAME"],
        ssl_ca=["DB_SSL"]
    )

# Query para obter os dados
query = """
SELECT 
    e.NO_ENTIDADE AS Nome_Escola,
    COUNT(DISTINCT m.ID_MATRICULA) AS Total_Alunos,
    COUNT(DISTINCT d.CO_PESSOA_FISICA) AS Total_Professores,
    CASE 
        WHEN COUNT(DISTINCT d.CO_PESSOA_FISICA) = 0 THEN NULL 
        ELSE ROUND(COUNT(DISTINCT m.ID_MATRICULA) / COUNT(DISTINCT d.CO_PESSOA_FISICA), 2)
    END AS Proporcao_Alunos_por_Professor
FROM 
    escola e
LEFT JOIN 
    matricula m ON e.CO_ENTIDADE = m.CO_ENTIDADE
LEFT JOIN 
    docente d ON e.CO_ENTIDADE = d.CO_ENTIDADE
GROUP BY 
    e.NO_ENTIDADE
ORDER BY 
    Total_Alunos DESC
LIMIT 10;
"""

# Obter os dados do banco
@st.cache_data
def load_data():
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar os dados
st.title("Dashboard: Proporção de Alunos por Professor")
data = load_data()

# Exibir os dados como tabela
st.subheader("Top 10 Escolas com Mais Alunos")
st.dataframe(data)

# Criar visualização gráfica
st.subheader("Proporção de Alunos por Professor (Top 10)")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(data["Nome_Escola"], data["Proporcao_Alunos_por_Professor"], color="dimgray")  # Cor cinza escuro
ax.set_xlabel("Escola", fontsize=12, color="white")
ax.set_ylabel("Proporção Alunos/Professor", fontsize=12, color="white")
ax.set_title("Proporção de Alunos por Professor (Top 10 Escolas)", fontsize=14, color="white")
ax.tick_params(axis='x', rotation=45, colors="white")  # Ajuste da cor das labels no eixo X
ax.tick_params(axis='y', colors="white")  # Ajuste da cor das labels no eixo Y
fig.patch.set_facecolor('#2b2b2b')  # Fundo do gráfico cinza escuro
ax.set_facecolor('#2b2b2b')  # Fundo da área do plot cinza escuro
st.pyplot(fig)
