import streamlit as st
import time

def check_authentication():
    """Checks if the user is authenticated."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login_form():
    """Displays the login form."""
    st.markdown("""
        <style>
            .stTextInput > div > div > input {
                padding: 10px;
            }
            .stButton > button {
                width: 100%;
                padding: 10px;
                background-color: #1a73e8;
                color: white;
                border: none;
                border-radius: 5px;
            }
            .stButton > button:hover {
                background-color: #1557b0;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("Login")
        st.markdown("Bem-vindo ao Dashboard de Produtividade")

        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            # Hardcoded credentials for simplicity
            if username == "admin" and password == "admin":
                st.session_state.authenticated = True
                st.success("Login realizado com sucesso!")
                time.sleep(0.5) # Give some time for the success message to be seen
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")

def logout_button():
    """Displays the logout button."""
    if st.button("Sair"):
        st.session_state.authenticated = False
        st.rerun()
