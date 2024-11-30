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

# Função para obter os bookmarks do usuário
def obter_bookmarks_usuario(id_usuario):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, descricao, id_escola FROM bookmark WHERE id_usuario = %s", (id_usuario,))
        bookmarks = cursor.fetchall()
    except mysql.connector.Error as err:
        st.error(f"Erro ao acessar o banco de dados: {err}")
        bookmarks = []
    
    cursor.close()
    
    return bookmarks

# Função para editar o bookmark
def editar_bookmark(id_bookmark, nova_descricao):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        query = "UPDATE bookmark SET descricao = %s WHERE id = %s"
        cursor.execute(query, (nova_descricao, id_bookmark))
        conn.commit()
        st.success("Bookmark atualizado com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar o bookmark: {err}")
    finally:
        cursor.close()

# Função para excluir o bookmark
def excluir_bookmark(id_bookmark):
    conn = conectar_banco()
    cursor = conn.cursor()
    
    try:
        query = "DELETE FROM bookmark WHERE id = %s"
        cursor.execute(query, (id_bookmark,))
        conn.commit()
        st.success("Bookmark excluído com sucesso!")
    except mysql.connector.Error as err:
        st.error(f"Erro ao excluir o bookmark: {err}")
    finally:
        cursor.close()

# Função para exibir os bookmarks e permitir edição/exclusão
def pagina_editar_excluir_bookmarks():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.title("Editar/Excluir Bookmarks")
        
        id_usuario = st.session_state["user_id"]
        
        # Obter os bookmarks do usuário
        bookmarks = obter_bookmarks_usuario(id_usuario)
        
        # Verifica se existem bookmarks
        if bookmarks:
            for bookmark in bookmarks:
                bookmark_id = bookmark[0]
                descricao = bookmark[1]
                id_escola = bookmark[2]
                
                st.subheader(f"Bookmark: {descricao}")
                st.write(f"ID Escola: {id_escola}")
                
                # Opção de editar a descrição do bookmark
                nova_descricao = st.text_input(f"Nova Descrição para o Bookmark {descricao}", descricao)
                if st.button(f"Salvar Alterações para o Bookmark {descricao}"):
                    if nova_descricao != descricao:
                        editar_bookmark(bookmark_id, nova_descricao)
                
                # Opção de excluir o bookmark
                if st.button(f"Excluir o Bookmark {descricao}"):
                    excluir_bookmark(bookmark_id)
                
                st.markdown("---")  # Separador entre os bookmarks
                
        else:
            st.write("Você não tem bookmarks criados.")
    else:
        st.error("Você precisa estar logado para acessar esta página.")

# Função principal para controlar a navegação
def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        pagina_editar_excluir_bookmarks()  # Exibe a página de editar/excluir bookmarks
    else:
        st.error("Você precisa estar logado para acessar os bookmarks.")

# Controla a navegação
pagina_principal()
