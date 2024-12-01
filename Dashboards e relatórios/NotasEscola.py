import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if "conn" in st.session_state and st.session_state.conn:
    try:
        query = """
        SELECT e.NO_ENTIDADE, r.ideb_AI, r.ideb_AF, r.ideb_EM
        FROM censo_escolar.escola_ideb r
        JOIN censo_escolar.escola e ON e.CO_ENTIDADE = r.CO_ENTIDADE
        ORDER BY e.NO_ENTIDADE;
        """
        
        df = pd.read_sql(query, con=st.session_state.conn)

        st.title("Resultado do IDEB por Escola")
        st.dataframe(df)

        df_sorted = df.sort_values('ideb_AI', ascending=False).head(10)
        
        plt.figure(figsize=(10,6))
        sns.barplot(y='NO_ENTIDADE', x='ideb_AI', data=df_sorted, palette='Blues_d')

        plt.title('Top 10 Escolas por Nota IDEB (AI)', fontsize=16, color='white')
        plt.xlabel('Nota IDEB - AI', fontsize=12, color='white')
        plt.ylabel('Nome da Escola', fontsize=12, color='white')
        plt.xticks(color='white')
        plt.yticks(color='white')

        plt.gca().set_facecolor('#2f2f2f')
        plt.gcf().patch.set_facecolor('#2f2f2f')

        st.pyplot(plt)

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
else:
    st.error("Conexão com o banco não está disponível.")