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

# Função para obter os usuários do banco de dados
def obter_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, nome, email, data_nascimento FROM usuario")
        usuarios = cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao acessar o banco de dados: {err}")
        usuarios = []
    
    cursor.close()
    
    return usuarios

# Função para editar um usuário
def editar_usuario(id_usuario, novo_nome, novo_email, nova_senha, nova_dt_nasc):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        # Atualiza apenas os campos necessários (nome, email, senha, data_nascimento)
        query = "UPDATE usuario SET nome = %s, email = %s, senha = SHA(%s), data_nascimento = %s WHERE id = %s"
        cursor.execute(query, (novo_nome, novo_email, nova_senha, nova_dt_nasc, id_usuario))
        conn.commit()
        st.success("Usuário atualizado com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar o usuário: {err}")
    finally:
        cursor.close()

# Função para excluir um usuário
def excluir_usuario(id_usuario):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM usuario WHERE id = %s"
        cursor.execute(query, (id_usuario,))
        conn.commit()
        st.success("Usuário excluído com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro ao excluir o usuário: {err}")
    finally:
        cursor.close()

# Função para exibir os usuários e permitir edição/exclusão
def pagina_editar_excluir_usuarios():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.title("Editar/Excluir Usuários")
        
        # Obter os usuários
        usuarios = obter_usuarios()
        
        # Verifica se existem usuários
        if usuarios:
            for usuario in usuarios:
                usuario_id = usuario[0]
                nome = usuario[1]
                email = usuario[2]
                dt_nasc = usuario[3]
                
                st.subheader(f"Usuário: {nome} ({email})")
                
                # Opção de editar as informações do usuário
                novo_nome = st.text_input(f"Novo Nome para {nome}", nome, key=f"nome_{usuario_id}")
                novo_email = st.text_input(f"Novo Email para {email}", email, key=f"email_{usuario_id}")
                nova_senha = st.text_input("Nova Senha", type="password", key=f"senha_{usuario_id}")
                nova_dt_nasc = st.date_input("Nova Data de Nascimento", value=dt_nasc, key=f"nascimento_{usuario_id}")
                
                if st.button(f"Salvar Alterações para o Usuário {nome}", key=f"salvar_{usuario_id}"):
                    # Checa se algum campo foi alterado
                    if novo_nome != nome or novo_email != email or nova_senha or nova_dt_nasc != dt_nasc:
                        editar_usuario(usuario_id, novo_nome, novo_email, nova_senha, nova_dt_nasc)
                
                # Opção de excluir o usuário
                if st.button(f"Excluir o Usuário {nome}", key=f"excluir_{usuario_id}"):
                    excluir_usuario(usuario_id)
                
                st.markdown("---")  # Separador entre os usuários
        else:
            st.write("Nenhum usuário encontrado.")
    else:
        st.error("Você precisa estar logado para acessar esta página.")

# Função principal para controlar a navegação
def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        pagina_editar_excluir_usuarios()  # Exibe a página de editar/excluir usuários
    else:
        st.error("Você precisa estar logado para acessar os usuários.")

# Controla a navegação
pagina_principal()
