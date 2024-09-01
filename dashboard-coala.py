import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import unicodedata

# Função para remover acentos
def remove_acentos(texto):
    if isinstance(texto, str):
        return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))
    return texto

# Configuração da página (deve ser a primeira função chamada)
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Carregando os dados do arquivo JSON
with open('dados_lanchonete.json', 'r') as f:
    data = json.load(f)

# Removendo acentos das chaves e valores no JSON
data = {remove_acentos(k): [remove_acentos(item) for item in v] for k, v in data.items()}

# Convertendo para DataFrame
df = pd.DataFrame(data)

# Verificando as colunas do DataFrame
st.write("Colunas do DataFrame:", df.columns.tolist())

# Título do dashboard
st.title('Dashboard de Vendas da Lanchonete')
st.write('Visualizacao dos dados de vendas por categoria e mes.')

# Filtro de Meses
selected_months = st.sidebar.multiselect(
    "Escolha os Meses para Exibir",
    options=df['Mes'].unique(),
    default=df['Mes'].unique()
)

# Filtrando o DataFrame pelos meses selecionados
filtered_df = df[df['Mes'].isin(selected_months)]

# Resumo dos Dados
st.sidebar.header("Resumo dos Dados")
st.sidebar.metric("Pedidos Totais", sum(filtered_df['Pedidos Totais']))
st.sidebar.metric("Ganho Total", f"R$ {sum(filtered_df['Ganho Total']):,.2f}")
st.sidebar.metric("Ganho Medio por Pedido", f"R$ {sum(filtered_df['Ganho Total']) / sum(filtered_df['Pedidos Totais']):,.2f}")

# Seletor de Graficos
selected_graphs = st.sidebar.multiselect(
    "Escolha os Graficos para Exibir",
    [
        "Pedidos Totais", "Ganho Total", 
        "Entrega Pedidos", "Entrega Valor", 
        "Retirada Pedidos", "Retirada Valor",
        "Salao Pedidos", "Salao Valor", 
        "Saipos Pedidos", "Saipos Valor", 
        "Telefone Pedidos", "Telefone Valor", 
        "Ifood Pedidos", "Ifood Valor"
    ],
    default=["Pedidos Totais", "Ganho Total"]
)

# Funcao para criar e exibir graficos
def plot_graph(x, y, title, ylabel):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(filtered_df[x], filtered_df[y], marker='o', color='#4C72B0')
    ax.set_title(title)
    ax.set_xlabel('Mes')
    ax.set_ylabel(ylabel)
    ax.grid(True)
    st.pyplot(fig)

# Organizando os graficos em duas colunas
col1, col2 = st.columns(2)

# Dicionario para associar os graficos
graphs_dict = {
    "Pedidos Totais": ('Mes', 'Pedidos Totais', 'Pedidos Totais por Mes', 'Quantidade de Pedidos'),
    "Ganho Total": ('Mes', 'Ganho Total', 'Ganho Total por Mes', 'Ganho Total (R$)'),
    "Entrega Pedidos": ('Mes', 'Entrega Pedidos', 'Entrega - Pedidos por Mes', 'Pedidos de Entrega'),
    "Entrega Valor": ('Mes', 'Entrega Valor', 'Entrega - Valor por Mes', 'Valor de Entrega (R$)'),
    "Retirada Pedidos": ('Mes', 'Retirada Pedidos', 'Retirada - Pedidos por Mes', 'Pedidos de Retirada'),
    "Retirada Valor": ('Mes', 'Retirada Valor', 'Retirada - Valor por Mes', 'Valor de Retirada (R$)'),
    "Salao Pedidos": ('Mes', 'Salao Pedidos', 'Salao - Pedidos por Mes', 'Pedidos no Salao'),
    "Salao Valor": ('Mes', 'Salao Valor', 'Salao - Valor por Mes', 'Valor no Salao (R$)'),
    "Saipos Pedidos": ('Mes', 'Saipos Pedidos', 'Saipos - Pedidos por Mes', 'Pedidos Saipos'),
    "Saipos Valor": ('Mes', 'Saipos Valor', 'Saipos - Valor por Mes', 'Valor Saipos (R$)'),
    "Telefone Pedidos": ('Mes', 'Telefone Pedidos', 'Telefone - Pedidos por Mes', 'Pedidos via Telefone'),
    "Telefone Valor": ('Mes', 'Telefone Valor', 'Telefone - Valor por Mes', 'Valor via Telefone (R$)'),
    "Ifood Pedidos": ('Mes', 'Ifood Pedidos', 'Ifood - Pedidos por Mes', 'Pedidos via Ifood'),
    "Ifood Valor": ('Mes', 'Ifood Valor', 'Ifood - Valor por Mes', 'Valor via Ifood (R$)')
}

# Exibindo os graficos selecionados
for idx, graph in enumerate(selected_graphs):
    if idx % 2 == 0:
        with col1:
            plot_graph(*graphs_dict[graph])
    else:
        with col2:
            plot_graph(*graphs_dict[graph])
