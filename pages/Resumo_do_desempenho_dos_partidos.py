import dash
import json
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def float_to_currency(x):
    new = str(x).replace('.',',')
    if new.find(',')>0:
        [main, end] = new.split(',')
    else:
        [main, end] = [new, '']
    new = []
    if len(main)%3 > 0:
        new.append(main[:len(main)%3])
        main = main[len(main)%3:]
    while len(main) > 0:
        new.append(main[:3])
        main = main[3:]
    while len(end)<2:
        end = end+'0'
    return '.'.join(new)+','+end

id_map = pd.read_csv('data/teste_bh_dados.csv').reset_index()
#df = pd.read_csv('data/dados_tratados.csv').reset_index()
#df = df[df['cargo'] != '    Você aprova a alteração da bandeira  de Belo Horizonte?']
total_de_votos_por_partido = pd.read_csv('data/total_de_votos_por_partido_resumo.csv', sep=';').reset_index()
contagem_de_votos_ideológicos = pd.read_csv('data/contagem_de_votos_ideológicos_resumo.csv', sep=';').reset_index()
soma_votos_pref = pd.read_csv('data/soma_votos_pref_resumo.csv', sep=';').reset_index()
data_prefeitos_votos = pd.read_csv('data/data_prefeitos_votos_resumo.csv', sep=';').reset_index()
data_vereadores_votos = pd.read_csv('data/data_vereadores_votos_resumo.csv', sep=';').reset_index()
mais_votados_ver = pd.read_csv('data/mais_votados_ver_resumo.csv', sep=';').reset_index()
mais_votados = pd.read_csv('data/mais_votados_resumo.csv', sep=';').reset_index()
mais_votados_por_zona = pd.read_csv('data/mais_votados_por_zona_resumo.csv', sep=';').reset_index()
votos_por_zona_ver = pd.read_csv('data/votos_por_zona_ver_resumo.csv', sep=';').reset_index()
hist_all_data = pd.read_csv('data/hist_all_data_resumo.csv', sep=';').reset_index()
hist_all_data['zona'] = hist_all_data['zona'].astype(str)
pie_data = mais_votados_por_zona
partidos_prefeitura = list(set(data_prefeitos_votos['partido']))
partidos = list(set(data_vereadores_votos['partido'])) + ['Todos']
cargos = ['Prefeito', 'Vereador', 'Todos']

with open('data/variaveis_resumo.json', 'r') as file:
    variaveis = json.load(file)
with open('data/bairros_corrigido.json', 'r') as file:
        coord = json.load(file)

percentual_votos_nulos_pref = variaveis['percentual_votos_nulos_pref']
percentual_votos_esquerda_pref = variaveis['percentual_votos_esquerda_pref']
resultados_ver_dict = variaveis['resultados_ver_dict']
resultados_pref_dict = variaveis['resultados_pref_dict']
total_votos_pref = variaveis['total_votos_pref']
votos_total_brancos_nulos_ver = variaveis['votos_total_brancos_nulos_ver']
total_votos_ver = variaveis['total_votos_ver']
votos_total_esquerda_ver = variaveis['votos_total_esquerda_ver']
ranking_ver_dic = variaveis['ranking_ver_dic']
comparecimento_total = variaveis['comparecimento_total']
capacidade_total = variaveis['capacidade_total']
percentual_de_comparecimento = variaveis['percentual_de_comparecimento']
total_de_votos_no_partido = variaveis['total_de_votos_no_partido']
total_de_votos = variaveis['total_de_votos']
votos_ideologicos = variaveis['votos_ideologicos']

matriz_de_valores = []
data_prefeitos_votos['zona'] = data_prefeitos_votos['zona'].astype(str)
zona_heatmap = list(set(data_prefeitos_votos['zona']))
for partido in partidos_prefeitura:
    vars = []
    for zona in zona_heatmap:
        vars.append(int(sum(data_prefeitos_votos[(data_prefeitos_votos['partido']==partido)&(data_prefeitos_votos['zona']==zona)]['votos'])))
    matriz_de_valores.append(vars)



