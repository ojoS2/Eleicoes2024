import dash
from statistics import stdev
import json
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import Image


investimentos_dict = {'INDIRA XAVIER':40459.29,
                    'ADRIEL DO MLB':17254.25,
                    'EDNA DA IZIDORA': 13644.50,
                    'MARI FERNANDES':21199.64,
                    'ANA EVANGELISTA': 171610.33,
                    'ANDRE XAVIER': 298600.40,
                    'LUIZA DULCI': 384439.81,
                    'SAMUEL RODRIGUES':53263.73,
                    'CHIQUINHO MACIEL':86113.04,
                    'JU SANTANA':188828.34, 
                    'GERALDO MINEIRINHO DO GÁS': 49243.03, 
                    'JOÃO FEIJÃO': 74679.17, 
                    'ELSON SANTANA':171989.59, 
                    'VIVIANE SANTOS':157853.38, 
                    'ROGERIO CORREIA':8501774.29, 
                    'LUANA':322757.22, 
                    'ADRIANA ARAÚJO': 237172.22, 
                    'PEDRO ROUSSEFF':500291.11, 
                    'TAIS FERREIRA':60583.04, 
                    'PROFESSOR DIMAS':177800.34, 
                    'DR BRUNO PEDRALVA':473166.78, 
                    'NANCI MENEZES':60013.04, 
                    'PEDRO PATRUS':430221.43, 
                    'NEUZA FREITAS':106718.94, 
                    'CLEUSA DO ONIBUS':66743.04, 
                    'JULIANA CARVALHO':56113.04, 
                    'RENATO DE JESUS':155917.34, 
                    'RUBINHO GIAQUINTO':189219.59, 
                    'DIMI':670149.41, 
                    'ROBSON':306848.41, 
                    'JÂNIO RIBEIRO':28769.39, 
                    'ENGENHEIRO FABRICIO':159085.53, 
                    'ADRIANO VENTURA':468066.40, 
                    'JOÃO LOCADORA':127737.34,
                    'ALUIZIO LEANDRO':48764.00, 
                    'ANDRÉ FERNANDES':55000.00, 
                    'BRUNO ENGLER':22567000.00, 
                    'CAMILA COELHO':50000.00,
                    'CLAUDIO DO MUNDO NOVO':571000.00, 
                    'CLAUDIO ONG JUNTOS PODEMOS':45000.00, 
                    'CORONEL GILMAR LUCIANO':105900.00, 
                    'CRISTIANE LOPES': 55120.00, 
                    'CRISTIANO REIS': 85000.00, 
                    'DAI DIAS': 372000.00,
                    'DELEGADO ESIO VIANA':31150.00, 
                    'DÉCIO CHAMO':20000.00, 
                    'EDUARDO ZIMBU':40000.00, 
                    'ELIZABETH MARIANO':60000.00, 
                    'FABIANO DROGARIA MENEZES':60000.00, 
                    'FELIPE CÂNDIDO':57600.00, 
                    'GCM FERNANDES':50450.00, 
                    'HELADIO DA AGRO COTA':54065.00, 
                    'JULIANA GALLINDO':580000.00, 
                    'KARLA DAYRELL':0, 
                    'LAERTE STRADA':60000.00, 
                    'MARCUS POLICARPO':42559.81, 
                    'MARILDA PORTELA':860000.00, 
                    'NANCI JUSSARA':22000.00, 
                    'PABLO ALMEIDA':302080.00, 
                    'PASTOR ALTAMIRO ALVES':61260.00, 
                    'PAULA DI PAULA':50000.00, 
                    'PILOLO DO MDP':55000.00, 
                    'PROFESSORA ROBERTA':121000.00, 
                    'RAFAEL TRAVASSOS':50000.00, 
                    'RENATA LIBERATO':25000.00, 
                    'RICARDO SCHEID':30000.00, 
                    'ROSIMEIRE MEIRINHA':65000.00, 
                    'SARGENTO JALYSON':142000.00, 
                    'SARGENTO RODRIGUES':45000.00, 
                    'SYLVIA GUERRA':25000.00, 
                    'TENENTE CLÁUDIO':24200.00, 
                    'TIAGO LISBOA':40000.00, 
                    'TIAGO OLIVEIRA':60000.00, 
                    'UNER AUGUSTO':138792.22, 
                    'VICTOR LUCCHESI':142051.35, 
                    'VILE':354114.36, 
                    'WALFREDO RODRIGUES':60000.00,
                    'CARLOS VIANA':10086892.92,
                    'DUDA SALABERT':8504968.55,
                    'FUAD NOMAN':21977555.16,
                    'GABRIEL':4455063.85,
                    'LOURDES FRANCISCO':35881.61,
                    'MAURO TRAMONTE':12887483.00,
                    'WANDERSON ROCHA':149194.75,
                    'PT':0,
                    'PL':0,
                    'UP':0}

with open('data/variaveis_analise_do_partido.json', 'r') as file:
    variaveis = json.load(file)
with open('data/bairros_corrigido.json', 'r') as file:
        coordenadas = json.load(file)

id_map = pd.read_csv('data/teste_bh_dados.csv').reset_index()
id_map = id_map[['id', 'nome', 'area', 'zona', 'cor_por_zona']]
votos = pd.read_csv('data/data_mapa_analise.csv',sep=';').reset_index()
data = pd.read_csv('data/data_histograma_analise.csv',sep=';').reset_index()
votos_por_zona = pd.read_csv('data/data_area_analise.csv',sep=';').reset_index()
votos_por_zona_Adriel = pd.read_csv('data/data_Zona_Adriel_analise.csv',sep=';').reset_index()
votos_por_zona_Edna = pd.read_csv('data/data_Zona_Edna_analise.csv',sep=';').reset_index()
votos_por_zona_Indira = pd.read_csv('data/data_Zona_Indira_analise.csv',sep=';').reset_index()
votos_por_zona_Mari = pd.read_csv('data/data_Zona_Mari_analise.csv',sep=';').reset_index()
votos_por_zona_Up = pd.read_csv('data/data_Zona_Up_analise.csv',sep=';').reset_index()

