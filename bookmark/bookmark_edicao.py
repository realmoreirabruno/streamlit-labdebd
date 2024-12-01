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
            port=int(st.secrets["DB_PORT"]),
            user=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            database=st.secrets["DB_NAME"],
            ssl_ca=["DB_SSL"]
        )
        
        st.session_state.conn = conn
    
    return st.session_state.conn

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

def pagina_editar_excluir_bookmarks():
    if "logado" in st.session_state and st.session_state["logado"]:
        st.title("Editar/Excluir Bookmarks")
        
        id_usuario = st.session_state["user_id"]
        
        bookmarks = obter_bookmarks_usuario(id_usuario)
        
        if bookmarks:
            for bookmark in bookmarks:
                bookmark_id = bookmark[0]
                descricao = bookmark[1]
                id_escola = bookmark[2]
                
                st.subheader(f"Bookmark: {descricao}")
                st.write(f"ID Escola: {id_escola}")
                
                nova_descricao = st.text_input(f"Nova Descrição para o Bookmark {descricao}", descricao)
                if st.button(f"Salvar Alterações para o Bookmark {descricao}"):
                    if nova_descricao != descricao:
                        editar_bookmark(bookmark_id, nova_descricao)
                
                if st.button(f"Excluir o Bookmark {descricao}"):
                    excluir_bookmark(bookmark_id)
                
                st.markdown("---")
                
        else:
            st.write("Você não tem bookmarks criados.")
    else:
        st.error("Você precisa estar logado para acessar esta página.")

def pagina_principal():
    if "logado" in st.session_state and st.session_state["logado"]:
        pagina_editar_excluir_bookmarks()
    else:
        st.error("Você precisa estar logado para acessar os bookmarks.")

pagina_principal()
