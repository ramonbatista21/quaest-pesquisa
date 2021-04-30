#!/usr/bin/env python
# coding: utf-8

# # <center>Avaliação técnica — Quaest, Data Scientist Jr.</center>
# ### <center> Ramon Batista de Araújo</center>
# 
# 
# O objetivo deste teste é avaliar um pouco suas habilidades como cientista de dados e, também, demonstrar como será parte do seu dia a dia atuando na Quaest.
# 
# #### Dataset
# Base de dados resumida e fictícia <br>
# Arquivo 'bd_surveyquaest.xlsx' 
# 
# #### Variáveis
# sbjnum: id do respondente<br>
# sexo: sexo do respondente<br>
# idade: idade (numérica) do respondente<br>
# rendaf: renda familiar do respondente<br>
# esc: escolaridade do respondente<br>
# aval_gov: avaliação do governo<br>
# voto1: intenção de voto do respondente.<br>
# 
# ### Atividades
# ##### Tabela de contigência 
# Crie uma função em alguma linguagem de programação, preferencialmente em R ou Python, que automatize a construção de tabelas de contingência. O objetivo é identificar se há uma diferença sociodemográfica na intenção de voto. Em outras palavras, por ex.: As mulheres e os homens estão votando no mesmo candidato ?
# 
# ##### Gráficos
# 2.1) O primeiro gráfico será da variável intenção de voto.
# 
# 2.2) Já o segundo, plot um gráfico que represente o cruzamento entre as variáveis intenção de voto e avaliação do governo. Quem avalia o governo de forma positiva, vota em qual candidato ? E quem avalia de forma negativa ?
# 

# ### Importando as bibliotecas

# In[1]:


#Instalação das bibliotecas (se necessário)
# !pip install pandas
# !pip install numpy
# !pip install sys
# !pip install seaborn
# !pip install matplotlib


# In[2]:


#Tratamento dos dados
import pandas as pd
import numpy as np
import sys
import xlsxwriter

#Criação de Gráficos
import seaborn as sns
import matplotlib as mpl  
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Importando o banco de dados

# In[3]:


bd = pd.read_excel('bd_surveyquaest.xlsx') #Importando a planilha

bd.head() #Lendo as primeiras linhas


# ### Análise Exploratória 

# In[4]:


#Verificando o tamanho do dataset

bd.shape #1000 registros e 7 variáveis


# In[5]:


#Confirmando o nome das variáveis
bd.columns


# In[6]:


#Verificando valores ausentes

bd.isna().sum() #Não existem valores ausentes


# In[7]:


#Verificando valores duplicados

bd.duplicated().sum() #Não existem registros duplicados


# In[8]:


#Verificando os tipos de variáveis

bd.info() #Categoricas e Inteiro


# #### Verificando os valores únicos e outliers de cada variável

# In[9]:


#Conferência de valores únicos

bd.nunique()


# In[10]:


#Sexo 

bd['sexo'].value_counts()


# In[11]:


#Idade

bd['idade'].describe()


# In[12]:


#Renda

bd['rendaf'].value_counts()


# In[13]:


#Escolaridade

bd['esc'].value_counts()


# In[14]:


#Avaliação do governo

bd['aval_gov'].value_counts()


# In[15]:


#Intenção de voto

bd['voto1'].value_counts()


# #### Categorizando as idades de acordo com o eleitorado do TSE
# 
# BRASIL. TRIBUNAL SUPERIOR ELEITORAL. Estatísticas Eleitorais. 2020. Data da última atualização: 10.9.2020 - 23:04. Disponível em: https://www.tse.jus.br/eleicoes/estatisticas/estatisticas-eleitorais . Acesso em: 26 abr. 2021 
# <br>
# 
# ##### As Faixas etárias de acordo com o TSE são:
# 
# 16 anos <br>
# 17 anos <br>
# 18 anos <br>
# 19 anos <br> 
# 20 anos <br>
# 21 a 24 anos <br>
# 25 a 29 anos <br>
# 30 a 34 anos <br>
# 35 a 39 anos <br>
# 40 a 44 anos <br> 
# 45 a 49 anos <br>
# 50 a 54 anos <br>
# 55 a 59 anos <br>
# 60 a 64 anos <br>
# 65 a 69 anos <br>
# 70 a 74 anos <br>
# 75 a 79 anos <br>
# 80 a 84 anos <br>
# 85 a 89 anos <br>
# 90 a 94 anos <br>
# 95 a 99 anos <br>
# 100 anos ou mais <br>

