import streamlit as st
import pandas as pd



# Verifica se a conexão está disponível
if "conn" in st.session_state and st.session_state.conn:
    try:
        # Consulta para contar alunos por nível de ensino
        query = """
       SELECT * FROM censo_escolar.resumo_alunos_escola
        ORDER BY Nome_Escola;
        """
        
        # Executa a consulta no banco de dados
        df = pd.read_sql(query, con=st.session_state.conn)

        # Exibe o dataframe com os resultados
        st.title("Total de Alunos por Nível de Ensino")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
else:
    st.error("Conexão com o banco não está disponível.")