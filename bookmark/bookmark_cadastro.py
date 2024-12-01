import streamlit as st
import mysql.connector

# Conexão com o banco de dados
import streamlit as st
import mysql.connector
import tempfile

def conectar_banco():
    # Verifica se a conexão já existe e está ativa
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        # Salvar o certificado `ca.pem` em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(st.secrets["DB_SSL"].encode("utf-8"))
            ssl_cert_path = tmp_file.name
        
        # Criar conexão com o banco de dados usando os secrets
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            port=st.secrets["DB_PORT"],
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"],
            ssl_ca=["DB_SSL"]
        )
        
        st.session_state.conn = conn
    
    return st.session_state.conn

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

def pagina_bookmark():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.title("Cadastrar Bookmark")
        
        escolas = obter_escolas()
        
        if escolas:
            lista_escolas = [escola[1] for escola in escolas]
            escola_selecionada = st.selectbox("Selecione a Escola:", lista_escolas)
            
            descricao = st.text_area("Descrição do Bookmark:")
            
            if st.button("Cadastrar"):
                if escola_selecionada and descricao:
                    id_escola = escolas[lista_escolas.index(escola_selecionada)][0]
                    id_usuario = st.session_state["user_id"] 
                    cadastrar_bookmark(id_usuario, id_escola, descricao)
                else:
                    st.warning("Preencha todos os campos!")
        else:
            st.error("Não há escolas disponíveis para selecionar.")
    else:
        st.error("Você precisa estar logado para acessar esta página.")

def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        pagina_bookmark() 
    else:
        st.error("Você precisa estar logado para acessar os bookmarks.")

pagina_principal()
