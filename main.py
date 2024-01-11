import pandas as pd
import streamlit as st

# Configurações gerais do Streamlit
st.set_page_config(page_title='Análise concorrência', page_icon=':chart_with_upwards_trend:', layout="wide")

@st.cache_data
def get_data():
    df = pd.read_csv("amostra_google_empresas.csv")
    del df['Endereco']
    df = df.sample(df.shape[0]).reset_index(drop=True)
    df.fillna('', inplace=True)
    df['Avaliacao'] = df['Avaliacao'].apply(lambda x: x.replace(',','.') if x!='' else x)

    return df

# ler csv com os dados
df = get_data()

# select box para os estados
estado = st.sidebar.selectbox(
    "Selecione o estado:",
    ['Todos'] + df.Estado.unique().tolist(),
)

# se for == 'Todos' vai retornar um df vazio
df_estado = df[(df["Estado"] == estado)]
# se for vazio, trazer tudo
if df_estado.empty:
    df_estado = df

# select box para as cidades
cidade = st.sidebar.selectbox(
    "Selecione a cidade:",
    ['Todas'] + df_estado.Cidade.unique().tolist(),
)

# se for == 'Todas' vai retornar um df vazio
df_cidade = df_estado[(df_estado["Cidade"] == cidade)]
# se for vazio, trazer tudo
if df_cidade.empty:
    df_cidade = df_estado

# select box para as categorias
categoria = st.sidebar.selectbox(
    "Selecione a categoria:",
    ['Todas'] + df_cidade.Categoria.unique().tolist(),
)

#se for == 'Todas' vai retornar um df vazio
df_cat = df_cidade[df_cidade['Categoria']==categoria]
# se for vazio, trazer tudo
if df_cat.empty:
    df_cat = df_cidade

#------------------------------------LABELS-----------------------------------------
grid = st.columns([1, 1, 1])
grid[0].markdown(f"Estado selecionado: :violet[**{estado}**]")
grid[1].markdown(f"Cidade selecionada: :violet[**{cidade}**]")
grid[2].markdown(f"Categoria selecionada: :violet[**{categoria}**]")
st.text('')

#------------------------------------INDICADORES--------------------------------------
st.header(":violet[Indicadores]")
grid = st.columns([1, 1, 1])
grid[0].metric("Quantidade de empresas", value=df_cat.shape[0])
grid[1].metric("Quantidade de categorias", value=df_cat.Categoria.nunique())
grid[2].metric("Média de avaliação (de 0 a 5 estrelas)", value=round(df_cat[df_cat['Avaliacao']!='']['Avaliacao'].astype(float).mean(),2))

grid = st.columns([1, 1, 1])
grid[0].metric("Quantidade de empresas com **avaliação** ⭐", value=df_cat[df_cat['Avaliacao']!=''].shape[0])
grid[1].metric("Quantidade de empresas com **Telefone** 📞", value=df_cat[df_cat['Telefone']!=''].shape[0])
grid[2].metric("Quantidade de empresas com **Site** 🖱️", value=df_cat[df_cat['Site']!=''].shape[0])

def calc_proporcao(numerador):
    denominador = df_cat.shape[0]

    if denominador != 0:
        return f'{round((numerador/denominador*100),2)} %'
    else:
        return '0%'

grid[0].metric("Proporção de empresas com **avaliação**", value=calc_proporcao(df_cat[df_cat['Avaliacao']!=''].shape[0]))
grid[1].metric("Proporção de empresas com **Telefone**", value=calc_proporcao(df_cat[df_cat['Telefone']!=''].shape[0]))
grid[2].metric("Proporção de empresas com **Site**", value=calc_proporcao(df_cat[df_cat['Site']!=''].shape[0]))
st.text('')

#------------------------------------DADOS-----------------------------------------
#st.header(":violet[Dados]")
with st.expander("Dados"):
    st.dataframe(df_cat.reset_index(drop=True), use_container_width=True)