def cards_components(mode, entries, partido, texto_1, texto_2):
    titnome_11 = entries[0][0]
    titnome_12 = entries[0][1]
    titnome_13 = entries[0][2]
    titval_21 = entries[1][0]
    titval_22 = entries[1][1]
    titval_23 = entries[1][2]
    titval_31 = entries[2][0]
    titval_32 = entries[2][1]
    titval_33 = entries[2][2]
    if mode == 1:
        titulo_1 = 'Zona eleitoral com melhor performance'
        titulo_2 = 'Votos contabilizados pelo partido na zona eleitoral'    
        titulo_3 = 'Percentual em relação ao total de votos contabilizados na zona eleitoral'
    elif mode == 0:
        titulo_1 = 'Candidatos a prefeitura mais votados'
        titulo_2 = 'Partidos'    
        titulo_3 = 'Percentual de votos em relação ao total'
    elif mode == 2:
        titnome_14 = entries[0][3]
        titnome_15 = entries[0][4]
        titnome_16 = entries[0][5]
        titnome_17 = entries[0][6]
        titnome_18 = entries[0][7]
        titnome_19 = entries[0][8]
        titnome_110 = entries[0][9]
        titval_24 = entries[1][3]
        titval_25 = entries[1][4]
        titval_26 = entries[1][5]
        titval_27 = entries[1][6]
        titval_28 = entries[1][7]
        titval_29 = entries[1][8]
        titval_210 = entries[1][9]
        titval_34 = entries[2][3]
        titval_35 = entries[2][4]
        titval_36 = entries[2][5]
        titval_37 = entries[2][6]
        titval_38 = entries[2][7]
        titval_39 = entries[2][8]
        titval_310 = entries[2][9]
        titval_41 = entries[3][0]
        titval_42 = entries[3][1]
        titval_43 = entries[3][2]
        titval_44 = entries[3][3]
        titval_45 = entries[3][4]
        titval_46 = entries[3][5]
        titval_47 = entries[3][6]
        titval_48 = entries[3][7]
        titval_49 = entries[3][8]
        titval_410 = entries[3][9]

        titulo_1 = 'Candidato votado'
        titulo_2 = 'Votos contabilizados'    
        titulo_3 = 'Partido'
        titulo_4 = 'Gasto declarado ao TSE (R$)'
        paygap = dbc.Row([
                    dbc.Col([
                        html.Div(titulo_1, className=" border-bottom border-3"),
                        html.Div(titnome_11),
                        html.Div(titnome_12),
                        html.Div(titnome_13),
                        html.Div(titnome_14),
                        html.Div(titnome_15),
                        html.Div(titnome_16),
                        html.Div(titnome_17),
                        html.Div(titnome_18),
                        html.Div(titnome_19),
                        html.Div(titnome_110)
                    ], style={"minWidth": 250}),
                    dbc.Col([
                        html.Div(titulo_2, className=" border-bottom border-3"),
                        html.Div(titval_21),
                        html.Div(titval_22),
                        html.Div(titval_23),
                        html.Div(titval_24),
                        html.Div(titval_25),
                        html.Div(titval_26),
                        html.Div(titval_27),
                        html.Div(titval_28),
                        html.Div(titval_29),
                        html.Div(titval_210)
                    ]),
                    dbc.Col([
                        html.Div(titulo_3, className=" border-bottom border-3"),
                        html.Div(titval_31),
                        html.Div(titval_32),
                        html.Div(titval_33),
                        html.Div(titval_34),
                        html.Div(titval_35),
                        html.Div(titval_36),
                        html.Div(titval_37),
                        html.Div(titval_38),
                        html.Div(titval_39),
                        html.Div(titval_310)
                    ]),
                    dbc.Col([
                        html.Div(titulo_4, className=" border-bottom border-3"),
                        html.Div(float_to_currency(titval_41)),
                        html.Div(float_to_currency(titval_42)),
                        html.Div(float_to_currency(titval_43)),
                        html.Div(float_to_currency(titval_44)),
                        html.Div(float_to_currency(titval_45)),
                        html.Div(float_to_currency(titval_46)),
                        html.Div(float_to_currency(titval_47)),
                        html.Div(float_to_currency(titval_48)),
                        html.Div(float_to_currency(titval_49)),
                        html.Div(float_to_currency(titval_410))
                    ], style={"minWidth": 250}),
                ], style={"minWidth": 400}
                )
        mean = dbc.Alert(dcc.Markdown(
                texto_1,
            ), color="dark")

        median = dbc.Alert(dcc.Markdown(
                texto_2,
            ), color="dark")
        return paygap, mean, median
    elif mode == 3:
        titulo_1 = 'Candidatos a vereança mais votados do partido ' + partido
        titulo_2 = 'Percentual de votos em relação ao total (do partido)'    
        titulo_3 = 'Desvio padrão da contagem de votos'
    elif mode == 4:
        titulo_1 = 'Partidos mais votados'
        titulo_2 = 'Numero de votos contabilizados'    
        titulo_3 = 'Percentual de votos em relação ao total'
    elif mode == 5:
        titulo_1 = 'Zonas eleitorais'
        titulo_2 = 'Votos contabilizados no partido'    
        titulo_3 = 'Percentual de votos em relação ao total de votos no partido'
    elif mode == 6:
        titulo_1 = 'Não se aplica'
        titulo_2 = 'Não se aplica'
        titulo_3 = 'Não se aplica'
    paygap = dbc.Row([
                dbc.Col([
                    html.Div(titulo_1, className=" border-bottom border-3"),
                    html.Div(titnome_11),
                    html.Div(titnome_12),
                    html.Div(titnome_13)
                ], style={"minWidth": 250}),
                dbc.Col([
                    html.Div(titulo_2, className=" border-bottom border-3"),
                    html.Div( f"{titval_21}"),
                    html.Div(f"{titval_22}"),
                    html.Div(f"{titval_23}"),
                ]),
                dbc.Col([
                    html.Div(titulo_3, className=" border-bottom border-3"),
                    html.Div(f"{titval_31}"),
                    html.Div(f"{titval_32}"),
                    html.Div(f"{titval_33}"),
                ])
            ], style={"minWidth": 400})

    mean = dbc.Alert(dcc.Markdown(
            #f"""
            #** Mean Pay **  
            #### {70}  
            #Higher for men
            #""",
            texto_1,
        ), color="dark")

    median = dbc.Alert(dcc.Markdown(
            #f"""
            #    ** Median Pay ** 
            #    ### {80}  
            #    Higher for men
            #    """,
            texto_2,
        ), color="dark")

    return paygap, mean, median