data['zona'] = data['zona'].astype(str)
votos['zona'] = votos['zona'].astype(str)
votos_por_zona['zona'] = votos_por_zona['zona'].astype(str)
votos_por_zona_Adriel['zona'] = votos_por_zona_Adriel['zona'].astype(str)
votos_por_zona_Edna['zona'] = votos_por_zona_Edna['zona'].astype(str)
votos_por_zona_Indira['zona'] = votos_por_zona_Indira['zona'].astype(str)
votos_por_zona_Mari['zona'] = votos_por_zona_Mari['zona'].astype(str)
votos_por_zona_Up['zona'] = votos_por_zona_Up['zona'].astype(str)


def cards_components(mode, entries, texto_2):
    titnome_11 = entries[0][0]
    titnome_12 = entries[0][1]
    titnome_13 = entries[0][2]
    titnome_14 = entries[0][3]
    titval_21 = entries[1][0]
    titval_22 = entries[1][1]
    titval_23 = entries[1][2]
    titval_24 = entries[1][3]
    titval_31 = entries[2][0]
    titval_32 = entries[2][1]
    titval_33 = entries[2][2]
    titval_34 = entries[2][3]
    if mode == 0:
        titulo_1 = 'Candidato'
        titulo_2 = 'Cargo pleiteado'    
        titulo_3 = 'Votos contabilizados'
        paygap = dbc.Row([
                        dbc.Col([
                            html.Div(titulo_1, className=" border-bottom border-3"),
                            html.Div(titnome_11),
                            html.Div(titnome_12),
                            html.Div(titnome_13),
                            html.Div(titnome_14)
                        ], style={"minWidth": 250}),
                        dbc.Col([
                            html.Div(titulo_2, className=" border-bottom border-3"),
                            html.Div( f"{titval_21}"),
                            html.Div(f"{titval_22}"),
                            html.Div(f"{titval_23}"),
                            html.Div(f"{titval_24}"),
                        ]),
                        dbc.Col([
                            html.Div(titulo_3, className=" border-bottom border-3"),
                            html.Div(f"{titval_31}"),
                            html.Div(f"{titval_32}"),
                            html.Div(f"{titval_33}"),
                            html.Div(f"{titval_34}"),
                        ])
                    ], style={"minWidth": 400})
        pil_img = Image.open('assets/UP_logo.png')
        mean = html.Img(src=pil_img, style={'height':'96%', 'width':'100%'})
        median = dbc.Alert(dcc.Markdown(
                texto_2,
            ), color="dark")
        return paygap, mean, median
    elif mode == 1:
        titulo_1 = 'Zona eleitoral mais votada'
        titulo_2 = 'Votos contabilizados'    
        titulo_3 = 'Percentual de ocupacao de urnas'
        pil_img = Image.open('assets/Adriel.png')
    elif mode == 2:
        titulo_1 = 'Zona eleitoral mais votada'
        titulo_2 = 'Votos contabilizados'    
        titulo_3 = 'Percentual de ocupacao de urnas'
        pil_img = Image.open('assets/Edna.png')
    elif mode == 3:
        titulo_1 = 'Zona eleitoral mais votada'
        titulo_2 = 'Votos contabilizados'    
        titulo_3 = 'Percentual de ocupacao de urnas'
        pil_img = Image.open('assets/Indira.png')
    elif mode == 4:
        titulo_1 = 'Partidos mais votados'
        titulo_2 = 'Numero de votos contabilizados'    
        titulo_3 = 'Percentual de votos em relacao ao total'
        pil_img = Image.open('assets/Mari.png')
    paygap = dbc.Row([
                dbc.Col([
                    html.Div(titulo_1, className=" border-bottom border-3"),
                    html.Div(titnome_11),
                    html.Div(titnome_12),
                    html.Div(titnome_13),
                    html.Div(titnome_14)
                ], style={"minWidth": 250}),
                dbc.Col([
                    html.Div(titulo_2, className=" border-bottom border-3"),
                    html.Div( f"{int(titval_21)}"),
                    html.Div(f"{int(titval_22)}"),
                    html.Div(f"{int(titval_23)}"),
                    html.Div(f"{int(titval_24)}")
                ]),
                dbc.Col([
                    html.Div(titulo_3, className=" border-bottom border-3"),
                    html.Div(f"{round(100*titval_31,2)}"),
                    html.Div(f"{round(100*titval_32,2)}"),
                    html.Div(f"{round(100*titval_33,2)}"),
                    html.Div(f"{round(100*titval_34,2)}")
                ])
            ], style={"minWidth": 400})
    mean = html.Img(src=pil_img, style={'height':'96%', 'width':'100%'})#dbc.Alert(html.Img(src='assets/UP_logo.png'), color="dark")
    median = dbc.Alert(dcc.Markdown(
            texto_2,
        ), color="dark")
    return paygap, mean, median

