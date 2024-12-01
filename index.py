import streamlit as st
import mysql.connector

st.set_page_config(page_title="Login", initial_sidebar_state="collapsed")

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
            port=int(st.secrets["DB_PORT"]),
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"],
            ssl_ca=["DB_SSL"]
        )
        
        st.session_state.conn = conn
    
    return st.session_state.conn


def validar_login(email, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    query = "SELECT id, nome FROM usuario WHERE email = %s AND senha = SHA(%s)"
    valores = (email, senha)
    cursor.execute(query, valores)
    resultado = cursor.fetchone()
    
    cursor.close()
    
    return resultado

def pagina_login():
    if "logado" not in st.session_state or not st.session_state["logado"]:
        st.title("Login")
        email = st.text_input("Email:")
        senha = st.text_input("Senha:", type="password")
        login = st.button("Entrar")
        
        if login:
            usuario = validar_login(email, senha)
            if usuario:
                user_id, nome = usuario
                st.session_state["logado"] = True
                st.session_state["nome_usuario"] = nome
                st.session_state["user_id"] = user_id
                st.success(f"Bem-vindo, {nome}!")
                return True
            else:
                st.error("Email ou senha inválidos!")
                return False  
    return False  

def exibir_menu():
    if "logado" in st.session_state and st.session_state["logado"]:
        pg = st.navigation(
            {
                "Usuários": [
                    st.Page("users/usuarios_cadastro.py", title="Cadastro Usuário", icon=":material/person_add:"),
                    st.Page("users/usuarios_edicao.py", title="Alteração Usuário", icon=":material/person_edit:")
                ],
                "Bookmarks": [
                    st.Page("bookmark/bookmark_cadastro.py", title="Cadastro Bookmark", icon=":material/bookmark_add:"),
                    st.Page("bookmark/bookmark_edicao.py", title="Alteração Bookmark", icon=":material/bookmark:"),
                ],
                   "Tabelas e Consultas": [
                    st.Page("Tabelas e Consultas/Cidades.py", title="Escolas", icon=":material/bookmark_add:"),
                    st.Page("Tabelas e Consultas/docentes.py", title="Alunos e docentes", icon=":material/bookmark:"),
                ],
                   "Dashboards": [
                    st.Page("Dashboards e relatórios/alunos_por_escola.py", title="Alunos por professor", icon=":material/bookmark_add:"),
                    st.Page("Dashboards e relatórios/NotasEscola.py", title="Notas e ranking", icon=":material/bookmark:"),
                ],
            }
        )
        pg.run()

# Página principal (após login)
def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.write(f"Bem-vindo, {st.session_state['nome_usuario']}!")
        exibir_menu()
    else:
        if pagina_login(): 
            exibir_menu()

pagina_principal()
