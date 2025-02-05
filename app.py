import streamlit as st
import pandas as pd

def configure_page():
    """Configura a página do Streamlit."""
    st.set_page_config(
        page_title="Instagram Data Viewer",
        page_icon="✨",
        layout="wide"
    )

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame | None:
    """
    Carrega o arquivo XLSX e retorna um DataFrame.
    Em caso de erro, exibe a mensagem e retorna None.
    """
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

def get_required_columns() -> list[str]:
    """Retorna a lista de colunas obrigatórias."""
    return [
        "user/username", 
        "text", 
        "comment_like_count",
        "user/is_verified", 
        "created_at", 
        "user_profile_url"
    ]

def get_column_order() -> list[str]:
    """Define a ordem das colunas para exibição."""
    return [
        "user_profile_url",
        "user/username",
        "user/is_verified",
        "comment_like_count",
        "text",
        "created_at"
    ]

def get_column_config() -> dict:
    """Define a configuração das colunas para o dataframe."""
    return {
        "user/profile_pic_url": st.column_config.LinkColumn(
            "Foto de perfil",
            help="Foto de perfil do usuário",
            display_text="Ver foto",

        ),
        "user_profile_url": st.column_config.LinkColumn("Perfil do usuário", display_text="Ver perfil"),
        "user/username": st.column_config.TextColumn("Usuário"),
        "user/is_verified": st.column_config.CheckboxColumn("Verificado"),
        "comment_like_count": st.column_config.NumberColumn("Curtidas"),
        "text": st.column_config.TextColumn("Comentário"),
        "created_at": st.column_config.DateColumn("Data do comentário")
    }

def validate_columns(df: pd.DataFrame, required_columns: list[str]) -> bool:
    """
    Verifica se todas as colunas obrigatórias estão presentes no DataFrame.
    Retorna True se estiverem, caso contrário exibe erro e retorna False.
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"As seguintes colunas estão faltando no arquivo: {missing}")
        return False
    return True

def display_data(df: pd.DataFrame, required_columns: list[str]):
    """Exibe o dataframe com a configuração definida."""
    st.header("Dados do Instagram", divider=True)
    st.dataframe(
        data=df[required_columns],
        key="dataframe-instagram",
        column_order=get_column_order(),
        column_config=get_column_config(),
        use_container_width=True
    )

def export_usernames(df: pd.DataFrame):
    """Exporta os nomes de usuário da coluna 'user/username' em um arquivo de texto com 'https://www.instagram.com/' adicionado a cada nome."""
    if "user/username" in df.columns:
        usernames = df["user/username"].dropna().tolist()
        instagram_urls = [f"https://www.instagram.com/{username}" for username in usernames]
        urls_text = "\n".join(instagram_urls)
        st.download_button(
            label="Exportar user/username como texto",
            data=urls_text,
            file_name="usernames.txt",
            mime="text/plain"
        )
    else:
        st.error("A coluna 'user/username' não foi encontrada no arquivo XLSX.")
        
        



def main():
    """Função principal do aplicativo."""
    configure_page()

    uploaded_file = st.file_uploader("Escolha um arquivo XLSX", type="xlsx")
    if uploaded_file is not None:
        df = load_data(uploaded_file)
    else:
        st.stop()

    if df is None:
        st.stop()

    required_columns = get_required_columns()
    if not validate_columns(df, required_columns):
        st.stop()

    display_data(df, required_columns)
    export_usernames(df)

if __name__ == "__main__":
    main()
