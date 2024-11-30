import streamlit as st
import mysql.connector

# Conexão com o banco de dados
def conectar_banco():
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        conn = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='1234',
            port=3306, 
            database='censo_escolar'
        )
        # Armazena a conexão no estado da sessão
        st.session_state.conn = conn
    return st.session_state.conn

# Função para obter as escolas
def obter_escolas():
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        # Ajustando para pegar CO_ENTIDADE (id) e NOME (nome da escola)
        cursor.execute("SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola")
        escolas = cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao acessar o banco de dados: {err}")
        escolas = []
    
    cursor.close()
    
    return escolas

# Função para cadastrar o bookmark
def cadastrar_bookmark(id_usuario, id_escola, descricao):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        query = "INSERT INTO bookmark (id_usuario, id_escola, descricao) VALUES (%s, %s, %s)"
        valores = (id_usuario, id_escola, descricao)
        cursor.execute(query, valores)
        conn.commit()
        st.success("Bookmark cadastrado com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro ao cadastrar o bookmark: {err}")
    finally:
        cursor.close()

# Função para exibir o formulário de bookmark
def pagina_bookmark():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.title("Cadastrar Bookmark")
        
        # Obter as escolas para o dropdown
        escolas = obter_escolas()
        
        # Verifica se a consulta retornou escolas
        if escolas:
            lista_escolas = [escola[1] for escola in escolas]  # Obtém apenas os nomes das escolas
            escola_selecionada = st.selectbox("Selecione a Escola:", lista_escolas)
            
            descricao = st.text_area("Descrição do Bookmark:")
            
            if st.button("Cadastrar"):
                # Verifica se a descrição e escola foram preenchidas
                if escola_selecionada and descricao:
                    id_escola = escolas[lista_escolas.index(escola_selecionada)][0]  # Obtém o CO_ENTIDADE correspondente
                    id_usuario = st.session_state["user_id"]  # Pega o ID do usuário logado
                    cadastrar_bookmark(id_usuario, id_escola, descricao)
                else:
                    st.warning("Preencha todos os campos!")
        else:
            st.error("Não há escolas disponíveis para selecionar.")
    else:
        st.error("Você precisa estar logado para acessar esta página.")

# Função principal para controlar a navegação
def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        pagina_bookmark()  # Exibe a página de cadastro de bookmark
    else:
        st.error("Você precisa estar logado para acessar os bookmarks.")

# Controla a navegação
pagina_principal()
