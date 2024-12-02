import pandas as pd
import json
from statistics import stdev
import plotly.graph_objects as go

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
eleitos_PL = ['MARILDA PORTELA', 'SARGENTO JALYSON', 'CLAUDIO DO MUNDO NOVO', 'UNER AUGUSTO', 'VILE', 'PABLO ALMEIDA']
eleitos_PT = ['PEDRO ROUSSEFF', 'DR BRUNO PEDRALVA', 'LUIZA DULCI', 'PEDRO PATRUS']
def load_data():
    df = pd.read_csv('data/dados_tratados.csv').reset_index()
    df['secao'] = (df['secao'].astype(int)).astype(str)
    df['zona'] = (df['zona'].astype(int)).astype(str)
    df = df[df['cargo'] != '    Você aprova a alteração da bandeira  de Belo Horizonte?']
    with open('data/bairros_corrigido.json', 'r') as file:
        coords_file = json.load(file)
    return df, coords_file
#cards data
df, coord = load_data()
id_map = pd.read_csv('data/teste_bh_dados.csv').reset_index()


pref_inv_df = df[df['partido']=='UP'][['nome', 'votos']]
pref_inv_df = pref_inv_df.groupby('nome').sum().reset_index()
pref_inv_df['custo total'] = [investimentos_dict[i] for i in pref_inv_df['nome']]
pref_inv_df['custo do voto'] = pref_inv_df['custo total']/pref_inv_df['votos']
custo_todos_os_votos = sum(pref_inv_df['votos'])/sum(pref_inv_df['custo total'])
secoes_zonas = df[['zona', 'secao']].drop_duplicates()
candidatos = df[df['partido']=='UP'][['zona', 'secao', 'nome', 'votos']].drop_duplicates()

dfs = []
for nome in ['MARI FERNANDES', 'EDNA DA IZIDORA', 'ADRIEL DO MLB', 'UP', 'INDIRA XAVIER']:
    temp = candidatos[candidatos['nome']==nome][['votos', 'zona', 'secao']]
    temp['ocupacao ' + nome] = [1 for _ in range(temp.shape[0])]
    temp['votos ' + nome] = temp['votos']
    temp = temp[['zona', 'secao', 'ocupacao ' + nome, 'votos ' + nome]]
    dfs.append(secoes_zonas.set_index(['zona', 'secao']).join(temp.set_index(['zona', 'secao']),
              on=['zona', 'secao'], how='left').reset_index().fillna(0))
data = dfs[0].set_index(['zona', 'secao']).join(dfs[1].set_index(['zona', 'secao']),
                                                on=['zona', 'secao']).reset_index()
data = data.set_index(['zona', 'secao']).join(dfs[2].set_index(['zona', 'secao']),
                                                on=['zona', 'secao']).reset_index()
data = data.set_index(['zona', 'secao']).join(dfs[3].set_index(['zona', 'secao']),
                                                on=['zona', 'secao']).reset_index()
data = data.set_index(['zona', 'secao']).join(dfs[4].set_index(['zona', 'secao']),
                                                on=['zona', 'secao']).reset_index()
data['ocupacao real do partido'] = data['ocupacao MARI FERNANDES']+\
                                   data['ocupacao EDNA DA IZIDORA']+\
                                   data['ocupacao ADRIEL DO MLB']+\
                                   data['ocupacao UP']+\
                                   data['ocupacao INDIRA XAVIER']
