import dash
import json
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def load_data():
    df = pd.read_csv('data/dados_tratados.csv').reset_index()
    df['secao'] = (df['secao'].astype(int)).astype(str)
    df['zona'] = (df['zona'].astype(int)).astype(str)
    with open('data/bairros_corrigido.json', 'r') as file:
        coords_file = json.load(file)

    return df, coords_file
    
def grouping_data(partido, cargo):
    df, coords_file = load_data()
    df = df[df['cargo'] != '    Você aprova a alteração da bandeira  de Belo Horizonte?']
    zon_sec = df[['zona', 'secao']].copy()
    zon_sec = zon_sec.drop_duplicates(subset=['zona', 'secao'])
    num_secoes = {}
    for zona in list(set(zon_sec['zona'])):
        num_secoes[zona] = zon_sec[zon_sec['zona']==zona].shape[0]
    if cargo == 'Prefeito':
        if partido == 'Todos':
            df = df[df['cargo'] == 'Prefeito']
            new_idx = ['nome', 'partido', 'zona']
            temp = df.copy().reset_index().set_index(new_idx)
            dados = temp.groupby(new_idx).sum().reset_index()[['nome', 'partido', 'zona', 'votos']]
            dados = dados.set_index('nome').join(dados[['nome', 'votos']].set_index('nome').groupby('nome').sum(), on='nome', rsuffix='_total', lsuffix='_por_secao').reset_index()
            temp = df[['zona', 'secao', 'capacidade_da_secao', 'comparecimento']].copy()
            temp.drop_duplicates(subset=['zona', 'secao'], inplace=True)
            capacidade_por_zona = temp[['zona', 'capacidade_da_secao']].groupby('zona').sum().reset_index()
            capacidade_por_zona.columns = ['zona', 'capacidade_por_zona']
            capacidade_por_zona.set_index('zona', inplace=True)
            comparecimento_por_zona = temp[['zona', 'comparecimento']].groupby('zona').sum().reset_index()
            comparecimento_por_zona.columns = ['zona', 'comparecimento_por_zona']
            comparecimento_por_zona.set_index('zona', inplace=True)
            dados = dados.set_index('zona').join(capacidade_por_zona, on='zona').reset_index()
            dados = dados.set_index('zona').join(comparecimento_por_zona, on='zona').reset_index()
            dados['ausencia_por_zona'] = dados['capacidade_por_zona'] - dados['comparecimento_por_zona']
            return [coords_file, dados]
        else:
            return [coords_file, df]
    elif cargo == 'Vereador':
        df = df[df['cargo'] == 'Vereador']
        zon_sec = df[['zona', 'secao']].copy()
        zon_sec = zon_sec.drop_duplicates(subset=['zona', 'secao'])
        if partido == 'Todos':
            new_idx = ['nome', 'partido', 'zona']
            temp = df.copy().reset_index().set_index(new_idx)
            dados = temp.groupby(new_idx).sum().reset_index()[['nome', 'partido', 'zona', 'votos']]
            dados = dados.set_index('nome').join(dados[['nome', 'votos']].set_index('nome').groupby('nome').sum(), on='nome', rsuffix='_total', lsuffix='_por_secao').reset_index()
            temp = df[['zona', 'secao', 'capacidade_da_secao', 'comparecimento']].copy()
            temp.drop_duplicates(subset=['zona', 'secao'], inplace=True)
            capacidade_por_zona = temp[['zona', 'capacidade_da_secao']].groupby('zona').sum().reset_index()
            capacidade_por_zona.columns = ['zona', 'capacidade_por_zona']
            capacidade_por_zona.set_index('zona', inplace=True)
            comparecimento_por_zona = temp[['zona', 'comparecimento']].groupby('zona').sum().reset_index()
            comparecimento_por_zona.columns = ['zona', 'comparecimento_por_zona']
            comparecimento_por_zona.set_index('zona', inplace=True)
            dados = dados.set_index('zona').join(capacidade_por_zona, on='zona').reset_index()
            dados = dados.set_index('zona').join(comparecimento_por_zona, on='zona').reset_index()
            dados['ausencia_por_zona'] = dados['capacidade_por_zona'] - dados['comparecimento_por_zona']
            return [coords_file, dados]
        else:
            df = df[df['partido'] == partido]
            #new = zon_sec.set_index(['zona', 'secao']).join(df.set_index(['zona', 'secao']), how='left', on=['zona', 'secao']).reset_index()
            votos_no_partido = df[['zona', 'votos']].groupby('zona').sum().reset_index()
            candidato_mais_votado = df[['nome','zona', 'votos']].groupby(['nome','zona']).sum().reset_index()
            candidato_mais_votado_por_zona = candidato_mais_votado.sort_values(by='votos')
            candidato_mais_votado = candidato_mais_votado[['nome', 'votos']].groupby('nome').sum().reset_index().sort_values(by='votos', ascending=False)
            return [coords_file, num_secoes, candidato_mais_votado_por_zona, candidato_mais_votado, votos_no_partido]
    elif cargo == 'Todos':
        if partido == 'Todos':
            mais_votados_por_zona = df[['zona', 'partido', 'votos']].copy().groupby(['partido','zona']).sum().reset_index()
            return [coords_file, mais_votados_por_zona, df]
        else:
            new = df[df['partido'] == partido]
            mais_votados_por_zona = new[['zona', 'partido', 'votos']].copy().groupby(['partido','zona']).sum().reset_index()
            return [coords_file, mais_votados_por_zona, df]