def card_none():
    ent=[
        ['não se aplica' for _ in range(3)],
        ['não se aplica' for _ in range(3)],
        ['não se aplica' for _ in range(3)]
    ]
    texto_1 = f"""
                ** -- ** 
                ### O partido não participa do certame à prefeitura
                """
    paygap, mean, median = cards_components(mode=0, entries=ent, partido=None,
                                            texto_1=texto_1, texto_2=texto_1)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Numeros brutos"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_0_body(partido):
    ent=[
        list(soma_votos_pref['nome'])[:3],
        list(soma_votos_pref['partido'])[:3],
        list(soma_votos_pref['percentual'])[:3]
    ]
    texto_1 = f"""
                ** Percentual de votos nulos e brancos ** 
                ### {percentual_votos_nulos_pref}%
                """
    texto_2 = f"""
                ** Percentual de votos na esquerda (UP + PT + PDT + PSTU)** 
                ### {percentual_votos_esquerda_pref}%  
                """

    paygap, mean, median = cards_components(mode=0, entries=ent, partido=partido,
                                            texto_1=texto_1, texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Numeros brutos"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_1_body(partido):
    
    if partido not in partidos_prefeitura:
        return card_none()
    else:
        
        ent=[
            resultados_pref_dict[partido]['zona'],
            resultados_pref_dict[partido]['votos'],
            resultados_pref_dict[partido]['percentual']
        ]
        vp = resultados_pref_dict[partido]['total']
        vv = resultados_ver_dict[partido]['total']
        texto_1 = f"""
                    ** Votos a vereança por voto para prefeito** 
                    ### {round(vv/vp,2)}  
                    """
        
        texto_2 = f""" 
                    ** Percentual de votos à prefeitura** 
                    ### {round(100*vp/total_votos_pref,2)}%
                    """
        paygap, mean, median = cards_components(mode=1, entries=ent, partido=partido,
                                                texto_1=texto_1, texto_2=texto_2)
        card =  dbc.Card([
            dbc.CardHeader(html.H2("Numeros brutos"), className="text-center"),
            dbc.CardBody([
                dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
                paygap
            ])#,
            #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
        ])
        return card

def card_2_body(partido):
    ent=[
        list(mais_votados_ver['nome']),
        list(mais_votados_ver['votos']),
        list(mais_votados_ver['partido']),
        list(mais_votados_ver['investimento declarado'])
    ]
    texto_1 = f"""
                ** Percentual de votos nulos e brancos com relação à vereança** 
                ### {round(100*votos_total_brancos_nulos_ver/total_votos_ver,2)}% 
                """
    texto_2 = f"""
                ** percentual de votos na esquerda (UP + PT + PDT + PCB + PCdoB + PSOL + PSTU + PSB) à vereança em relação ao total de votos ao pleito** 
                ### {round(100*votos_total_esquerda_ver/total_votos_ver,2)}%  
                """

    paygap, mean, median = cards_components(mode=2, entries=ent, partido=partido,
                                            texto_1=texto_1, texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Numeros brutos"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_3_body(partido):
    somas_votos_partido = list(total_de_votos_por_partido[total_de_votos_por_partido['partido']==partido]['votos'])[0]
    votos_ideologicos = list(contagem_de_votos_ideológicos[contagem_de_votos_ideológicos['nome']==partido]['votos'])[0]
    ent=[
        ranking_ver_dic[partido]['nome'],
        [round(100*i/somas_votos_partido,2) for i in ranking_ver_dic[partido]['votos']],
        [round(i,4) for i in ranking_ver_dic[partido]['std']]
    ]
    texto_1 = f"""
                ** total de votos no partido {partido}** 
                ### {int(somas_votos_partido)}  
                """
    texto_2 = f"""
                ** percentual de votos ideológicos no partido {partido}** 
                ### {round(100*votos_ideologicos/somas_votos_partido,2)}%
            """
    paygap, mean, median = cards_components(mode=3, entries=ent, partido=partido,
                                            texto_1=texto_1, texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Desempenho do partido"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])
    return card

def card_4_body(partido):
    
    ent=[
        list(mais_votados['partido'])[:3],
        list(mais_votados['votos'])[:3],
        [round(i/mais_votados['votos'].sum(),2) for i in list(mais_votados['votos'][:3])]
    ]
    texto_1 = f"""
                ** Capacidade atual de todas as seções somadas** 
                ### {int(capacidade_total)}  
                """
    texto_2 = f"""
                ** percentual de comparecimento nas seções em relação à capacidade total somada** 
                ### {round(100*percentual_de_comparecimento,2)} %
                """

    paygap, mean, median = cards_components(mode=4, entries=ent, partido=partido,
                                            texto_1=texto_1, texto_2=texto_2)
    card =  dbc.Card([
        dbc.CardHeader(html.H2("Resumo"), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
            paygap
        ])#,
        #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
    ])

    return card

def card_5_body(partido):
    if partido not in partidos_prefeitura:
        return card_3_body(partido)
    else:
        temp = pie_data[pie_data['partido']==partido].sort_values(by='votos', ascending=False)
        ent=[
            list(temp['zona'])[:3],
            [int(i) for i in list(temp['votos'])[:3]],
            [round(i*100,2) for i in list(temp['percentual'])[:3]]
        ]
        texto_1 = f"""
                    ** Percentual de votos em relação à soma de todos os partidos** 
                    ### {round(100*total_de_votos_no_partido/total_de_votos,2)}%  
                    """
        texto_2 = f"""
                    ** Percentual de votos ideológicos no partido** 
                    ### {round(100*votos_ideologicos/total_de_votos_no_partido,2)} %
                    """


        paygap, mean, median = cards_components(mode=4, entries=ent, partido=partido,
                                                texto_1=texto_1, texto_2=texto_2)
        card =  dbc.Card([
            dbc.CardHeader(html.H2("Resumo"), className="text-center"),
            dbc.CardBody([
                dbc.Row([dbc.Col(mean), dbc.Col(median)], className="text-center"),
                paygap
            ])#,
            #dbc.Row([dbc.Col(mean), dcc.Graph(id="polar-chord")], className="text-center"),
        ])

        return card

def hist_map(partido, cargo):
    if cargo == 'Prefeito':
        data = data_prefeitos_votos[data_prefeitos_votos['partido']==partido]
        data['zona'] = data['zona'].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos'], x=data['zona'], marker={'color':'rgb(150, 75, 150)'}, name=partido))
        fig.update_layout(title=dict(text=f"Votos por zona contabilizados ao partido {partido} no certame à prefeitura"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend={'title':{'text':'Partido'}}
                        )
        return fig
    elif cargo == 'Vereador' or cargo == 'Todos':
        data = data_vereadores_votos[data_vereadores_votos['partido']==partido]
        data['zona'] = data['zona'].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Histogram(histfunc="sum", y=data['votos'], x=data['zona'], marker={'color':'rgb(150, 75, 150)'}))
        fig.update_layout(title=dict(text=f"Votos por zona contabilizados ao partido {partido} no certame à vereança"),
                        xaxis=dict(title=dict(text="Soma dos votos")),
                        yaxis=dict(title=dict(text="Zona eleitoral")),
                        legend={'title':{'text':'Partido'}}
                        )
        return fig
    else:
        return {}

def heat_map():
    fig = px.imshow(matriz_de_valores,
                    labels=dict(x="Zona eleitoral", y="Partido",
                    color="Total de votos contabilizados"),
                    y=partidos_prefeitura,
                    x=zona_heatmap,
                    #color_continuous_scale=px.colors.cyclical.IceFire,
                    text_auto=True)
    fig.update_layout(
    title=dict(text="""Votos contabilizados para a prefeitura por partidos por zona eleitoral""",
                    font=dict(size=20), automargin=True))
    return fig

def pie_chart(partido):
    aux_0, aux_1 = data_prefeitos_votos[data_prefeitos_votos['partido']==partido][['votos']], data_vereadores_votos[data_vereadores_votos['partido']==partido][['votos']]
    aux_0['cargo'], aux_1['cargo'] = ['Prefeito' for _ in range(aux_0.shape[0])], ['Vereador' for _ in range(aux_1.shape[0])]
    fig = px.pie(pd.concat([aux_0, aux_1]), values='votos', names='cargo', title='Votos a prefeitura e vereaça atrelados ao partido')
    return fig

def map(partido):
    data = votos_por_zona_ver[votos_por_zona_ver['partido']==partido]
    data['zona'] = data['zona'].astype(str)
    dados = id_map.set_index('zona').join(data.set_index('zona'), on='zona', how='left', rsuffix='_r', lsuffix='_l').reset_index()
    fig = px.choropleth_map(dados, geojson=coord, color='votos',
                                locations="id", featureidkey="properties.ID",
                                center={"lat": -19.912998, "lon": -43.940933},
                                zoom=10,
                                hover_data={'nome':True, 'zona':True,
                                            'votos':True,
                                            'partido':True,
                                            'id':False})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(
    title=dict(text="""Mapa de BH colorido de acordo com a quantidade dos votos do partido por zona""",
                    font=dict(size=20), automargin=True))
    fig.update_traces(marker={"opacity":0.6})
    return fig

def all_hist_graf():
    fig = px.bar(hist_all_data, x="zona",
                y='votos para prefeito por votos para vereador',
                color='partido', pattern_shape='partido',
                labels={"zona":'Zona eleitoral',
                        'votos para vereador por votos para prefeito':"Razão entre votos para vereador e votos para prefeito",
                        'partido':'Partido'})

    return fig

partido_dropdown = html.Div(
    [
        dbc.Label("Selecione o partido", html_for="dropdown_partido"),
        dcc.Dropdown(
            id="partido-dropdown",
            options=partidos,
            value='Todos',
            clearable=False,
            maxHeight=600,
            optionHeight=50
        ),
    ],  className="mb-4",
)

atividade_radio = html.Div(
    [
        dbc.Label("Selecione a atividade", html_for="atividade-checklist"),
        dbc.RadioItems(
            options=cargos,
            value='Prefeito',
            id="cargos-radio",
        ),
    ],
    className="mb-4",
)

control_panel = dbc.Card(
    dbc.CardBody(
        [atividade_radio, partido_dropdown],
        className="bg-light",
    ),
    className="mb-4"
)

heading = html.H1("Analise do primeiro turno das eleições de 2024 em Belo Horizonte",className="bg-secondary text-white p-2 mb-4")

about_card = dcc.Markdown(
    """
    Os gráficos e cartões apresentados nesta página e nas demais são interativos, isto é, apresentam capacidades de apresentar mais informações ou mudar a sua própria forma quando selecionamos diferentes entradas nas listas de opções localizadas no lado esquerdo dos painéis. É recomendado a plena exploração dessas características.
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

dash.register_page(__name__)
#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container(
    [
        dcc.Store(id="store-selected", data={}),
        heading,
        dbc.Row([
            dbc.Col([control_panel, info], md=3),
            dbc.Col(
                [
                    dcc.Markdown(id="title_resumo"),
                    dbc.Row([dbc.Col(html.Div(id="entrada-card-resumo"))]),# dbc.Col( html.Div(id="entrada-card-resumo"))]),
                    #html.Div(id="bar-chart-card", className="mt-4"),
                    html.Div(className='parent', children=[ dcc.Graph(id="map-chart"),
                    ]),
                ],  md=9
            ),
        ]),
        #dbc.Row(dbc.Col( make_grid()), className="my-4")
    ],
    fluid=True,
)

@callback(
    Output("title_resumo", "children"),
    Input("partido-dropdown", "value"),
    Input("cargos-radio", "value")
)
def make_title(partido, cargo):    
    if cargo == 'Todos' and partido == 'Todos':
        title = f"""
        ## Resultados relativos a todos os dados
        ** Para mais informações, abra as caixas de diálogo**
        """          
    elif cargo == 'Todos':
        title = f"""
        ## Resultados relativos a todos os cargos do partido {partido}
        ** Para mais informações, abra as caixas de diálogo**
        """
    elif partido == 'Todos':
        title = f"""
        ## Resultados relativos ao cargo {cargo} considerando todos os partidos
        ** Para mais informações, abra as caixas de diálogo**
        """
    else:
        title = f"""
        ## Resultados relativos ao cargo {cargo} do partido {partido}
        ** Para mais informações, abra as caixas de diálogo**
        """
    return title

@callback(
    Output("entrada-card-resumo", "children"),
    Input("partido-dropdown", "value"),
    Input("cargos-radio", "value")
)
def make_card(partido, cargo):
    if cargo == 'Prefeito':
        if partido == 'Todos':
            card = card_0_body(partido)
        else:
            card = card_1_body(partido)
    elif cargo == 'Vereador':
        if partido == 'Todos':
            card = card_2_body(partido)
        else:
            card = card_3_body(partido)
    elif cargo == 'Todos':
        if partido == 'Todos':
            card = card_4_body(partido)
        else: 
            card = card_5_body(partido)
    else:
        print('error:', partido, cargo)
        return None
    return card

@callback(
    Output("map-chart", "figure"), 
    Input("partido-dropdown", "value"),
    Input("cargos-radio", "value")
)
def display_map(partido, cargo):
    if cargo == 'Prefeito':
        if partido == 'Todos':
            return heat_map()
        else: 
            if partido in partidos_prefeitura:
                return hist_map(partido, cargo)
            else:
                return {}
    elif cargo == 'Vereador':
        if partido == 'Todos':
            return {}
        else:
            return map(partido)
    else:
        if partido == 'Todos':
            return all_hist_graf()
        else:
            if partido in partidos_prefeitura:
                return pie_chart(partido)
            else:
                return hist_map(partido, cargo)

 
#if __name__ == '__main__':
#    app.run(debug=True)


