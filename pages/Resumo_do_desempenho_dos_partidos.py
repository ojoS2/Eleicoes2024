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
df = pd.read_csv('data/dados_tratados.csv').reset_index()
df = df[df['cargo'] != '    Você aprova a alteração da bandeira  de Belo Horizonte?']
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
    fig = px.pie(df[df['partido']==partido], values='votos', names='cargo', title='Votos a prefeitura e vereaça atrelados ao partido')
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
    The gender pay gap does not measure equal pay, instead it measures the difference between men and
    women's average and median hourly pay.  Equal pay, on the other hand, is the legal obligation under the Employment
    Equality Acts that requires  employers to give men and women equal pay if they are employed to do equal work. 
    
    Note that there is no equivalent reporting requirement in the US. Refer to this [US Department of Labour brief](https://www.dol.gov/sites/dolgov/files/WB/equalpay/WB_issuebrief-undstg-wage-gap-v1.pdf)
    which notes that "regardless of the gender composition of jobs, women tend to be paid less on average than men in the
    same occupation even when working full time."
    """)

help_card = dcc.Markdown(
    """
    Ajuda sobre o que é mostrado
    """)

data_card = dcc.Markdown(
    """
    Starting from 2022, Gender Pay Gap Reporting is a regulatory requirement that mandates employers in Ireland with
    more than 250 employees to publish information on their gender pay gap.
    
    [Data source](https://paygap.ie/)
    
    [Data source GitHub](https://github.com/zenbuffy/irishGenderPayGap/tree/main)
    
    This site was created for Plotly's Figure Friday challenge. For additional data visualizations of this dataset and
    to join the conversation, visit the [Plotly Community Forum](https://community.plotly.com/t/figure-friday-2024-week-32/86401)
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