df, coord = load_data()
id_map = pd.read_csv('data/teste_bh_dados.csv').reset_index()   
data_prefeitos = df[df['cargo']=='Prefeito']
data_prefeitos_votos = data_prefeitos[['zona', 'partido', 'nome', 'votos']]
temp = data_prefeitos_votos.groupby(['zona', 'partido', 'nome']).sum()
data_prefeitos_votos = data_prefeitos_votos.set_index(['zona', 'partido', 'nome']).join(temp, on=['zona', 'partido', 'nome'], how='left', rsuffix='_soma_secao').reset_index()
data_prefeitos_votos.columns = ['zona', 'partido', 'nome', 'votos', 'soma de votos na zona']
temp = data_prefeitos[['zona', 'votos']].groupby('zona').sum()
data_prefeitos_votos = data_prefeitos_votos.set_index('zona').join(temp,on='zona', how='left',rsuffix='_total').reset_index()
brancos = ['#BRANCO#' if j == 'Branco' else i for i,j in zip(data_prefeitos_votos['partido'], data_prefeitos_votos['nome'])]
data_prefeitos_votos['partido'] = brancos
soma_votos_pref = data_prefeitos_votos[['partido','nome','votos']].groupby(['partido','nome']).sum().reset_index().sort_values(by='votos',ascending=False)
total_votos_pref = soma_votos_pref['votos'].sum()
soma_votos_pref['percentual'] = round(100*soma_votos_pref['votos']/soma_votos_pref['votos'].sum(),2)
partidos_prefeitura = list(set(data_prefeitos_votos['partido']))

resultados_pref_dict = {}
for partido in partidos_prefeitura:
    temp = data_prefeitos_votos[['zona', 'partido', 'nome', 'soma de votos na zona', 'votos_total']].drop_duplicates()
    temp = temp[temp['partido']==partido].sort_values(by='soma de votos na zona',ascending=False).head(3)
    resultados_pref_dict[partido] = {'zona':list(temp['zona']),
                                     'votos':list(temp['soma de votos na zona'].astype(int)),
                                     'percentual':[round(100*i/j,2) for i,j in zip(temp['soma de votos na zona'],temp['votos_total'])],
                                     'total':int(data_prefeitos[data_prefeitos['partido']==partido]['votos'].sum())}
    #print(resultados_pref_dict[partido])
data_vereadores = df[df['cargo']=='Vereador']
data_vereadores_votos = data_vereadores[['zona', 'partido', 'nome', 'votos']]
ranking_vereadores = data_vereadores_votos[['partido', 'nome', 'votos']].groupby(['partido', 'nome']).sum()
temp_ranking = data_vereadores_votos[['partido', 'nome', 'votos']].groupby(['partido', 'nome']).std()

ranking_vereadores = ranking_vereadores.join(temp_ranking, on=['partido', 'nome'], how='left',lsuffix='_soma',rsuffix='_std').reset_index()

