import streamlit as st
import mysql.connector
import datetime

st.title("Cadastro de usuário")

# Conexão com o banco de dados
def conectar_banco():
    return mysql.connector.connect(
        host='localhost', 
        user='root', 
        password='1234',
        port=3306, 
        database='censo_escolar'
    )

# Cabeçalho com o nome do usuário
def exibir_cabecalho():
    if st.session_state.get("logado") and st.session_state.get("nome_usuario"):
        st.markdown(f"### Bem-vindo, {st.session_state['nome_usuario']}!")
    else:
        st.warning("Você precisa estar logado para acessar esta página!")

# Página de cadastro
def pagina_cadastro():
    exibir_cabecalho()
    
    st.header("Cadastro de Usuários")
    
    def validar(nome, email, senha, dt_nasc):
        return all([nome, email, senha, dt_nasc])
    
    def cadastra_usuario(nome, email, senha, dt_nasc):
        conn = conectar_banco()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO Usuario (nome, email, senha, data_nascimento, data_cadastro) 
            VALUES (%s, %s, SHA(%s), %s, NOW())
        """
        valores = (nome, email, senha, dt_nasc)
        
        try:
            cursor.execute(query, valores)
            conn.commit()
            st.success("Usuário cadastrado com sucesso!")
        except Exception as e:
            conn.rollback()
            st.error(f"Erro ao cadastrar o usuário: {e}")
        finally:
            cursor.close()
            conn.close()

    with st.form("cadastro"):
        nome = st.text_input('Nome:')
        email = st.text_input('Email:')
        senha = st.text_input('Senha:', type="password")
        dt_nasc = st.date_input(
            'Data de nascimento:', 
            min_value=datetime.date(1924, 1, 1), 
            max_value=datetime.date(2024, 1, 1)
        )
        submit = st.form_submit_button("Enviar")
    
    if submit and validar(nome, email, senha, dt_nasc):
        cadastra_usuario(nome, email, senha, dt_nasc)
    elif submit:
        st.warning("Dados inválidos!")

# Inicializa o estado
if "logado" not in st.session_state or not st.session_state["logado"]:
    st.warning("Acesso negado! Faça login primeiro.")
    st.session_state["page"] = "login"  # Muda a página para login
else:
    pagina_cadastro()