def card_UP():
    
    texto_2 = f"""
                ** Contagem final de votos ** 
                ### {variaveis['votos_total_UP']}  
                ** Custo final declarado por voto** 
                ### {variaveis['preco_do_voto_total_UP']} R$
                ** Média do percentual de ocupacao de urnas**
                ### {variaveis['media_de_ocupacao_de_urna']}%
                ** Percentual de votos ideológicos**
                ### {variaveis['percentual_voto_ideologico']}%
                """
    ent = [['Adriel', 'Edna', 'Indira', 'Mari'],
           ['Vereador', 'Vereadora', 'Prefeita', 'Vereadora'],
           [variaveis['votos_Adriel'], variaveis['votos_Edna'], variaveis['votos_Indira'], variaveis['votos_Mari']]]
    paygap, mean, median = cards_components(mode=0, 
                                            entries=ent,
                                            texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resultados"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center", style={"minHight": 250, "maxHight": 250}),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_Adriel():

    texto_2 = f"""
                ** Contagem de votos ** 
                ### {variaveis['votos_Adriel']}  
                ** Custo final declarado por voto** 
                ### {variaveis['custo_voto_Adriel']} R$
                ** Ocupacao média das urnas**
                ### {variaveis['ocupacao_media_Adriel']}%
                ** Tipo de liderança**
                ### Liderança local (std = {round(variaveis['std_Adriel'], 3)})
                """
    zona_1 = votos_por_zona_Adriel.iloc[0,1]
    zona_2 = votos_por_zona_Adriel.iloc[1,1]
    zona_3 = votos_por_zona_Adriel.iloc[2,1]
    zona_4 = votos_por_zona_Adriel.iloc[3,1]
    voto_1 = votos_por_zona_Adriel.iloc[0,2]
    voto_2 = votos_por_zona_Adriel.iloc[1,2]
    voto_3 = votos_por_zona_Adriel.iloc[2,2]
    voto_4 = votos_por_zona_Adriel.iloc[3,2]
    presenca_1 = votos_por_zona_Adriel.iloc[0,3]
    presenca_2 = votos_por_zona_Adriel.iloc[1,3]
    presenca_3 = votos_por_zona_Adriel.iloc[2,3]
    presenca_4 = votos_por_zona_Adriel.iloc[3,3]
    ent = [[zona_1, zona_2, zona_3, zona_4],
           [voto_1, voto_2, voto_3, voto_4],
           [presenca_1, presenca_2, presenca_3, presenca_4]]
    paygap, mean, median = cards_components(mode=1, 
                                            entries=ent, 
                                            texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resultados"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center", style={"minHight": 250, "maxHight": 250}),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_Edna():
    texto_2 = f"""
                ** Contagem de votos ** 
                ### {variaveis['votos_Edna']}  
                ** Custo final declarado por voto** 
                ### {variaveis['custo_voto_Edna']} R$
                ** Ocupacao média das urnas**
                ### {variaveis['ocupacao_media_Edna']}%
                ** Tipo de liderança**
                ### Liderança local (std = {round(variaveis['std_Edna'],3)})
                """
    zona_1 = votos_por_zona_Edna.iloc[0,1]
    zona_2 = votos_por_zona_Edna.iloc[1,1]
    zona_3 = votos_por_zona_Edna.iloc[2,1]
    zona_4 = votos_por_zona_Edna.iloc[3,1]
    voto_1 = votos_por_zona_Edna.iloc[0,2]
    voto_2 = votos_por_zona_Edna.iloc[1,2]
    voto_3 = votos_por_zona_Edna.iloc[2,2]
    voto_4 = votos_por_zona_Edna.iloc[3,2]
    presenca_1 = votos_por_zona_Edna.iloc[0,3]
    presenca_2 = votos_por_zona_Edna.iloc[1,3]
    presenca_3 = votos_por_zona_Edna.iloc[2,3]
    presenca_4 = votos_por_zona_Edna.iloc[3,3]
    ent = [[zona_1, zona_2, zona_3, zona_4],
           [voto_1, voto_2, voto_3, voto_4],
           [presenca_1, presenca_2, presenca_3, presenca_4]]
    paygap, mean, median = cards_components(mode=2, 
                                            entries=ent, 
                                            texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resultados"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center", style={"minHight": 250, "maxHight": 250}),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_Indira():
    texto_2 = f"""
                ** Contagem de votos ** 
                ### {variaveis['votos_Indira']}  
                ** Custo final declarado por voto** 
                ### {variaveis['custo_voto_Indira']} R$
                ** Ocupacao média das urnas**
                ### {variaveis['ocupacao_media_Indira']}%
                ** Tipo de liderança**
                ### Liderança regional (std = {round(variaveis['std_Indira'],3)})
                """
    zona_1 = votos_por_zona_Indira.iloc[0,1]
    zona_2 = votos_por_zona_Indira.iloc[1,1]
    zona_3 = votos_por_zona_Indira.iloc[2,1]
    zona_4 = votos_por_zona_Indira.iloc[3,1]
    voto_1 = votos_por_zona_Indira.iloc[0,2]
    voto_2 = votos_por_zona_Indira.iloc[1,2]
    voto_3 = votos_por_zona_Indira.iloc[2,2]
    voto_4 = votos_por_zona_Indira.iloc[3,2]
    presenca_1 = votos_por_zona_Indira.iloc[0,3]
    presenca_2 = votos_por_zona_Indira.iloc[1,3]
    presenca_3 = votos_por_zona_Indira.iloc[2,3]
    presenca_4 = votos_por_zona_Indira.iloc[3,3]
    ent = [[zona_1, zona_2, zona_3, zona_4],
           [voto_1, voto_2, voto_3, voto_4],
           [presenca_1, presenca_2, presenca_3, presenca_4]]
    paygap, mean, median = cards_components(mode=3, 
                                            entries=ent, 
                                            texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resultados"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center", style={"minHight": 250, "maxHight": 250}),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_Mari():
    texto_2 = f"""
                ** Contagem de votos ** 
                ### {variaveis['votos_Mari']}  
                ** Custo final declarado por voto** 
                ### {variaveis['custo_voto_Mari']} R$
                ** Ocupacao média das urnas**
                ### {variaveis['ocupacao_media_Mari']}%
                ** Tipo de liderança**
                ### Liderança regional (std = {round(variaveis['std_Mari'], 3)})
                """
    zona_1 = votos_por_zona_Mari.iloc[0,1]
    zona_2 = votos_por_zona_Mari.iloc[1,1]
    zona_3 = votos_por_zona_Mari.iloc[2,1]
    zona_4 = votos_por_zona_Mari.iloc[3,1]
    voto_1 = votos_por_zona_Mari.iloc[0,2]
    voto_2 = votos_por_zona_Mari.iloc[1,2]
    voto_3 = votos_por_zona_Mari.iloc[2,2]
    voto_4 = votos_por_zona_Mari.iloc[3,2]
    presenca_1 = votos_por_zona_Mari.iloc[0,3]
    presenca_2 = votos_por_zona_Mari.iloc[1,3]
    presenca_3 = votos_por_zona_Mari.iloc[2,3]
    presenca_4 = votos_por_zona_Mari.iloc[3,3]
    ent = [[zona_1, zona_2, zona_3, zona_4],
           [voto_1, voto_2, voto_3, voto_4],
           [presenca_1, presenca_2, presenca_3, presenca_4]]
    paygap, mean, median = cards_components(mode=4, 
                                            entries=ent, 
                                            texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resultados"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center", style={"minHight": 250, "maxHight": 250}),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def partido_map():
    dados = id_map.set_index('zona').join(votos.set_index('zona'), how='left', on='zona').reset_index()
    fig = px.choropleth_map(dados, geojson=coordenadas, color='votos no partido',
                                locations="id", featureidkey="properties.ID",
                                center={"lat": -19.912998, "lon": -43.940933},
                                zoom=10,
                                hover_data={'nome':True, 
                                            'zona':True,
                                            'votos no partido':True,
                                            'votos ADRIEL DO MLB':True,
                                            'votos EDNA DA IZIDORA':True,
                                            'votos MARI FERNANDES':True,
                                            'votos INDIRA XAVIER':True,
                                            'votos UP':True,
                                            'id':False}
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ad_coord_1'][0])],
            lon=[float(variaveis['melhor_Ad_coord_1'][1])],
            mode='markers',
            name='local com mais votos para Adriel',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(255, 0, 0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f'Locais com maior número de votos registrados para o Adriel: local{variaveis["melhor_Ad_local_1"]} com {int(variaveis["melhor_Ad_votos_1"])}',
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ad_coord_2'][0])],
            lon=[float(variaveis['melhor_Ad_coord_2'][1])],
            mode='markers',
            name='segundo local com mais votos para Adriel',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(255, 0, 0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para o Adriel: local{variaveis['melhor_Ad_local_2']} com {int(variaveis['melhor_Ad_votos_2'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ed_coord_1'][0])],
            lon=[float(variaveis['melhor_Ed_coord_1'][1])],
            mode='markers',
            name='local com mais votos para Edna',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 255, 0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para a Edna: local{variaveis['melhor_Ed_local_1']} com {int(variaveis['melhor_Ed_votos_1'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ed_coord_2'][0])],
            lon=[float(variaveis['melhor_Ed_coord_2'][1])],
            mode='markers',
            name='segundo local com mais votos para Edna',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 255, 0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para a Edna: local{variaveis['melhor_Ed_local_2']} com {int(variaveis['melhor_Ed_votos_2'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Id_coord_1'][0])+0.001],
            lon=[float(variaveis['melhor_Id_coord_1'][1])+0.001],
            mode='markers',
            name='local com mais votos para Indira',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 0, 255)',
                opacity=1.,
            ),
            text=f"Locais com maior número de votos registrados para a Indira: local {variaveis['melhor_Id_local_1']} com {int(variaveis['melhor_Id_votos_1'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Id_coord_2'][0])],
            lon=[float(variaveis['melhor_Id_coord_2'][1])],
            mode='markers',
            name='segundo local com mais votos para Indira',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 0, 255)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para a Indira: local{variaveis['melhor_Id_local_2']} com {int(variaveis['melhor_Id_votos_2'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Up_coord_1'][0])],
            lon=[float(variaveis['melhor_Up_coord_1'][1])],
            mode='markers',
            name='local com mais votos ideológicos',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 0, 0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de ideológicos votos registrados: local{variaveis['melhor_Up_local_1']} com {int(variaveis['melhor_Up_votos_1'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Up_coord_2'][0])],
            lon=[float(variaveis['melhor_Up_coord_2'][1])],
            mode='markers',
            name='segundo local com mais votos ideológicos',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0,0,0)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos ideológicos registrados: local{variaveis['melhor_Up_local_2']} com {int(variaveis['melhor_Up_votos_2'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ma_coord_1'][0])],
            lon=[float(variaveis['melhor_Ma_coord_1'][1])],
            mode='markers',
            name='local com mais votos para Mari',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 255, 255)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para o Mari: local{variaveis['melhor_Ma_local_1']} com {int(variaveis['melhor_Ma_votos_1'])}",
            hoverinfo='text'
        ))
    fig.add_trace(go.Scattermap(
            lat=[float(variaveis['melhor_Ma_coord_2'][0])],
            lon=[float(variaveis['melhor_Ma_coord_2'][1])],
            mode='markers',
            name='segundo local com mais votos para Mari',
            marker=go.scattermap.Marker(
                size=20,
                color='rgb(0, 255, 255)',
                opacity=1.,
                #symbol="diamond-dot",
            ),
            text=f"Locais com maior número de votos registrados para a Mari: local{variaveis['melhor_Ma_local_2']} com {int(variaveis['melhor_Ma_votos_2'])}",
            hoverinfo='text'
        ))
    
    fig.update_traces(marker={"opacity":0.6})

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.50,
        xanchor="left",
        x=0.05
    ))
    fig.update_layout(
    title=dict(text="""Resultado eleitoral por zonas eleitorais em BH""",
                    font=dict(size=20), automargin=True))
    return fig

def end_card_test(flag):
    if flag == 'Interno':
        var_10 = round(1/variaveis['votos_a_vereador_por_votos_a_pref_UP'],2)
        var_11 = variaveis['corr_ind_Adriel']
        var_21 = variaveis['corr_ind_Edna']
        var_30 = round(variaveis['custo_voto_Indira'],2)
        var_31 = variaveis['corr_ind_Mari']
        var_40 = round(variaveis['custo_voto_ver_UP'],2)
        var_41 = variaveis['corr_ind_Up']
        var_50 = round(variaveis['percentual_ideo_UP'],2)
        var_51 = variaveis['corr_ind_ver']
        text_0 = f"""
        ### UP
        ** Razão de votos a prefeitura por votos a vereança ** 
        ### {var_10}  
        ** Preço médio do voto a prefeitura**
        ### {var_30} R$
        ** Preço médio do voto a vereança**
        ### {var_40} R$
        ** Percentual de votos ideológicos **
        ### {var_50}%
        """
        text_1 = f"""
        ### Correlações de votos (Spearman)
        ** Correlação Indira-Adriel** 
        ### {var_11}  
        ** Correlação Indira-Edna** 
        ### {var_21} 
        ** Correlação Indira-Mari** 
        ### {var_31}
        ** Correlação Indira-votos ideológicos** 
        ### {var_41}
        ** Correlação Indira-todos** 
        ### {var_51}
        """
        text_2 = f"""
        ### Valores declarados
        ** Adriel ** 
        ### {investimentos_dict['ADRIEL DO MLB']} R$ 
        ** Edna ** 
        ### {investimentos_dict['EDNA DA IZIDORA']} R$
        ** Mari **
        ### {investimentos_dict['MARI FERNANDES']} R$
        ** Indira **
        ### {investimentos_dict['INDIRA XAVIER']} R$
        """
        body_1 = dbc.Alert(dcc.Markdown(
                    text_0,
                ), color="dark")
        
        body_2 = dbc.Alert(dcc.Markdown(
                    text_1,
                ), color="dark")
        
        body_3 = dbc.Alert(dcc.Markdown(
                    text_2,
                ), color="dark")

        card =  dbc.Card([
            dbc.CardHeader(html.H2("Informações adicionais"), className="text-center"),
            dbc.CardBody([
                dbc.Row([dbc.Col(body_1), dbc.Col(body_2), dbc.Col(body_3)], className="text-center", style={"minHight": 250, "maxHight": 250})
            ])
        ])
        
    elif flag == 'Comparado':
        #percentual de votos a vereador por votos a prefeito 
        var_1 = round(1/variaveis['votos_a_vereador_por_votos_a_pref_UP'],2)
        var_1_comp_1 = round(1/variaveis['votos_a_vereador_por_votos_a_pref_PT'],2)
        var_1_comp_2 = round(1/variaveis['votos_a_vereador_por_votos_a_pref_PL'],2)
        var_3 = round(variaveis['custo_voto_Indira'],2)
        var_3_comp_1 = round(variaveis['custo_voto_Rogerio'],2)
        var_3_comp_2 = round(variaveis['custo_voto_Bruno'],2)
        var_4 = round(variaveis['custo_voto_ver_UP'],2)
        var_4_comp_1 = round(variaveis['custo_voto_ver_PT'],2)
        var_4_comp_2 = round(variaveis['custo_voto_ver_PL'],2)
        var_5 = round(variaveis['percentual_ideo_UP'],2)
        var_5_comp_1 = round(variaveis['percentual_ideo_PT'],2)
        var_5_comp_2 = round(variaveis['percentual_ideo_PL'],2)
        text_0 = f"""
        ### UP
        ** Votos à prefeitura por votos a vereança** 
        ### {var_1}  
        ** Preço médio do voto a prefeitura**
        ### {var_3}R$
        ** Preço médio do voto a vereança**
        ### {var_4}R$   
        ** Percentual de votos ideológicos **
        ### {var_5}%
        """
        text_1 = f"""
        ### PT
        ** Votos à prefeitura por votos a vereança** 
        ### {var_1_comp_1}  
        ** Preço médio do voto a prefeitura**
        ### {var_3_comp_1} R$
        ** Preço médio do voto a vereança**
        ### {var_4_comp_1} R$
        ** Percentual de votos ideológicos **
        ### {var_5_comp_1}%
        """
        text_2 = f"""
        ### PL
        ** Votos à prefeitura por votos a vereança** 
        ### {var_1_comp_2}  
        ** Preço médio do voto a prefeitura**
        ### {var_3_comp_2}R$
        ** Preço médio do voto a vereança**
        ### {var_4_comp_2}R$
        ** Percentual de votos ideológicos **
        ### {var_5_comp_2}%
        """
        text_3 = f"""
        ### Custo medio de vereadores eleitos
        ** Custo médio do vereador eleito do PL ** 
        ### {variaveis['custo_medio_eleito_PL']}
        ** Custo médio do vereador eleito do NOVO ** 
        ### {variaveis['custo_medio_eleito_NOVO']}  
        ** Custo médio do vereador eleito do PT ** 
        ### {variaveis['custo_medio_eleito_PT']}  
        ** Custo médio do vereador eleito do PSOL ** 
        ### {variaveis['custo_medio_eleito_PSOL']}  
        ** Custo médio do vereador eleito do PCdoB ** 
        ### {variaveis['custo_medio_eleito_PCdoB']}  
        """

        body_1 = dbc.Alert(dcc.Markdown(
                    text_0,
                ), color="dark")
        
        body_2 = dbc.Alert(dcc.Markdown(
                    text_1,
                ), color="dark")
        
        body_3 = dbc.Alert(dcc.Markdown(
                    text_2,
                ), color="dark")

        body_4 = dbc.Alert(dcc.Markdown(
                    text_3,
                ), color="dark")

        card =  dbc.Card([
            dbc.CardHeader(html.H2("Informações adicionais"), className="text-center"),
            dbc.CardBody([
                dbc.Row([dbc.Col(body_1), dbc.Col(body_2), dbc.Col(body_3), dbc.Col(body_4)], className="text-center", style={"minHight": 250, "maxHight": 250})
            ])
        ])

    elif flag == 'Indisponível':
        var_00 = 'Indisponível'
        text_0 = f"""
        ### 
        ** ** 
        ### {var_00}  
        """
        body_1 = dbc.Alert(dcc.Markdown(
                    text_0,
                ), color="dark")

        card =  dbc.Card([
            dbc.CardHeader(html.H2("Informações adicionais"), className="text-center"),
            dbc.CardBody([
                dbc.Row([dbc.Col(body_1)], className="text-center", style={"minHight": 250, "maxHight": 250})
            ])
        ])
    return card

def hist_votos(flag):
    fig = go.Figure()
    if flag == 'Todos':
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos EDNA DA IZIDORA'], x=data['zona'], marker={'color':'rgb(250, 125, 250)'}, name="Edna", legendgroup = '1'))
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos MARI FERNANDES'], x=data['zona'], marker={'color':'rgb(150, 75, 150)'}, name="Mari", legendgroup = '1'))
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos INDIRA XAVIER'], x=data['zona'], marker={'color':'rgb(100, 50, 100)'}, name="Indira", legendgroup = '1'))
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos ADRIEL DO MLB'], x=data['zona'], marker={'color':'rgb(50, 25, 50)'}, name="Adriel", legendgroup = '1'))
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos UP'], x=data['zona'], marker={'color':'rgb(100, 0, 100)'}, name="no partido", legendgroup = '1'))
        fig.update_layout(title=dict(text="Votos por zona"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Mari':
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos MARI FERNANDES'], x=data['zona'], marker={'color':'rgb(150, 75, 150)'}, name="Mari", legendgroup = '1'))
        fig.update_layout(title=dict(text="Votos por zona"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Edna':
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos EDNA DA IZIDORA'], x=data['zona'], marker={'color':'rgb(250, 125, 250)'}, name="Edna", legendgroup = '1'))
        fig.update_layout(title=dict(text="Votos por zona"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Adriel':
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos ADRIEL DO MLB'], x=data['zona'], marker={'color':'rgb(50, 25, 50)'}, name="Adriel", legendgroup = '1'))
        fig.update_layout(title=dict(text="Votos por zona"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Indira':
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos INDIRA XAVIER'], x=data['zona'], marker={'color':'rgb(100, 50, 100)'}, name="Indira", legendgroup = '1'))
        fig.update_layout(title=dict(text="Votos por zona"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig

def ocupacao_area(flag):
    fig = go.Figure()
    if flag == 'Adriel':
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL DO MLB'], x=votos_por_zona['zona'], marker={'color':'rgb(250, 0, 250)'}, name="Adriel",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL'], x=votos_por_zona['zona'], marker={'color':'rgb(150, 0, 0)'}, name="Edna e Adriel",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 200)'}, name="Adriel e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 150)'}, name="Adriel e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(50, 50, 50)'}, name="Adriel, Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.update_traces(marker_size=1)
        fig.update_layout(title=dict(text="Ocupação média de seções por zona"),
                          xaxis=dict(title=dict(text="Ocupação média")),
                          yaxis=dict(title=dict(text="Zona eleitoral")),
                          legend=dict(title=dict(text="Candidato"))
                         )
        return fig
    elif flag == 'Edna':
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA DA IZIDORA'], x=votos_por_zona['zona'], marker={'color':'rgb(250, 0, 0)'},fill='tozeroy', name="Edna", legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL'], x=votos_por_zona['zona'], marker={'color':'rgb(150, 0, 0)'}, name="Edna e Adriel",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(110, 0, 0)'}, name="Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(80, 0, 0)'}, name="Edna e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(50, 50, 50)'}, name="Adriel, Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.update_traces(marker_size=1)
        fig.update_layout(title=dict(text="Ocupação média de seções por zona"),
                            xaxis=dict(title=dict(text="Ocupação média")),
                            yaxis=dict(title=dict(text="Zona eleitoral")),
                            legend=dict(title=dict(text="Candidato"))
                            )
        return fig
    elif flag == 'Mari':
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao MARI FERNANDES'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 250)'}, name="Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(110, 0, 0)'}, name="Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 200)'}, name="Adriel e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao MARI + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 150, 0)'}, name="Mari e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(50, 50, 50)'}, name="Adriel, Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.update_traces(marker_size=1)
        fig.update_layout(title=dict(text="Ocupação média de seções por zona"),
                        xaxis=dict(title=dict(text="Ocupação média")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Indira':
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao INDIRA XAVIER'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 250, 0)'}, name="Indira",fill='tozeroy', legendgroup = '2'))
        fig.update_traces(marker_size=1)
        fig.update_layout(title=dict(text="Ocupação média de seções por zona"),
                        xaxis=dict(title=dict(text="Ocupação média")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    elif flag == 'Todos':
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA DA IZIDORA'], x=votos_por_zona['zona'], marker={'color':'rgb(250, 0, 0)'},fill='tozeroy', name="Edna", legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao MARI FERNANDES'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 250)'}, name="Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao INDIRA XAVIER'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 250, 0)'}, name="Indira",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL DO MLB'], x=votos_por_zona['zona'], marker={'color':'rgb(250, 0, 250)'}, name="Adriel",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao UP'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 0)'}, name="ideológicos",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao real do partido'], x=votos_por_zona['zona'], marker={'color':'rgb(150, 150, 150)'}, name="O partido",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL'], x=votos_por_zona['zona'], marker={'color':'rgb(150, 0, 0)'}, name="Edna e Adriel",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(110, 0, 0)'}, name="Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(80, 0, 0)'}, name="Edna e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 200)'}, name="Adriel e Mari",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao ADRIEL + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 0, 150)'}, name="Adriel e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao MARI + UP'], x=votos_por_zona['zona'], marker={'color':'rgb(0, 150, 0)'}, name="Mari e UP",fill='tozeroy', legendgroup = '2'))
        fig.add_trace(go.Scatter(y=votos_por_zona['ocupacao EDNA + ADRIEL + MARI'], x=votos_por_zona['zona'], marker={'color':'rgb(50, 50, 50)'}, name="Adriel, Edna e Mari",fill='tozeroy', legendgroup = '2'))
        fig.update_traces(marker_size=1)
        fig.update_layout(title=dict(text="Ocupação média de seções por zona"),
                        xaxis=dict(title=dict(text="Ocupação média")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend=dict(title=dict(text="Candidato"))
                        )
        return fig
    else:
        return{}



aspectos = ['O partido',
            'Adriel',
            'Edna',
            'Indira',
            'Mari',
            'Ver no mapa']

medidas = ['Mais medidas internas',
           'Comparações com outros partidos']

aspecto_radio = html.Div(
    [
        dbc.Label("Aspecto de análise", html_for="atividade-checklist"),
        dbc.RadioItems(
            options=aspectos,
            value='O partido',
            id='aspecto-radio',
        ),
    ],
    className="mb-4",
)

measure_radio = html.Div(
    [
        dbc.Label("Aspecto de análise", html_for="atividade-checklist"),
        dbc.RadioItems(
            options=medidas,
            value='Mais medidas internas',
            id='measure-radio',
        ),
    ],
    className="mb-4",
)

control_panel = dbc.Card(
    dbc.CardBody(
        [aspecto_radio],
        className="bg-light",
    ),
    className="mb-4"
)

control_panel_end = dbc.Card(
    dbc.CardBody(
        [measure_radio],
        className="bg-light",
    ),
    className="mb-4"
)

heading = html.H1("Analise do primeiro turno das eleições de 2024 em Belo Horizonte",className="bg-secondary text-white p-2 mb-4")


about_card = dcc.Markdown(
    """
    Reações variadas dominaram as redes após a divulgação dos resultados do primeiro turno das eleições municipais pelo Brasil 
    e muitas pessoas sugeriram diversas justificativas dos resultados e sugeriram novas estratégias que "virariam a mesa" em 
    termos de resultados eleitorais. 

    Embora seja absolutamente necessário que haja discussões sérias sobre resultados eleitorais, mesmo que sejam resultados numa 
    falsa democracia, no sentido de constante aprimoramento dos resultados e consequente ocupação de novos espaços (especialmente 
    espaços de poder), é chocante como nos recusamos a olhar os dados antes de elaborar qualquer discussão sobre o assunto. Neste 
    sentido, esta apresentação tem a função de trazer os números à discussão de maneira clara e comparada à campanha dos demais 
    partidos nos diversos campos políticos que participaram do certame para embasar novas estratégias de busca de apoio popular 
    transformado em votos, assim como aprimorar as estratégias e ações já adotadas.
    """
)

help_card = dcc.Markdown(
    """
    Alguns conceitos apresentados neste trabalho podem apresentar alguma dificuldade de compreenção devido a aspectos técnicos ou 
    mesmo devido a novidade de uso, logo é conveniente que sejam explicados e justificados com mais cuidado.

    O **voto ideológico**, o qual se faz referencia no trabalho, se trata de votos a vereança na legenda (80 no caso da UP) e são uma 
    medida indireta do nível de alinhamento ideológico com o partido, embora apresente também caráter ambíguo: é possivel que se votou 
    na legenda porque apesar de conhecer os candidatos a vereança, não se notou motivo forte o suficiente para se engajar com um candidato 
    apenas mas simpatiza com a luta do partido, o que seria uma fenômeno positivo para o futuro eleitoral do partido, ou; é possivel que se vota na legenda porque as informações 
    sobre as candidaturas não chegaram à pessoa, mas a pessoa conhece o partido de outras fontes, por exemplo das redes, o que caracteriza um fenômeno negativo para a saúde eleitoral do partido.


    O **custo declarado por voto** é a razão entre os custos declarados e o número de votos. Quando se refere a um candidato, os custos 
    e os votos se referem apenas a este candidato. Quando há a referencia a todos os candidatos à vereança, juntamos os custos e os votos
    registrados a vereança (neste caso, votos ideológicos são contabilizados e é atribuído a eles o valor 0 R$ de investimento). Finalmente, 
    quando é feita a referência de **todos**, implica que se faz referência aos candidatos a prefeitura **e** vereança.

    O **percentual de votos ideológicos** é a razão entre a quantidade de votos ideológicos com o total de votos a vereança no partido e é uma 
    medida indireta de compromisso ideológicos dos eleitores.

    O **percentual de ocupação de urnas** é a razão entre as urnas (ou seções) que apresentaram ao menos um voto no partido ou candidato contra o 
    número total de urnas (o que pode ser agrupado em zonas eleitorais). Em partidos conhecidos como PT e PL, a taxa de ocupação de urnas é 
    importante para se distinguir candidatos entre lideranças loais e lideranças regionais (mais sobre estes conceitos abaixo). No caso de 
    partidos que buscam o reconhecimento dos eleitores, como os partidos da esquerda radical, esta medida é importante para identificarmos a difusão
    das informações dos partidos pelas diversas regiões contempladas pelo pleito.

    A **votos a prefeitura por voto a vereança** se trata, como o nome sugere, na quantidade de votos ao candidato a prefeito dividido pelo total de votos 
    à vereança dos candidatos do partido. Se trata de uma medida indireta de identificação ideológica dos eleitores com os respectivos partidos assim como 
    uma medida indireta dos movimentos ideológicos dos eleitores. Valores maiores que um indicam que a quantidade de votos a prefeito supera a quantidade 
    de votos a vereança alcançada pelo próprio partido o que implica que eleitores de outros partidos identificaram o projeto deste partido específico como 
    representativo de seus anseios.

    As **correlações de votos (spearman)** são uma medida de co-variação dos resultados de dois candidatos. Um valor próximo de -1 indica que nos locais onde o 
    primeiro candidato tem uma votação expressiva, o segundo tem uma votação irrisória e vice-versa. Um valor perto de 1 indica que os locais de votação expressiva
    do primeiro candidato corresponde aos locais de votação expressiva do outro candidato assim como os locais de votação baixa também são correspondentes. Um valor 
    próximo de 0 indica que não se pode tirar tais conclusões. 

    As **lideranças locais** são candidatos que apresentam votação expressiva em certas cesões, geralmente hospedadas no mesmo local, mas que não apresentam resultados  
    em outras regiões, isto é, são candidatos com trabalho prévio na região e por isso são conhecidos localmente. Já **lideranças regionais** são candidatos que apresentam 
    votos em grandes porções do municipio. Uma forma de se diferenciar tais candidatos de forma objetiva é se montar a distribuição estatística dos votos pelas seções e se 
    medir o desvio padrão dos votos, que é uma medida de largura da distribuição. Lideranças locais tendem a ter uma distribuição de votos fina, decorrente do seu numero expressivo 
    contido em poucas seções ao passo que lideranças regionais apresentam números não despresíveis em comparação com o total em grande parte das seções. 

    """)

data_card = dcc.Markdown(
    """
    A busca por informações para a análise não foi fácil e foi preciso o acesso em 
    várias fontes distintas, a junção estratégica destes dados e a preparação para 
    análise. 
    
    Os dados relativos aos números brutos do pleito foram retirados do portal de dados abertos do TSE:
    [Fonte](https://dadosabertos.tse.jus.br/dataset/resultados-2024-boletim-de-urna)

    O endereço dos locais de votação por zona e seção não estavam disponíveis no portal de dados abertos 
    então foi preciso extraí-los diretamente de agentes de imprensa:
    [Fonte](https://g1.globo.com/mg/minas-gerais/eleicoes/2024/noticia/2024/10/28/resultados-do-2o-turno-por-local-de-votacao-em-belo-horizonte-nas-eleicoes-2024.ghtml)
    
    Os custos declarados dos candidatos foram retirados diretamente do TSE:
    [Fonte](https://divulgacandcontas.tse.jus.br/)

    Para os mapas, e geolocalização das escolas (coordenadas geográficas), assim como seus endereços, 
    foram necessárias consultas ao google maps usando o nome dos locais:
    [Fonte](https://www.google.com/maps)

    Para a representação dos mapas, é preciso dados especiais dos desenhos aproximados dos mapas que foi encontrado 
    no portal de dados abertos da prefeitura de Belo Horizonte:
    [Fonte](https://dados.pbh.gov.br/dataset?res_format=JSON&organization=prodabel_pbh)

    Finalmente, a geolocalização das zonas eleitorais foi especialmente desafiadora porque não existem 
    fronteiras fixas entre uma zona e outra no sentido que há entre bairros de forma que foi necessário 
    acessar o mapa de zonas eleitorais disponível no TSE:
    [Fonte](https://www.justicaeleitoral.jus.br/++theme++justica_eleitoral/pdfjs/web/viewer.html?file=https://www.justicaeleitoral.jus.br/arquivos/tre-mg-mapa-zonas-bh/@@download/file/mapa-zonas-bh.pdf).
     Atribuiu-se então, bairro a bairro, a zona eleitoral pertinente se os bairros em questão estavam no interior 
    da zona eleitoral (bulk) e atribuir às zonas de fronteira a zona com maior percentual do bairro. Na prática
    a diferença entre as zonas apresentadas nos mapas e as regiões inerentes às zonas eleitorais pertinentes se 
    diferenciam pouco.
    """
)

info = dbc.Accordion([
    dbc.AccordionItem(about_card, title="Informações pertinentes", ),
    dbc.AccordionItem(data_card, title="Fonte dos dados"),
    dbc.AccordionItem(help_card, title="Ajuda sobre os conceitos")
],  start_collapsed=True)

#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__)

layout = dbc.Container(
    [
        #dcc.Store(id="store-selected", data={}),
        heading,
        dbc.Row([
            dbc.Col([control_panel, info], md=3),
            dbc.Col(
                [
                    dcc.Markdown(id="title"),
                    dbc.Row([dbc.Col(html.Div(id="entrada-card"))]),# dbc.Col( html.Div(id="entrada-card"))]),
                    #html.Div(id="bar-chart-card", className="mt-4"),
                    html.Div(className='parent', children=[ dcc.Graph(id="main-chart"),
                    ]),
                    dcc.Markdown(id="title_end"),
                    html.Div(className='parent', children=[ dcc.Graph(id="secondary-chart"),
                    ]),
                ],  md=9
            ),
            dbc.Col(
                [
                    dbc.Row([dbc.Col([control_panel_end], md=3),dbc.Col(html.Div(id="saida-card"))]),# dbc.Col( html.Div(id="entrada-card"))]),
                    #html.Div(id="bar-chart-card", className="mt-4"),
                ],  md=12
            ),
        ]),
        #dbc.Row(dbc.Col( make_grid()), className="my-4")
    ],
    fluid=True,
)

@callback(
    Output("title", "children"),
    Input("aspecto-radio", "value")
)
def make_title(aspect):    
    title = f"""
    ## {aspect}
    ** Para mais informações, abra as caixas de diálogo**
    """
    return title

@callback(
    Output("entrada-card", "children"),
    Input("aspecto-radio", "value")
)
def make_card(aspecto):
    if aspecto == 'O partido':
        return card_UP()
    elif aspecto == 'Adriel':
        return card_Adriel()
    elif aspecto == 'Edna':
        return card_Edna()
    elif aspecto == 'Mari':
        return card_Mari()
    elif aspecto == 'Indira':
        return card_Indira()

@callback(
    Output("main-chart", "figure"), 
    Input("aspecto-radio", "value")
)
def grafico_principal(aspecto):
    
    if aspecto == 'Ver no mapa':
        return partido_map()
    elif aspecto == 'O partido':
        return hist_votos('Todos')
    elif aspecto == 'Adriel':
        return hist_votos('Adriel')
    elif aspecto == 'Edna':
        return hist_votos('Edna')
    elif aspecto == 'Mari':
        return hist_votos('Mari')
    elif aspecto == 'Indira':
        return hist_votos('Indira')
    


@callback(
    Output("title_end", "children"),
    Input("measure-radio", "value")
)
def make_title_end(measure):    
    title = f"""
    ## {measure}
    ** Fim **
    """
    return title

@callback(
    Output("saida-card", "children"),
    Input("measure-radio", "value"),
    Input("aspecto-radio", "value")
)
def make_card(measure, aspecto):
    if aspecto != 'O partido':
        return end_card_test('Indisponível')
    if measure == 'Mais medidas internas':
        return end_card_test('Interno')
    elif measure == 'Comparações com outros partidos':
        return end_card_test('Comparado')

        
@callback(
    Output("secondary-chart", "figure"), 
    Input("aspecto-radio", "value"),
    Input("measure-radio", "value")
)
def grafico_principal(aspecto, measure):
    if aspecto == 'Ver no mapa':
        return {}
    elif aspecto == 'O partido':
        return ocupacao_area('Todos')
    elif aspecto == 'Adriel':
        return ocupacao_area('Adriel')
    elif aspecto == 'Edna':
        return ocupacao_area('Edna')
    elif aspecto == 'Mari':
        return ocupacao_area('Mari')
    elif aspecto == 'Indira':
        return ocupacao_area('Indira')
    




    
#if __name__ == '__main__':
#    app.run(debug=True)