temp = data_vereadores_votos.groupby(['zona', 'partido', 'nome']).sum()
data_vereadores_votos = data_vereadores_votos.set_index(['zona', 'partido', 'nome']).join(temp, on=['zona', 'partido', 'nome'], how='left', rsuffix='_soma_secao').reset_index()
data_vereadores_votos.columns = ['zona', 'partido', 'nome', 'votos', 'soma de votos na zona']
temp = data_vereadores[['zona', 'votos']].groupby('zona').sum()
data_vereadores_votos = data_vereadores_votos.set_index('zona').join(temp,on='zona', how='left',rsuffix='_total').reset_index()
brancos = ['#BRANCO#' if j == 'Branco' else i for i,j in zip(data_vereadores_votos['partido'], data_vereadores_votos['nome'])]
data_vereadores_votos['partido'] = brancos
soma_votos_ver = data_vereadores_votos[['partido','nome','votos']].groupby(['partido','nome']).sum().reset_index().sort_values(by='votos',ascending=False)
soma_votos_ver['percentual'] = round(100*soma_votos_pref['votos']/soma_votos_pref['votos'].sum(),2)
total_votos_ver = soma_votos_ver['votos'].sum()
partidos_vereanca = list(set(data_vereadores_votos['partido']))
resultados_ver_dict, ranking_ver_dic = {}, {}
for partido in partidos_vereanca:
    temp = data_vereadores_votos[['zona', 'partido', 'nome', 'soma de votos na zona', 'votos_total']].drop_duplicates()
    temp = temp[temp['partido']==partido].sort_values(by='soma de votos na zona',ascending=False).head(3)
    resultados_ver_dict[partido] = {'zona':list(temp['zona']),
                                     'votos':list(temp['soma de votos na zona'].astype(int)),
                                     'percentual':[round(100*i/j,2) for i,j in zip(temp['soma de votos na zona'],temp['votos_total'])],
                                     'total':int(data_vereadores[data_vereadores['partido']==partido]['votos'].sum())}

    temp = ranking_vereadores[ranking_vereadores['partido']==partido].sort_values('votos_soma',ascending=False).head(3)
    ranking_ver_dic[partido] = {'nome':list(temp['nome']),
                                'votos':list(temp['votos_soma']),
                                'std':list(temp['votos_std'])
    }

votos_por_zona_ver = data_vereadores[['zona', 'partido', 'votos']].groupby(['partido', 'zona']).sum().reset_index()

mais_votados_ver = soma_votos_ver[['partido', 'nome', 'votos']].sort_values(by='votos', ascending=False).head(10)
mais_votados_ver['investimento declarado']=[0.0, 0.0, 302080.00, 726000.00, 546934.18, 372263.05, 0.0, 431746.89, 500291.11, 289843.57]
votos_nulos_vereanca = mais_votados_ver.head(2)['votos'].sum()
total_de_votos_por_partido = data_vereadores_votos[['partido', 'votos']].groupby('partido').sum().reset_index()
contagem_de_votos_ideológicos = data_vereadores_votos[data_vereadores_votos['nome'].isin(list(set(data_vereadores_votos['partido'])))][['nome', 'votos']].groupby('nome').sum().reset_index()


# heatmap params
matriz_de_valores = []
zona_heatmap = list(set(data_prefeitos_votos['zona']))
for partido in partidos_prefeitura:
    vars = []
    for zona in zona_heatmap:
        vars.append(int(sum(data_prefeitos_votos[(data_prefeitos_votos['partido']==partido)&(data_prefeitos_votos['zona']==zona)]['votos'])))
    matriz_de_valores.append(vars)

votos_por_zona_partidos_ver = data_vereadores_votos[['zona', 'partido', 'soma de votos na zona']].drop_duplicates()
votos_total_esquerda_ver = votos_por_zona_partidos_ver[votos_por_zona_partidos_ver['partido'].isin(['PT', 'PDT', 'PSOL', 'PCdoB', 'PCB', 'UP', 'PSTU', 'PSB'])]['soma de votos na zona'].sum()
votos_total_brancos_nulos_ver = votos_por_zona_partidos_ver[votos_por_zona_partidos_ver['partido'].isin(['#NULO#', '#BRANCO#'])]['soma de votos na zona'].sum()

#### map

hist_all_data = pd.DataFrame({'zona':[],
                    'partido':[],
                    'votos para prefeito':[],
                    'votos para vereador': [],
                    'máximo de votos':[]})
zon, len_zon =  list(set(df['zona'])), len(list(set(df['zona'])))
num_cand = {}
for part in partidos_prefeitura:
    num_cand[part] = len(set(df[(df['cargo']=='Vereador')&(df['partido']==part)]['nome']))
for part in partidos_prefeitura:
    data_pref = df[(df['cargo']=='Prefeito')&(df['partido']==part)]
    data_ver = df[(df['cargo']=='Vereador')&(df['partido']==part)]
    votos_pref = data_pref[['zona', 'votos']].groupby('zona').sum().reset_index()
    votos_pref.columns=['zona', 'votos para prefeito']
    votos_ver = data_ver[['zona', 'votos']].groupby('zona').sum().reset_index()
    votos_ver.columns=['zona', 'votos para vereador']
    new = pd.DataFrame({'zona':zon,
                        'partido':[part for _ in range(len_zon)],
                        'máximo de votos':[num_cand[part] for _ in range(len_zon)]})
    new = new.set_index('zona').join(votos_pref.set_index('zona'), on='zona', how='left')
    new = new.join(votos_ver.set_index('zona'), on='zona', how='left').reset_index()
    hist_all_data = pd.concat([hist_all_data, new])

