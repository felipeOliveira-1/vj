import streamlit as st
import importlib
import json
import os

# Configuration
st.set_page_config(page_title="Cadastro Clientes", layout='wide', initial_sidebar_state="expanded")

# Helper Functions
def load_module(module_name):
    return importlib.import_module(f"pages.{module_name}")

def create_header():
    st.title("🏢 Sistema de Cadastro de Clientes VJ")
    st.markdown("<p class='big-font'>Gerencie seus clientes de forma eficiente</p>", unsafe_allow_html=True)
    st.markdown("---")

def load_page(page_name):
    try:
        module = load_module(page_name.lower().replace(" ", "_").replace("'", ""))
        module.run()
    except ImportError as e:
        st.error(f"Erro ao importar a página {page_name}: {str(e)}")
    except Exception as e:
        st.error(f"Erro ao carregar a página {page_name}: {str(e)}")

def count_total_clients():
    total = 0
    json_files = ['clientes_coco.json', 'clientes_manikraft.json', 'clientes_plastnova.json', 'clientes_stella_doro.json', 'clientes_stretch_center.json']
    for file in json_files:
        path = os.path.join(os.path.dirname(__file__), 'data', file)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                total += len(data)
        except Exception as e:
            st.error(f"Erro ao ler o arquivo {file}: {str(e)}")
    return total

# Main App
def main():
    create_header()

    # Sidebar
    st.sidebar.title("📋 Navegação")
    pages = ["Página Inicial", "Coco do Vale", "Stretch Center", "Manikraft", "Stella d'Oro", "Plastnova"]
    page = st.sidebar.selectbox("Selecione uma Empresa", pages)

    # Main Content
    if page == "Página Inicial":
        st.write("👋 Bem-vindo ao Sistema de Cadastro de Clientes!")
        st.info("Escolha uma empresa no menu lateral para gerenciar seus clientes.")

        # Quick stats
        total_clients = count_total_clients()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total de Clientes", value=total_clients)
        with col2:
            st.metric(label="Empresas Cadastradas", value="5")
        with col3:
            st.metric(label="Média de Clientes por Empresa", value=f"{total_clients/5:.1f}")

    else:
        load_page(page)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("💼 Desenvolvido por FSTech © 2024")

    # Help tooltip
    st.sidebar.markdown("ℹ️ **Precisa de ajuda?**")
    if st.sidebar.button("Clique aqui"):
        st.sidebar.write("Para suporte, entre em contato: contato@fstech.digital")

if __name__ == "__main__":
    main()
