import streamlit as st
import json
import os

def load_json_data(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return []

def save_json_data(json_path, data):
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        st.success("Dados salvos com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")

def filter_clients(clientes_data, nome_empresa, cnpj, ramo_atividade):
    resultados = clientes_data
    if nome_empresa:
        resultados = [cliente for cliente in resultados if nome_empresa.lower() in cliente.get("Nome da Empresa", "").lower()]
    if cnpj:
        resultados = [cliente for cliente in resultados if cnpj in cliente.get("CNPJ", "")]
    if ramo_atividade:
        resultados = [cliente for cliente in resultados if ramo_atividade.lower() in cliente.get("Ramo de Atividade", "").lower()]
    return resultados

def run():
    json_path = os.path.join(os.path.dirname(__file__), '../data/clientes_stella_doro.json')
    clientes_data = load_json_data(json_path)

    st.title("Clientes - Stella d'Oro")

    st.sidebar.title("Filtros de Busca")
    nome_empresa = st.sidebar.text_input("Nome da Empresa")
    cnpj = st.sidebar.text_input("CNPJ")
    ramo_atividade = st.sidebar.text_input("Ramo de Atividade")

    resultados = filter_clients(clientes_data, nome_empresa, cnpj, ramo_atividade)

    if resultados:
        st.write(f"Mostrando {len(resultados)} resultado(s):")
        for cliente in resultados:
            with st.expander(cliente.get("Nome da Empresa", "Nome da Empresa não encontrado")):
                for key, value in cliente.items():
                    st.write(f"**{key}:** {value}")
            st.markdown("---")
    else:
        st.write("Nenhum resultado encontrado.")

    st.sidebar.title("Adicionar Novo Cliente")
    with st.sidebar.form(key='form_add_cliente'):
        novo_cliente = {}
        for field in [
            "Razão Social", "Nome da Empresa", "CNPJ", "IE", "Logradouro", "Bairro", "CEP",
            "Cidade", "Estado", "Telefone do Comprador", "Nome do Comprador", "Email do Comprador",
            "Telefone do Financeiro", "Nome do Financeiro", "Email do Financeiro",
            "Condição de Pagamento", "Email XML", "Ramo de Atividade"
        ]:
            novo_cliente[field] = st.text_input(field)
        novo_cliente["Anotações"] = st.text_area("Anotações")

        submit_button = st.form_submit_button(label='Adicionar Cliente')

    if submit_button:
        clientes_data.append(novo_cliente)
        save_json_data(json_path, clientes_data)

if __name__ == "__main__":
    run()