hist_all_data['votos para prefeito por votos para vereador'] = round(hist_all_data['votos para vereador']/hist_all_data['votos para prefeito'],2)

#### dfs

mais_votados_por_zona = df[['zona', 'partido', 'votos']].groupby(['partido','zona']).sum().reset_index()
mais_votados = mais_votados_por_zona[['partido', 'votos']].groupby('partido').sum().sort_values(by='votos', ascending = False).reset_index()
temp = df[['zona', 'secao', 'capacidade_da_secao', 'comparecimento']].drop_duplicates(subset=['zona', 'secao'])
comparecimento_total = temp['comparecimento'].sum()
capacidade_total = temp['capacidade_da_secao'].sum()
#percentual_de_ausencia = (capacidade_total - comparecimento_total)/comparecimento_total
percentual_de_comparecimento = comparecimento_total/capacidade_total

total_de_votos_no_partido = mais_votados_por_zona['votos'].sum()
mais_votados_por_zona['percentual'] = mais_votados_por_zona['votos']/total_de_votos_no_partido
mais_votados_por_zona.sort_values(by='votos', ascending=False, inplace=True)
total_de_votos = df['votos'].sum()
votos_ideologicos = df[(df['partido']==partido)&(df['nome']==partido)]['votos'].sum()


#### variables
percentual_votos_nulos_pref = round(soma_votos_pref.set_index('nome')['percentual']['Nulo'] +\
                              soma_votos_pref.set_index('nome')['percentual']['Branco'],2)
percentual_votos_esquerda_pref = round(soma_votos_pref.set_index('nome')['percentual']['DUDA SALABERT'] +\
                                 soma_votos_pref.set_index('nome')['percentual']['ROGERIO CORREIA'] +\
                                 soma_votos_pref.set_index('nome')['percentual']['INDIRA XAVIER'] +\
                                 soma_votos_pref.set_index('nome')['percentual']['WANDERSON ROCHA'],2)



total_de_votos_por_partido.to_csv('data/total_de_votos_por_partido_resumo.csv', sep=';', index=False)
contagem_de_votos_ideológicos.to_csv('data/contagem_de_votos_ideológicos_resumo.csv', sep=';', index=False)
soma_votos_pref.to_csv('data/soma_votos_pref_resumo.csv', sep=';', index=False)
data_prefeitos_votos.to_csv('data/data_prefeitos_votos_resumo.csv', sep=';', index=False)
data_vereadores_votos.to_csv('data/data_vereadores_votos_resumo.csv', sep=';', index=False)
mais_votados_ver.to_csv('data/mais_votados_ver_resumo.csv', sep=';', index=False)
mais_votados.to_csv('data/mais_votados_resumo.csv', sep=';', index=False)
mais_votados_por_zona.to_csv('data/mais_votados_por_zona_resumo.csv', sep=';', index=False)
votos_por_zona_ver.to_csv('data/votos_por_zona_ver_resumo.csv', sep=';', index=False)
hist_all_data.to_csv('data/hist_all_data_resumo.csv', sep=';', index=False)


varaveis_resumo = {'percentual_votos_nulos_pref': percentual_votos_nulos_pref,
                   'percentual_votos_esquerda_pref':percentual_votos_esquerda_pref,
                   'resultados_pref_dict':resultados_pref_dict,
                   'resultados_ver_dict':resultados_ver_dict,
                   'votos_total_brancos_nulos_ver':votos_total_brancos_nulos_ver,
                   'total_votos_ver':total_votos_ver,
                   'total_votos_pref':total_votos_pref,
                   'votos_total_esquerda_ver':votos_total_esquerda_ver,
                   'ranking_ver_dic':ranking_ver_dic,
                   'comparecimento_total':comparecimento_total,
                   'capacidade_total':capacidade_total,
                   'percentual_de_comparecimento':percentual_de_comparecimento,
                   'total_de_votos_no_partido':total_de_votos_no_partido,
                   'total_de_votos':total_de_votos,
                   'votos_ideologicos':votos_ideologicos,
                   }

with open('data/variaveis_resumo.json', 'w') as outfile:
    json.dump(varaveis_resumo, outfile)