# In[16]:


#Categoriazando as idades

bd['faixa_etaria']=pd.cut(

   bd['idade'],

   bins=[16, 17, 18, 19, 20, 21, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, sys.maxsize],

   labels=['16 anos',
           '17 anos',
           '18 anos',
           '19 anos',
           '20 anos',
           '21 a 24 anos',
           '25 a 29 anos',
           '30 a 34 anos',
           '35 a 39 anos',
           '40 a 44 anos',
           '45 a 49 anos',
           '50 a 54 anos',
           '55 a 59 anos',
           '60 a 64 anos',
           '65 a 69 anos',
           '70 a 74 anos',
           '75 a 79 anos',
           '80 a 84 anos',
           '85 a 89 anos']       
)

bd['faixa_etaria'].value_counts() #Quantidade de eleitores por idade


# ## Criando para construção de tabelas de contingência.

# In[17]:


#Função tabela de contigência com os total

def contigencia(tabela):
    tabela = pd.crosstab(tabela,bd['voto1'], dropna=False, margins=True, margins_name="Total" )
    return tabela


# In[18]:


#Função tabela de contigência sem os total

def contig_sem_total(tabela):
    tabela = pd.crosstab(tabela,bd['voto1'], dropna=False)
    return tabela


# In[19]:


df = bd.drop(columns=['sbjnum', 'idade', 'voto1']) #Eliminando as colunas desnecessárias na tabela de contigência 
df.head()


# In[20]:


lista_col = list(df.columns) #listando as colunas
lista_col


# In[21]:


writer = pd.ExcelWriter('tabela_contigencia.xlsx', engine='xlsxwriter') #Criar um arquivo Excel


# In[22]:


#Automatização da criação de tabelas

for i in range(len(lista_col)):
    colunas = bd[lista_col[i]]
    tabela = contigencia(colunas) #criar tabelas pela função
    
    nome_planilha = lista_col[i]
    tabela.to_excel(writer,sheet_name=nome_planilha, index=False) #Escrever no arquivo excel
    
writer.save() #Fechar o arquivo


# #### As mulheres e os homens estão votando no mesmo candidato ?

# In[23]:


#Pode-se criar uma Lista com as colunas que deseja criar a tabela de contigência

colunas = [bd['sexo']]


# In[24]:


#A função recebe as colunas para criar a tabela de contigência com a intenção de voto

tabela_cont = contigencia(colunas) 
tabela_cont


# In[25]:


#Calculando as porcentagens de intenção de voto por sexo

colunas = tabela_cont.shape[0]
for i in list(range(colunas)):
    tabela_cont.iloc[i] = tabela_cont.iloc[i]/tabela_cont.iloc[i, -1]*100
    
tabela_cont


# # 
# Ou seja, 54,12844% entre as 545 mulheres entrevistadas têm a intenção de votar no candidato 2. Assim como os 50,10989% entre os 455 homens entrevistas também têm a intenção de votar no candidato 2.

# ## Gráfico da variável intenção de voto

# In[26]:


#Selecionando somente a intenção de voto

intencao = bd['voto1'].value_counts().reset_index()


# In[27]:


#Porcentagem

tamanho_amostra = len(bd) #Tamanho da amostra
intencao['voto1'] = (intencao['voto1']/tamanho_amostra)*100 

intencao #banco de dados com a intenção de voto


# In[28]:


#Ordenando os candidatos antes dos Ninguém/Branco/Nulo e NS/NR

#Removendo do dataset
intencao_cand = intencao[intencao['index'] != 'NS/NR'] 
intencao_cand = intencao_cand[intencao_cand['index'] !=  'Ninguém/Branco/Nulo']
intencao_cand


# In[29]:


#Criando novas variaveis

NS = intencao[intencao['index'] == 'NS/NR'] 
Ning = intencao[intencao['index'] == 'Ninguém/Branco/Nulo'] 


# In[30]:


#Adicionando novas variaveis ao final do dataset

intencao_cand = intencao_cand.append(Ning)

intencao_cand = intencao_cand.append(NS)
intencao_cand


# In[31]:


#Adicionando novas variaveis ao final do dataset


intencao_cand.reset_index(drop=True, inplace=True)
intencao_cand


# In[32]:


#Renomeando a coluna candidato

intencao_cand.rename(columns={'index': 'candidato'}, inplace=True)


