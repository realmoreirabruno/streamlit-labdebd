import streamlit as st
import pandas as pd

# Verifica se a conexão está configurada
if "conn" in st.session_state and st.session_state.conn:
    try:
        # Consulta para buscar as informações de escolas
        query = """
        SELECT 
            e.NO_ENTIDADE AS Nome_Escola,
            e.CO_ENTIDADE AS Codigo_Escola,
            (
                SELECT COUNT(DISTINCT m.CO_PESSOA_FISICA)
                FROM defaultdb.matricula m
                WHERE m.CO_ENTIDADE = e.CO_ENTIDADE
            ) AS Total_Alunos,
            (
                SELECT COUNT(DISTINCT d.CO_PESSOA_FISICA)
                FROM defaultdb.docente d
                WHERE d.CO_ENTIDADE = e.CO_ENTIDADE
            ) AS Total_Professores,
            (
                SELECT COUNT(DISTINCT t.ID_TURMA)
                FROM defaultdb.turma t
                WHERE t.CO_ENTIDADE = e.CO_ENTIDADE
            ) AS Total_Turmas
        FROM 
            defaultdb.escola e
        LIMIT 100;
        """
        
        # Executa a consulta e carrega os dados
        df = pd.read_sql(query, con=st.session_state.conn)
        
        # Exibe o DataFrame inicial
        st.title("Resumo Escolar")
        st.dataframe(df)

        # Botão para ordenar pelo número de alunos
        if st.button("Ordenar por Número de Alunos"):
            df = df.sort_values(by="Total_Alunos", ascending=False)
            st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao buscar os dados: {e}")
else:
    st.error("Conexão com o banco de dados não está disponível.")