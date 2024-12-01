import streamlit as st
import pandas as pd

if "conn" in st.session_state and st.session_state.conn:
    try:
        query = """
        SELECT * FROM defaultdb.resumo_alunos_escola
        ORDER BY Nome_Escola;
        """
        
        st.write("Testando conexão com o banco.")
        pd.read_sql("SELECT 1", con=st.session_state.conn)
        st.success("Conexão bem-sucedida.")
        
        df = pd.read_sql(query, con=st.session_state.conn)

        if df.empty:
            st.warning("Nenhum dado encontrado na tabela `resumo_alunos_escola`.")
        else:
            st.title("Total de Alunos por Nível de Ensino")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
else:
    st.error("Conexão com o banco não está disponível.")