# #### Criando o gráfico

# In[33]:


#Cor degradê que quanto menor a quantidade de votos, menor será <br> a saturação,
## O objetivo é destacar os candidatos com maior número de votos.

cores = sns.light_palette("lightseagreen",16, reverse=True)

#Tamanho do gráfico na proporção de uma tela widrescreen (16:9) para evitar erros de proporções  
fig = plt.figure(figsize=(16,9)) 

#Criando o gráfico de barras horizontais para o que o nome do candidato apareça por completo
#sem necessidade de rotacionar para não dificultar a leitura.

ax = sns.barplot(data=intencao_cand, y="candidato", x="voto1", palette=cores, zorder=2) 

#Titulo do gráfico
plt.title('Intenção de voto',fontsize=20, color='darkslategray')

#Criação dos eixos 
plt.xlabel('Porcentagem da intenção de voto (%)',fontsize=12, labelpad=20, color='slategray')
plt.ylabel('',fontsize=0, labelpad=0, color='slategray')
plt.xticks(fontsize=12, color='slategray')
plt.yticks(fontsize=14, color='darkslategray')
fmt = '%.0f%%' 
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)

#Distanciamento das bordas
plt.ylim(bottom=15.6, top=-1.0)
plt.xlim(0,100)

#Grade no fundo para facilitar a leitura, em cor clara para evitar conflito com as barras horizontais.
plt.grid( alpha=0.15, color='silver', zorder=-1)
voto1 = intencao_cand['voto1']

#Porcentagem das barras
for p in ax.patches:
    percentage ='{:,.1f}%'.format(p.get_width())
    width, height =p.get_width(),p.get_height()
    x=p.get_x()+width+0.5
    y=p.get_y()+height/1.5
    ax.annotate(percentage,(x,y), size = 12, color='teal')
    
#Reomação do quadro e inclusão apenas dos eixos verticais e horizontais com maior graduação.
plt.box(on=None)
ax.minorticks_on()
plt.axvline(x=0, ymin=0, ymax=1, color='lightgray')
plt.axhline(y=15.5, xmin=0, xmax=1, color='lightgray')

#Salvar gráfico em arquivo svg (Scalable Vector Graphics) 
#para não perder resolução quando ampliado ou reduzido em suas aplicações.
plt.savefig('intencao_voto.svg', format='svg', bbox_inches='tight')


# Não agrupou-se os canditados com menos de 1%. Pois, como exemplo, se a margem de erro for de três pontos percentuais, excluindo-se o primeiro colocado (candidato 2) o restante pode variar de posição.

# ## Cruzamento entre as variáveis intenção de voto e avaliação do governo

# In[34]:


#Utilizando a função criada de tabela de contigência

#Seleção da coluna avaliação do governo
colunas = bd['aval_gov']


# In[35]:


#Criando a tabela de contigência com total

tabela_cont = contigencia(colunas).T #Tabela Transposta
tabela_cont


# In[36]:


#Calculando as porcentagens em relação para cada a item da escala de avaliação

colunas = tabela_cont.shape[1]
for i in list(range(colunas)):
    tabela_cont.iloc[:,i] = (tabela_cont.iloc[:,i]/tabela_cont.iloc[-1,i])*100
    
tabela_cont #Percebe-se nas linha Total o percentual total de cada item da escala. 

#Na coluna Total têm-se o percentual de intenção de votos de cada candidato. 


# In[37]:


#Removendo a linha e coluna Total

tabela_cont = tabela_cont.iloc[:-1,:-1]
tabela_cont


# In[38]:


#Ordendando as colunas do pior para o melhor avaliação

tabela_cont = tabela_cont.iloc[:,[2,5,3,1,4,0,6]]
tabela_cont


# In[39]:


#Ordendando os candidatos pela total de intenção de votos

tabela_cont.reset_index(inplace=True)
tabela_cont.rename(columns={'voto1': 'candidato'}, inplace=True)
tabela_cont


# In[40]:


#Concatenando a tabela de contigência com a tabela de intenção de votos utilizada no gráfico de intenção de votos

ordem_tab = pd.merge(tabela_cont, intencao_cand, on=['candidato'], how='right')
ordem_tab


# In[41]:


#Removendo a coluna de intenção de votos

tabela_cont = ordem_tab.drop(columns=['voto1'])
tabela_cont


# In[42]:


#Definindo candidato como index

