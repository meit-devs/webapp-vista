import requests
import json
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout='wide')

headers = {
    'Accept': 'application/json'
}

page_num = 1
realty_list = []

while page_num < 3:
    url_base = "https://terrazal-rest.vistahost.com.br/imoveis/listar?"
    key = 'd59579d4676b3cb2de5b4c9db292e685'
    params = '&pesquisa={"fields":'
    columns = '["Codigo","CorretorNome","Categoria","Status","Situacao","Ocupacao","EstadoConservacaoImovel",\
        "Cidade","Bairro","Dormitorios","Suites","Salas","TotalBanheiros","Vagas","Varanda","ValorCondominio",\
            "AreaPrivativa","AreaTotal","ValorIptu","ValorLocacao","TituloSite","DescricaoWeb","FotoDestaque"],'
    pages = '"paginacao":{"pagina":' + str(page_num) + ',"quantidade":50}}'

    url = url_base + 'key=' + key + params + columns + pages

    response = requests.get(url, headers=headers).json()
    df = pd.DataFrame.from_dict(response).transpose()
    
    realty_list.append(df)
    page_num += 1

df = pd.concat(realty_list)
df = df.replace(r'^\s*$', np.nan, regex=True)
df['ValorCondominio'] = np.where((df['Categoria'] == 'Casa'), 0, df['ValorCondominio'])
df['ValorCondominio'] = pd.to_numeric(df['ValorCondominio'])

st.title("Vista CRM - Consulta de Imóveis")

# Creates box for text input to be utilized as filter
realty_id = st.text_input("Código do Imóvel - APENAS NÚMERO")

df_realty = df.loc[df['Codigo'] == str(realty_id)]

st.dataframe(df_realty)

st.header('TABELA COM TODOS OS IMÓVEIS')
st.dataframe(df)