data['ocupacao real do partido'] = [int(i>0) for i in data['ocupacao real do partido']]
data['ocupacao EDNA + ADRIEL'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao EDNA DA IZIDORA'],data['ocupacao ADRIEL DO MLB'])]
data['ocupacao EDNA + MARI'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao EDNA DA IZIDORA'],data['ocupacao MARI FERNANDES'])]
data['ocupacao EDNA + UP'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao EDNA DA IZIDORA'],data['ocupacao UP'])]
data['ocupacao ADRIEL + MARI'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao ADRIEL DO MLB'],data['ocupacao MARI FERNANDES'])]
data['ocupacao ADRIEL + UP'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao ADRIEL DO MLB'],data['ocupacao UP'])]
data['ocupacao MARI + UP'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao MARI FERNANDES'],data['ocupacao UP'])]
data['ocupacao EDNA + ADRIEL + MARI'] = [int((i>0)&(j>0)&(k>0)) for i,j,k in zip(data['ocupacao EDNA DA IZIDORA'],data['ocupacao ADRIEL DO MLB'],data['ocupacao MARI FERNANDES'])]
data['ocupacao EDNA + ADRIEL + MARI + UP'] = [int((i>0)&(j>0)&(k>0)&(l>0)) for i,j,k,l in zip(data['ocupacao EDNA DA IZIDORA'],data['ocupacao ADRIEL DO MLB'],data['ocupacao MARI FERNANDES'],data['ocupacao UP'])]
data['ocupacao INDIRA + ADRIEL'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao INDIRA XAVIER'],data['ocupacao ADRIEL DO MLB'])]
data['ocupacao INDIRA + EDNA'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao INDIRA XAVIER'],data['ocupacao EDNA DA IZIDORA'])]
data['ocupacao INDIRA + MARI'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao INDIRA XAVIER'],data['ocupacao MARI FERNANDES'])]
data['ocupacao INDIRA + UP'] = [int((i>0)&(j>0)) for i,j in zip(data['ocupacao INDIRA XAVIER'],data['ocupacao UP'])]

data_voto = data[['zona', 'votos ADRIEL DO MLB', 'votos EDNA DA IZIDORA', 'votos INDIRA XAVIER', 'votos MARI FERNANDES', 'votos UP']]
votos = data_voto.groupby('zona').sum().reset_index()
votos['votos no partido'] = votos.iloc[:,1]+votos.iloc[:,2]+votos.iloc[:,3]+votos.iloc[:,4]+votos.iloc[:,5]
data_ocupacao = data[['zona', 'ocupacao real do partido', 'ocupacao ADRIEL DO MLB',
                      'ocupacao EDNA DA IZIDORA', 'ocupacao INDIRA XAVIER', 'ocupacao MARI FERNANDES',
                      'ocupacao UP', 'ocupacao EDNA + ADRIEL','ocupacao EDNA + MARI', 
                      'ocupacao EDNA + UP', 'ocupacao ADRIEL + MARI', 'ocupacao ADRIEL + UP',
                      'ocupacao MARI + UP', 'ocupacao EDNA + ADRIEL + MARI', 'ocupacao EDNA + ADRIEL + MARI + UP',
                      'ocupacao INDIRA + ADRIEL','ocupacao INDIRA + EDNA', 'ocupacao INDIRA + MARI',
                      'ocupacao INDIRA + UP'
                      ]]

ocupacao = data_ocupacao.groupby('zona').mean().reset_index()
std_Adriel = stdev(data_voto['votos ADRIEL DO MLB'])
std_Edna = stdev(data_voto['votos EDNA DA IZIDORA'])
std_Indira = stdev(data_voto['votos INDIRA XAVIER'])
std_Mari = stdev(data_voto['votos MARI FERNANDES'])
std_UP = stdev(data_voto['votos UP'])

votos_por_zona=votos.set_index(['zona']).join(ocupacao.set_index(['zona']), on='zona', how='outer').reset_index()
votos_por_zona_Adriel = votos_por_zona[['zona', 'votos ADRIEL DO MLB', 'ocupacao ADRIEL DO MLB']].sort_values(by='votos ADRIEL DO MLB', ascending=False)
votos_por_zona_Edna = votos_por_zona[['zona', 'votos EDNA DA IZIDORA', 'ocupacao EDNA DA IZIDORA']].sort_values(by='votos EDNA DA IZIDORA', ascending=False)
votos_por_zona_Mari = votos_por_zona[['zona', 'votos MARI FERNANDES', 'ocupacao MARI FERNANDES']].sort_values(by='votos MARI FERNANDES', ascending=False)
votos_por_zona_Indira = votos_por_zona[['zona', 'votos INDIRA XAVIER', 'ocupacao INDIRA XAVIER']].sort_values(by='votos INDIRA XAVIER', ascending=False)
votos_por_zona_Up = votos_por_zona[['zona', 'votos UP', 'ocupacao UP']].sort_values(by='votos UP', ascending=False)

# variaveis
# melhores desempenhos
melhor_Adriel = df[df['nome']=='ADRIEL DO MLB'].sort_values(by='votos',ascending=False)
temp = melhor_Adriel[['local', 'votos']].groupby('local').sum().reset_index().set_index('local')
melhor_Adriel = temp.join(melhor_Adriel[['local', 'coordenadas']].set_index('local'), on='local', how='left').reset_index()
melhor_Adriel = melhor_Adriel.drop_duplicates('local').sort_values(by='votos',ascending=False)
melhor_Ad_local_1, melhor_Ad_local_2 = melhor_Adriel.iloc[0,0], melhor_Adriel.iloc[1,0]
melhor_Ad_coord_1, melhor_Ad_coord_2 = melhor_Adriel.iloc[0,2].split(', '), melhor_Adriel.iloc[1,2].split(', ')
melhor_Ad_votos_1, melhor_Ad_votos_2 = melhor_Adriel.iloc[0,1], melhor_Adriel.iloc[1,1]
melhor_Edna = df[df['nome']=='EDNA DA IZIDORA'].sort_values(by='votos',ascending=False)
temp = melhor_Edna[['local', 'votos']].groupby('local').sum().reset_index().set_index('local')
melhor_Edna = temp.join(melhor_Edna[['local', 'coordenadas']].set_index('local'), on='local', how='left').reset_index()
melhor_Edna = melhor_Edna.drop_duplicates('local').sort_values(by='votos',ascending=False)
melhor_Ed_local_1, melhor_Ed_local_2 = melhor_Edna.iloc[0,0], melhor_Edna.iloc[1,0]
melhor_Ed_coord_1, melhor_Ed_coord_2 = melhor_Edna.iloc[0,2].split(', '), melhor_Edna.iloc[1,2].split(', ')
melhor_Ed_votos_1, melhor_Ed_votos_2 = melhor_Edna.iloc[0,1], melhor_Edna.iloc[1,1]
melhor_Indira = df[df['nome']=='INDIRA XAVIER'].sort_values(by='votos',ascending=False)
temp = melhor_Indira[['local', 'votos']].groupby('local').sum().reset_index().set_index('local')
melhor_Indira = temp.join(melhor_Indira[['local', 'coordenadas']].set_index('local'), on='local', how='left').reset_index()
melhor_Indira = melhor_Indira.drop_duplicates('local').sort_values(by='votos',ascending=False)
melhor_Id_local_1, melhor_Id_local_2 = melhor_Indira.iloc[0,0], melhor_Indira.iloc[1,0]
melhor_Id_coord_1, melhor_Id_coord_2 = melhor_Indira.iloc[0,2].split(', '), melhor_Indira.iloc[1,2].split(', ')
melhor_Id_votos_1, melhor_Id_votos_2 = melhor_Indira.iloc[0,1], melhor_Indira.iloc[1,1]
melhor_Mari = df[df['nome']=='MARI FERNANDES'].sort_values(by='votos',ascending=False)
temp = melhor_Mari[['local', 'votos']].groupby('local').sum().reset_index().set_index('local')
melhor_Mari = temp.join(melhor_Mari[['local', 'coordenadas']].set_index('local'), on='local', how='left').reset_index()
melhor_Mari = melhor_Mari.drop_duplicates('local').sort_values(by='votos',ascending=False)
melhor_Ma_local_1, melhor_Ma_local_2 = melhor_Mari.iloc[0,0], melhor_Mari.iloc[1,0]
melhor_Ma_coord_1, melhor_Ma_coord_2 = melhor_Mari.iloc[0,2].split(', '), melhor_Mari.iloc[1,2].split(', ')
melhor_Ma_votos_1, melhor_Ma_votos_2 = melhor_Mari.iloc[0,1], melhor_Mari.iloc[1,1]
melhor_UP = df[df['nome']=='UP'].sort_values(by='votos',ascending=False)
temp = melhor_UP[['local', 'votos']].groupby('local').sum().reset_index().set_index('local')
melhor_UP = temp.join(melhor_UP[['local', 'coordenadas']].set_index('local'), on='local', how='left').reset_index()
melhor_UP = melhor_UP.drop_duplicates('local').sort_values(by='votos',ascending=False)
melhor_Up_local_1, melhor_Up_local_2 = melhor_UP.iloc[0,0], melhor_UP.iloc[1,0]
melhor_Up_coord_1, melhor_Up_coord_2 = melhor_UP.iloc[0,2].split(', '), melhor_UP.iloc[1,2].split(', ')
melhor_Up_votos_1, melhor_Up_votos_2 = melhor_UP.iloc[0,1], melhor_UP.iloc[1,1]

lista_candidatos_UP = list(set(df[(df['cargo']=='Vereador')&(df['partido']=='UP')]['nome']))
lista_candidatos_PT = list(set(df[(df['cargo']=='Vereador')&(df['partido']=='PT')]['nome']))
lista_candidatos_PL = list(set(df[(df['cargo']=='Vereador')&(df['partido']=='PL')]['nome']))

temp = secoes_zonas.set_index(['zona', 'secao']).join(df[df['nome']=='INDIRA XAVIER'][['zona', 'secao', 'votos']].set_index(['zona', 'secao']), on=['zona', 'secao'], rsuffix=' Indira', how='left').reset_index()
temp = temp.set_index(['zona', 'secao']).join(df[df['nome']=='MARI FERNANDES'][['zona', 'secao', 'votos']].set_index(['zona', 'secao']), on=['zona', 'secao'], lsuffix=' Indira', rsuffix=' Mari', how='left').reset_index()
temp = temp.set_index(['zona', 'secao']).join(df[df['nome']=='EDNA DA IZIDORA'][['zona', 'secao', 'votos']].set_index(['zona', 'secao']), on=['zona', 'secao'], lsuffix='', rsuffix=' Edna', how='left').reset_index()
temp = temp.set_index(['zona', 'secao']).join(df[df['nome']=='ADRIEL DO MLB'][['zona', 'secao', 'votos']].set_index(['zona', 'secao']), on=['zona', 'secao'], lsuffix='', rsuffix=' Adriel', how='left').reset_index()
temp = temp.set_index(['zona', 'secao']).join(df[df['nome']=='UP'][['zona', 'secao', 'votos']].set_index(['zona', 'secao']), on=['zona', 'secao'], lsuffix='', rsuffix=' Up', how='left').reset_index()
cand_corr = temp
cand_corr.columns = ['zona', 'secao', 'Indira', 'Mari', 'Edna', 'Adriel', 'Up']
cand_corr['todos os vereadores'] = cand_corr['Mari']+cand_corr['Edna']+cand_corr['Adriel']+cand_corr['Up']
corr_ind_Mari = round(cand_corr['Indira'].corr(cand_corr['Mari'], method='spearman'),3)
corr_ind_Edna = round(cand_corr['Indira'].corr(cand_corr['Edna'], method='spearman'),3)
corr_ind_Adriel = round(cand_corr['Indira'].corr(cand_corr['Adriel'], method='spearman'),3)
corr_ind_Up = round(cand_corr['Indira'].corr(cand_corr['Up'], method='spearman'),3)
corr_ind_ver = round(cand_corr['Indira'].corr(cand_corr['todos os vereadores'], method='spearman'),3)

custo_medio_eleito_PT = round(sum([investimentos_dict[nome] for nome in eleitos_PT])/len(eleitos_PT),2)
custo_medio_eleito_NOVO = round((372263.05 + 200551.65 + 343997.07)/3,2)
custo_medio_eleito_PL = round(sum([investimentos_dict[nome] for nome in eleitos_PL])/len(eleitos_PL),2)
custo_medio_eleito_PSOL = round((93343.40 + 316054.70 + 365050.76)/3,2)
custo_medio_eleito_PCdoB = round(139864.09,2)
# médias
num_vot_ideo = int(votos['votos UP'].sum())
num_vot_ver = int(votos['votos no partido'].sum() - votos['votos INDIRA XAVIER'].sum())
custo_por_voto_todos = round(sum(pref_inv_df['votos'])/sum(pref_inv_df['custo total']),2)
votos_totais = int(votos['votos no partido'].sum())
media_de_ocupacao_de_urna = round(100*ocupacao['ocupacao real do partido'].mean(), 2)
percentual_voto_ideologico = round(100*num_vot_ideo/num_vot_ver,2)
votos_Adriel = int(votos_por_zona_Adriel['votos ADRIEL DO MLB'].sum())
custo_voto_Adriel = round(investimentos_dict['ADRIEL DO MLB']/votos_Adriel,2)
ocupacao_media_Adriel = round(100*votos_por_zona_Adriel['ocupacao ADRIEL DO MLB'].mean(),2)
votos_Edna = int(votos_por_zona_Edna['votos EDNA DA IZIDORA'].sum())
custo_voto_Edna = round(investimentos_dict['EDNA DA IZIDORA']/votos_Edna,2)
ocupacao_media_Edna = round(100*votos_por_zona_Edna['ocupacao EDNA DA IZIDORA'].mean(),2)
votos_Mari = int(votos_por_zona_Mari['votos MARI FERNANDES'].sum())
custo_voto_Mari = round(investimentos_dict['MARI FERNANDES']/votos_Mari,2)
ocupacao_media_Mari = round(100*votos_por_zona_Mari['ocupacao MARI FERNANDES'].mean(),2)
votos_Indira = int(votos_por_zona_Indira['votos INDIRA XAVIER'].sum())
custo_voto_Indira = round(investimentos_dict['INDIRA XAVIER']/votos_Indira,2)
ocupacao_media_Indira = round(100*votos_por_zona_Indira['ocupacao INDIRA XAVIER'].mean(),2)
limite_teorico_UP = int(len(set(df[df['partido']=='UP']['nome']))) - 2
limite_teorico_PT = int(len(set(df[df['partido']=='PT']['nome']))) - 2
limite_teorico_PL = int(len(set(df[df['partido']=='PL']['nome']))) - 2
votos_pref_PT = int(df[(df['partido']=='PT')&(df['cargo']=='Prefeito')]['votos'].sum())
votos_pref_PL = int(df[(df['partido']=='PL')&(df['cargo']=='Prefeito')]['votos'].sum())
votos_ver_PT = int(df[df['partido']=='PT']['votos'].sum() - votos_pref_PT)
votos_ver_PL = int(df[df['partido']=='PL']['votos'].sum() - votos_pref_PL)
votos_ideologicos_PT = int(df[df['nome']=='PT']['votos'].sum())
votos_ideologicos_PL = int(df[df['nome']=='PL']['votos'].sum())
votos_ideologicos_UP = int(df[df['nome']=='UP']['votos'].sum())
votos_a_vereador_por_votos_a_pref_UP = round(num_vot_ver/votos_Indira,2)
votos_a_vereador_por_votos_a_pref_PT = round(votos_ver_PT/votos_pref_PT,2)
votos_a_vereador_por_votos_a_pref_PL = round(votos_ver_PL/votos_pref_PL,2)
custo_voto_Indira = round(investimentos_dict['INDIRA XAVIER']/votos_Indira,2)
custo_voto_Rogerio = round(investimentos_dict['ROGERIO CORREIA']/votos_pref_PT,2)
custo_voto_Bruno = round(investimentos_dict['BRUNO ENGLER']/votos_pref_PL,2)

invest_UP = round(sum([investimentos_dict[nome] for nome in lista_candidatos_UP]),2)
invest_PT = round(sum([investimentos_dict[nome] for nome in lista_candidatos_PT]),2)
invest_PL = round(sum([investimentos_dict[nome] for nome in lista_candidatos_PL]),2)

votos_UP_ver = int(df[(df['cargo']=='Vereador')&(df['partido']=='UP')]['votos'].sum())
votos_PT_ver = int(df[(df['cargo']=='Vereador')&(df['partido']=='PT')]['votos'].sum())
votos_PL_ver = int(df[(df['cargo']=='Vereador')&(df['partido']=='PL')]['votos'].sum())
votos_total_UP = int(votos_UP_ver + df[(df['nome']=='INDIRA XAVIER')]['votos'].sum())
votos_total_PT = int(votos_PT_ver + df[(df['nome']=='ROGERIO CORREIA')]['votos'].sum())
votos_total_PL = int(votos_PL_ver + df[(df['nome']=='BRUNO ENGLER')]['votos'].sum())
invest_total_UP = round(invest_UP + investimentos_dict['INDIRA XAVIER'],2)
invest_total_PT = round(invest_PT + investimentos_dict['ROGERIO CORREIA'],2)
invest_total_PL = round(invest_PL + investimentos_dict['BRUNO ENGLER'],2)
preco_do_voto_total_UP = round(invest_total_UP/votos_total_UP,2)
preco_do_voto_total_PT = round(invest_total_PT/votos_total_PT,2)
preco_do_voto_total_PL = round(invest_total_PL/votos_total_PL,2)

custo_voto_ver_UP = round(invest_UP/votos_UP_ver,2)
custo_voto_ver_PT = round(invest_PT/votos_PT_ver,2)
custo_voto_ver_PL = round(invest_PL/votos_PL_ver,2)
percentual_ideo_UP = round(100*votos_ideologicos_UP/votos_UP_ver)
percentual_ideo_PT = round(100*votos_ideologicos_PT/votos_PT_ver)
percentual_ideo_PL = round(100*votos_ideologicos_PL/votos_PL_ver)


variables ={'std_Adriel':std_Adriel,
            'std_Edna':std_Edna, 
            'std_Indira':std_Indira,
            'std_Mari':std_Mari,
            'std_UP':std_UP,
            'melhor_Ad_local_1':melhor_Ad_local_1,
            'melhor_Ad_coord_1':melhor_Ad_coord_1,
            'melhor_Ad_votos_1':melhor_Ad_votos_1,
            'melhor_Ad_local_2':melhor_Ad_local_2,
            'melhor_Ad_coord_2':melhor_Ad_coord_2,
            'melhor_Ad_votos_2':melhor_Ad_votos_2,
            'melhor_Ed_local_1':melhor_Ed_local_1,
            'melhor_Ed_coord_1':melhor_Ed_coord_1,
            'melhor_Ed_votos_1':melhor_Ed_votos_1,
            'melhor_Ed_local_2':melhor_Ed_local_2,
            'melhor_Ed_coord_2':melhor_Ed_coord_2,
            'melhor_Ed_votos_2':melhor_Ed_votos_2,
            'melhor_Id_local_1':melhor_Id_local_1,
            'melhor_Id_coord_1':melhor_Id_coord_1,
            'melhor_Id_votos_1':melhor_Id_votos_1,
            'melhor_Id_local_2':melhor_Id_local_2,
            'melhor_Id_coord_2':melhor_Id_coord_2,
            'melhor_Id_votos_2':melhor_Id_votos_2,
            'melhor_Ma_local_1':melhor_Ma_local_1,
            'melhor_Ma_coord_1':melhor_Ma_coord_1,
            'melhor_Ma_votos_1':melhor_Ma_votos_1,
            'melhor_Ma_local_2':melhor_Ma_local_2,
            'melhor_Ma_coord_2':melhor_Ma_coord_2,
            'melhor_Ma_votos_2':melhor_Ma_votos_2,
            'melhor_Ma_local_1':melhor_Ma_local_1,
            'melhor_Ma_coord_1':melhor_Ma_coord_1,
            'melhor_Ma_votos_1':melhor_Ma_votos_1,
            'melhor_Ma_local_2':melhor_Ma_local_2,
            'melhor_Ma_coord_2':melhor_Ma_coord_2,
            'melhor_Ma_votos_2':melhor_Ma_votos_2,
            'melhor_Up_local_1':melhor_Up_local_1,
            'melhor_Up_coord_1':melhor_Up_coord_1,
            'melhor_Up_votos_1':melhor_Up_votos_1,
            'melhor_Up_local_2':melhor_Up_local_2,
            'melhor_Up_coord_2':melhor_Up_coord_2,
            'melhor_Up_votos_2':melhor_Up_votos_2,
            'corr_ind_Mari':corr_ind_Mari,
            'corr_ind_Adriel':corr_ind_Adriel,
            'corr_ind_Edna':corr_ind_Edna,
            'corr_ind_Up':corr_ind_Up,
            'corr_ind_ver':corr_ind_ver,
            'custo_medio_eleito_PT':custo_medio_eleito_PT,
            'custo_medio_eleito_NOVO':custo_medio_eleito_NOVO,
            'custo_medio_eleito_PL':custo_medio_eleito_PL,
            'custo_medio_eleito_PSOL':custo_medio_eleito_PSOL,
            'custo_medio_eleito_PCdoB':custo_medio_eleito_PCdoB,
            'media_de_ocupacao_de_urna':media_de_ocupacao_de_urna,
            'percentual_voto_ideologico':percentual_voto_ideologico,
            'votos_Adriel':votos_Adriel,
            'custo_voto_Adriel':custo_voto_Adriel,
            'ocupacao_media_Adriel':ocupacao_media_Adriel,
            'votos_Edna':votos_Edna,
            'custo_voto_Edna':custo_voto_Edna,
            'ocupacao_media_Edna':ocupacao_media_Edna,
            'votos_Mari':votos_Mari,
            'custo_voto_Mari':custo_voto_Mari,
            'ocupacao_media_Mari':ocupacao_media_Mari,
            'votos_Indira':votos_Indira,
            'custo_voto_Indira':custo_voto_Indira,
            'ocupacao_media_Indira':ocupacao_media_Indira,
            'votos_a_vereador_por_votos_a_pref_UP':votos_a_vereador_por_votos_a_pref_UP,
            'votos_a_vereador_por_votos_a_pref_PT':votos_a_vereador_por_votos_a_pref_PT,
            'votos_a_vereador_por_votos_a_pref_PL':votos_a_vereador_por_votos_a_pref_PL,
            'custo_voto_Rogerio':custo_voto_Rogerio,
            'custo_voto_Bruno':custo_voto_Bruno,
            'votos_total_UP':votos_total_UP,
            'votos_total_PT':votos_total_PT,
            'votos_total_PL':votos_total_PL,
            'preco_do_voto_total_UP':preco_do_voto_total_UP,
            'preco_do_voto_total_PT':preco_do_voto_total_PT,
            'preco_do_voto_total_PL':preco_do_voto_total_PL,
            'custo_voto_ver_UP':custo_voto_ver_UP,
            'custo_voto_ver_PT':custo_voto_ver_PT,
            'custo_voto_ver_PL':custo_voto_ver_PL,
            'percentual_ideo_UP':percentual_ideo_UP,
            'percentual_ideo_PT':percentual_ideo_PT,
            'percentual_ideo_PL':percentual_ideo_PL
 }

with open('data/variaveis_analise_do_partido.json', 'w') as outfile:
    json.dump(variables, outfile)

votos.to_csv('data/data_mapa_analise.csv', sep=';',index=False)
data.to_csv('data/data_histograma_analise.csv', sep=';',index=False)
votos_por_zona.to_csv('data/data_area_analise.csv', sep=';',index=False)
votos_por_zona_Adriel.to_csv('data/data_Zona_Adriel_analise.csv', sep=';',index=False)
votos_por_zona_Edna.to_csv('data/data_Zona_Edna_analise.csv', sep=';',index=False)
votos_por_zona_Mari.to_csv('data/data_Zona_Mari_analise.csv', sep=';',index=False)
votos_por_zona_Indira.to_csv('data/data_Zona_Indira_analise.csv', sep=';',index=False)
votos_por_zona_Up.to_csv('data/data_Zona_Up_analise.csv', sep=';',index=False)