tabela_cont = tabela_cont.set_index("candidato")
tabela_cont


# In[43]:


#Criando a tabela transposta

tabela_cont= tabela_cont.T

tabela_cont


# In[44]:


#Criando uma lista com o nome dos candidatos 

lista =list(tabela_cont.columns)
lista


# In[45]:


#Criando uma paleta de cores de acordo com as cores dos partidos na ordem da lista acima

cores_dos_partidos = [ 'teal', 
                 'coral', 
                 'mistyrose', 
                 'burlywood', 
                 'darkseagreen', 
                 'cadetblue', 
                 'grey',
                 'rosybrown',
                 'indianred',
                 'palevioletred',
                 'mediumslateblue', 
                 'skyblue',
                 'dodgerblue', 
                 'steelblue',
                 'silver',
                 'slategrey',
                ]


# In[46]:



#Criando um gráfico estilo likert com as cores dos partidos de cada candidato
#Proporção tela widrescreen (16:6)
ax = tabela_cont.plot.barh(y=lista, stacked=True, width = 0.6, color=cores_dos_partidos, figsize=(16,9), zorder=3) 


#Criando a legenda
handler, label = ax.get_legend_handles_labels()
ax.legend(
    handler, 
    label, 
    loc='upper center', 
    bbox_to_anchor=(0.5, -0.15), 
    ncol=4, 
    edgecolor='white',
    fontsize = 'x-large',
    labelcolor='slategray')

# Criando um eixo nos 50% para facilitar visualização
z = plt.axvline(x=50, linestyle='--', color='silver', alpha=0.5)
z.set_zorder(-1)

#Título
plt.title('A avaliação do governo com relação a intenção de voto',fontsize=20, color='darkslategray')

#Criação dos eixos 
plt.xlabel('% da avaliação do governo',fontsize=14, labelpad=20, color='slategray')
plt.ylabel('',fontsize=12, labelpad=20, color='slategray')
plt.xticks(fontsize=12, color='slategray')
plt.yticks(fontsize=14, color='darkslategray')
fmt = '%.0f%%' 
xticks = mtick.FormatStrFormatter(fmt)
ax.xaxis.set_major_formatter(xticks)

#Distanciamento das bordas
plt.ylim(bottom=6.6, top=-1.0)
plt.xlim(0,100)

#Grade no fundo para facilitar a leitura.
plt.grid(axis='x', alpha=0.25, color='silver', zorder=-2)

#Reomação do quadro e inclusão apenas dos eixos verticais e horizontais com maior graduação.
plt.box(on=None)
ax.minorticks_on()
plt.axvline(x=0, ymin=0, ymax=0.8, color='lightgray')
plt.axhline(y=15.5, xmin=0, xmax=1, color='lightgray')

#Salvar gráfico em arquivo svg 
plt.savefig('avaliacao_x_intencao.svg', format='svg', bbox_inches='tight');


# # 
# De acordo com o gráfico acima, a maioria dos eleitores que avaliam o gorveno de forma positiva, isto é, Ótima, Boa e Regular positiva tem a intenção de votar no candidato 2 (Verde Turquesa). 
# 
# E a maioria que avalia de forma negativa, ou seja, a avaliação é Péssima, Ruim ou Regular negativa tem intenção de votar em Ninguém/Branco/Nulo ou NS/NR, fora isso tem a intenção de votar no candidato 8 (Rosa Claro) ou candidato 1 (Laranja).
# 
# Como pode ser confirmado pela tabela de contigência. 

# # 
# De acordo com o gráfico acima, a maioria dos eleitores que avaliam o gorveno de forma positiva, isto é, Ótima, Boa e Regular positiva tem a intenção de votar no candidato 2 (Verde Turquesa). 
# 
# E a maioria que avalia de forma negativa, ou seja, a avaliação é Péssima, Ruim ou Regular negativa tem intenção de votar em Ninguém/Branco/Nulo ou NS/NR, fora isso tem a intenção de votar no candidato 8 (Rosa Claro) ou no candidato 1 (Laranja).
# 
# Como pode ser confirmado pela tabela de contigência. 

# # 
# O design dos gráficos tem como referência o livro Storytelling com dados.
# 
# KNAFLIC, Cole Nussbaumer. Storytelling com dados: um guia sobre visualização de dados para profissionais de negócios. 2ª edição. Traduzido por João Tortello - Rio de Janeiro. ed. Alta Books, 2018. 256 p. v. 1.
