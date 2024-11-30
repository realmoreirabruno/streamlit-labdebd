import streamlit as st
import pandas as pd

# Criação do Radio para escolher a tabela a ser exibida
menu = st.radio("Escolha uma visualização", ["Turmas por Escola", "Professores e Alunos por Escola"])

if "conn" in st.session_state and st.session_state.conn:
    try:
        # Página 1: Exibir Turmas
        if menu == "Turmas por Escola":
            st.title("Turmas por Escola")

            # Consulta escolas
            escolas_query = "SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola"
            escolas_df = pd.read_sql(escolas_query, con=st.session_state.conn)

            # Seleção da escola
            escola_selecionada = st.selectbox("Selecione uma escola para listar suas turmas", escolas_df["NO_ENTIDADE"].tolist())

            # Recupera o código da escola selecionada
            co_entidade = escolas_df.loc[escolas_df["NO_ENTIDADE"] == escola_selecionada, "CO_ENTIDADE"].values[0]

            # Query para listar as turmas
            turmas_query = f"""
            SELECT 
                t.NO_TURMA AS 'Nome da Turma',
                CONCAT_WS(', ',
                    CASE WHEN t.IN_DISC_QUIMICA = 1 THEN 'Química' ELSE NULL END,
                    CASE WHEN t.IN_DISC_FISICA = 1 THEN 'Física' ELSE NULL END,
                    CASE WHEN t.IN_DISC_MATEMATICA = 1 THEN 'Matemática' ELSE NULL END,
                    CASE WHEN t.IN_DISC_BIOLOGIA = 1 THEN 'Biologia' ELSE NULL END,
                    CASE WHEN t.IN_DISC_LINGUA_PORTUGUESA = 1 THEN 'Língua Portuguesa' ELSE NULL END
                ) AS 'Disciplinas'
            FROM 
                turma t
            WHERE 
                t.CO_ENTIDADE = {co_entidade};
            """
            turmas_df = pd.read_sql(turmas_query, con=st.session_state.conn)

            # Exibe os dados
            if not turmas_df.empty:
                st.write(f"Turmas e disciplinas da escola: **{escola_selecionada}**")
                st.dataframe(turmas_df)
            else:
                st.warning("Nenhuma turma encontrada para a escola selecionada.")

        # Página 2: Professores e Alunos
        elif menu == "Professores e Alunos por Escola":
            st.title("Professores e Alunos por Escola")

            # Consulta escolas
            escolas_query = "SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola"
            escolas_df = pd.read_sql(escolas_query, con=st.session_state.conn)

            # Seleção da escola
            escola_selecionada = st.selectbox("Selecione uma escola para visualizar os professores e alunos", escolas_df["NO_ENTIDADE"].tolist())

            # Recupera o código da escola selecionada
            co_entidade = escolas_df.loc[escolas_df["NO_ENTIDADE"] == escola_selecionada, "CO_ENTIDADE"].values[0]

            # Query para listar professores com dados adicionais
            professores_query = f"""
            SELECT 
                d.CO_PESSOA_FISICA AS 'Código do Professor',
                d.TP_ESCOLARIDADE AS 'Escolaridade',
                d.TP_ETAPA_ENSINO AS 'Etapa de Ensino'
            FROM 
                docente d
            WHERE 
                d.CO_ENTIDADE = {co_entidade};
            """
            professores_df = pd.read_sql(professores_query, con=st.session_state.conn)

            # Query para listar alunos com dados adicionais
            alunos_query = f"""
            SELECT 
                m.CO_PESSOA_FISICA AS 'Código do Aluno',
                m.TP_SEXO AS 'Sexo',
                m.NU_IDADE AS 'Idade'
            FROM 
                matricula m
            WHERE 
                m.CO_ENTIDADE = {co_entidade};
            """
            alunos_df = pd.read_sql(alunos_query, con=st.session_state.conn)

            # Exibe os dados
            st.write(f"Professores e alunos da escola: **{escola_selecionada}**")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Professores")
                if not professores_df.empty:
                    st.dataframe(professores_df)
                else:
                    st.warning("Nenhum professor encontrado para a escola selecionada.")

            with col2:
                st.subheader("Alunos")
                if not alunos_df.empty:
                    st.dataframe(alunos_df)
                else:
                    st.warning("Nenhum aluno encontrado para a escola selecionada.")

    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
else:
    st.error("Conexão com o banco não está disponível.")
