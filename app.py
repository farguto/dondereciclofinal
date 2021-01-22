#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Instalación de librerías 

#!pip install jupyter-dash
#!pip install dash
#!pip install dash_core_components
#!pip install dash_html_components
#!pip install dash_table
#!pip install dash_bootstrap_components




# Importamos librerías


import dash
#import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output,State
import dash_table
import plotly.graph_objects as go
import plotly.express as px



# Importamos archivos y generamos las tablas. 

campanas_verdes=pd.read_csv('campanas-verdes.csv',sep=',', encoding='utf-8')
RSU_por_comuna_2015=pd.read_excel("datasets/RSU_por_comuna_2015_v2.xlsx")
pesaje_recibido_PT=pd.read_csv("datasets/BA datos abiertos/pesaje-recibido-en-puntos-verdes-2015-2016.csv",sep=";", encoding='utf-8')

puntoverde=pd.read_csv("puntoverde.csv",sep=",", encoding='ISO-8859-15')
Comuna_Mayor_PuntoVerde = pd.DataFrame({"Cantidad":puntoverde.Comuna.value_counts()})
listado_puntosverdes = Comuna_Mayor_PuntoVerde.head(5)

Comuna_Manor_PuntoVerde = pd.DataFrame({"Cantidad":puntoverde.Comuna.value_counts()})
Comuna_Manor_PuntoVerde=Comuna_Manor_PuntoVerde.sort_values("Cantidad", ascending=True).head()
menorcantidad_puntosverdes=Comuna_Manor_PuntoVerde=Comuna_Manor_PuntoVerde.sort_values("Cantidad", ascending=True).head()



#PREGUNTA1

data_tabla = listado_puntosverdes.to_dict('records')
listado_puntosverdes.columns
[{'name': i, 'id': i } for i in listado_puntosverdes.columns ]


rsu_melt=pd.melt(RSU_por_comuna_2015,
         id_vars=RSU_por_comuna_2015.columns[:2],
         value_vars=RSU_por_comuna_2015.columns[2:],
         var_name='Comuna',
         value_name='Toneladas')
rsu_melt.head()

#hago un sum de la columna Toneladas
pregunta1=round(rsu_melt['Toneladas'].sum())


#PREGUNTA2
#groupby de rsu_melt
#Sumo las toneladas por comuna con groupby, lo convierto en df y lo ordeno descendente (con esto tengo el top 5)
toneladasagrupadas = rsu_melt.groupby('Comuna').Toneladas.agg(sum)

rsu_por_comuna = pd.DataFrame( toneladasagrupadas ).reset_index() #reset index lleva comunasindex a comuna columna

rsu_por_comuna = rsu_por_comuna.sort_values('Toneladas',ascending=False)
rsu_por_comuna.head()


data_tabla2 = rsu_por_comuna.head().to_dict('records')
rsu_por_comuna.head().columns
[{'name': i, 'id': i } for i in rsu_por_comuna.head().columns ]


#PREGUNTA3

#filtro reciclable=='si' y luego hago groupby por comuna sumando la columna 'TONELADAS', y ordeno los valores descendente
# Filtro los si en reciclable
reciclables_por_comuna_temp = rsu_melt.loc[rsu_melt['Reciclable']=='si']

toneladasagrupadas_r = rsu_melt[rsu_melt.Reciclable == 'si'].groupby('Comuna').Toneladas.agg(sum)

#convierto el groupby anterior en un dataframe
reciclables_por_comuna = pd.DataFrame(toneladasagrupadas_r).reset_index()

#ordeno el dataframe descendente, redondeo los valores y me quedo con el máximo
reciclables_por_comuna.round({'Toneladas': 1}).sort_values('Toneladas',ascending=False).head(2)
pregunta3=reciclables_por_comuna.round({'Toneladas': 1}).sort_values('Toneladas',ascending=False).head(2)

#PREGUNTA4

#Sumo las toneladas por comuna con groupby, lo convierto en df y lo ordeno descendente (con esto tengo el top 5)

pesaje_recibido_PT_2015 = pesaje_recibido_PT.loc[pesaje_recibido_PT['ANIO']==2015]


pesaje_recibido_PT_2015=pesaje_recibido_PT_2015.drop('AVUS',axis=1)

pesaje_recibido_PT_2015_melt=pd.melt(pesaje_recibido_PT_2015,
         id_vars='COMUNA',
         value_vars=pesaje_recibido_PT_2015.columns[5:],
         var_name='COMPONENTE',
         value_name='KG')


#reemplazo las ',' por '.'
pesaje_recibido_PT_2015_melt['KG'] = pesaje_recibido_PT_2015_melt['KG'].str.replace(',','.')

#reemplazo los espacios en blanco de los extremos
pesaje_recibido_PT_2015_melt['KG'] = pesaje_recibido_PT_2015_melt['KG'].str.strip()

#para ver cuando son vacios
#pesaje_recibido_PT_2015_melt[pesaje_recibido_PT_2015_melt['KG'] == ''].index

#convierto los kg de object a float
pesaje_recibido_PT_2015_melt['KG'] = pd.to_numeric(pesaje_recibido_PT_2015_melt['KG'], errors='coerce')

#creo una columna con el peso en toneladas para que sea comparable con el df RSU_por_comuna
pesaje_recibido_PT_2015_melt['TONELADAS'] = pesaje_recibido_PT_2015_melt['KG']/1000

# hacer gropuby de pesaje_recibido_PT_2015_melt
#pesaje_recibido_PT_2015_melt
#pesaje_recibido_PT_2015_melt.groupby('COMUNA').TONELADAS.agg(sum).sort_values('TONELADAS',ascending=False)

#groupby de rsu_melt
#Sumo las toneladas por comuna con groupby, lo convierto en df y lo ordeno descendente (con esto tengo el top 5)
toneladasagrupadas_r = pesaje_recibido_PT_2015_melt.groupby('COMUNA').TONELADAS.agg(sum)

reciclado_por_comuna = pd.DataFrame( toneladasagrupadas_r ).reset_index() #reset index lleva comunasindex a comuna columna

reciclado_por_comuna = reciclado_por_comuna.sort_values('TONELADAS',ascending=False)


data_tabla3 = reciclado_por_comuna.to_dict('records')
reciclado_por_comuna.columns
[{'name': i, 'id': i } for i in reciclado_por_comuna.columns ]


#PREGUNTA5

# df reciclables generados por comua
reciclables_por_comuna_temp.Componente.unique()#sumar metales no ferrosos con metales ferrosos para comparar

# df reciclables reciclados por comua
pesaje_recibido_PT_2015_melt.COMPONENTE.unique() #pequenios electrodomésticos no se puede comparar porque no tiene desagregación a nivel ciudad

#reemplazo 'Metales Ferrosos' y 'Metales No Ferrosos' por 'METAL'
reciclables_por_comuna_temp.Componente = reciclables_por_comuna_temp.Componente.replace({'Metales Ferrosos':'METAL' , 'Metales No Ferrosos':'METAL'})

reciclables_por_comuna_temp.Componente.unique() 

#hago un groupby por componente

reciclables_por_comuna_bar = reciclables_por_comuna_temp.groupby('Componente').Toneladas.agg(sum)

reciclables_por_comuna_bar = pd.DataFrame( reciclables_por_comuna_bar).reset_index() #reset index lleva comunasindex a comuna columna

reciclables_por_comuna_bar = reciclables_por_comuna_bar.sort_values('Toneladas',ascending=True)

reciclables_por_comuna_bar

type(reciclables_por_comuna_bar)


#PREGUNTA5B

#genero un gráfico de barras 100% apilado, ordenar por %reciclado descendente
#primero hago un merge entre reciclables_por_comuna_bar y pesaje_recibido_PT_2015_melt
#para poder hacer el melt tengo que agrupar pesaje_recibido


#hago un groupby por componente, y cambio el nombre de la columna a Tipo de Residuo

reciclado_por_componente = pesaje_recibido_PT_2015_melt.groupby('COMPONENTE').TONELADAS.agg(sum)

reciclado_por_componente = pd.DataFrame( reciclado_por_componente).reset_index() #reset index lleva componenteindex a comuna columna

reciclado_por_componente

#merge entre lo generado (reciclables_por_comuna_bar) y lo reciclado (reciclado_por_componente)
residuos_merged = pd.merge(left=reciclables_por_comuna_bar,right=reciclado_por_componente, left_on='Componente', right_on='COMPONENTE')
residuos_merged

#cambio el nombre de las columnas para que no se confunda
residuos_merged.rename(columns={'Componente':'Tipo_de_residuo',
                        'Toneladas':'Toneladas_generadas',
                        'TONELADAS':'Toneladas_recicladas'},
               inplace=True)
#elimino la columna COMPONENTE que se repite
residuos_merged = residuos_merged.drop(['COMPONENTE'], axis=1)
residuos_merged

#genero la columna con el % de reciclado y otra con el % de no reciclado
#agrego una columna vacía % reciclado
residuos_merged['recicladosiporc'] = residuos_merged['Toneladas_recicladas'] * 100 / residuos_merged['Toneladas_generadas']
residuos_merged['recicladonoporc'] = 100 - residuos_merged['recicladosiporc']

residuos_merged

residuos_merged =residuos_merged.sort_values('recicladosiporc')


#App

#se inicia la App y se le agrega una selección de un tema en bootstrap.

#app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])



external_stylesheets = [
    'assets/style.css', 'http://fonts.googleapis.com/css?family=Roboto'

]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


#Server
server = app.server




#Layout
app.layout = html.Div([
    html.H1('Dónde reciclar'), 
    html.H2('Accedé a las ubicaciones para saber dónde llevar el material reciclable en la Ciudad de Buenos Aires'),
     

# Dentro de dcc.Tabs se colocan los 2 tabs. 

# En Tab1 se inserta un mapa de Campanas Verdes y Puntos Verdes mediante la utilización de un Iframe, en el cual se encuentra el mapa en html. 

    dcc.Tabs([


         dcc.Tab(id='Tab1a', label='Presentación',  children=[


         html.Iframe(id = 'intro', srcDoc = open('tab_principal.html', 'r').read(), width = '100%', height='600'), 
    
         ]),




        dcc.Tab(id='Tab1', label='Campanas y Puntos Verdes',  children=[
            
          
          html.Iframe(id = 'map', srcDoc = open('puntosverdesycampanas3.html', 'r').read(), width = '100%', height='600'),               
   
          html.Div([
    
                dcc.Graph(id='grafico_1', figure=px.bar(listado_puntosverdes,y='Cantidad', x=['Comuna 10', 'Comuna 12','Comuna 13','Comuna 9','Comuna 7',],              
color="Cantidad",                         
labels={'Cantidad':'Cantidad de Puntos Verdes', 'x': 'Comunas'}, title="Comunas con mayor cantidad de Puntos Verdes", height=600, width=600 ,),

),

            ]), 
          
           html.Div([
    
           dcc.Graph(id='grafico_2', figure=px.bar(menorcantidad_puntosverdes, y='Cantidad', x=['Comuna 5', 'Comuna 2','Comuna 1','Comuna 8','Comuna 11',], color="Cantidad", 
labels={'Cantidad':'Cantidad de Puntos Verdes', 'x': 'Comunas'}, title="Comunas con menor cantidad de Puntos Verdes", height=600, width=600 ,)
)





            ])
                
        ]),    

# En Tab2 se insertan los graficos y las tablas con data de Puntos Verdes. 
# Dentro de Tab2 se insertan los graficos mediante dcc.Graph, cada grafico dentro de un Div.
# Para generar el gŕafico, dentro de figure se inserta la generación del gráfico en Plotly, tomando la tabla armada anteriormente.
        
        dcc.Tab(id='Tab2', label='Más información sobre el reciclado en la Ciudad',  children=[


         html.Iframe(id = 'map2', srcDoc = open('mapachoroplet.html', 'r').read(), width = '100%', height='600'), 
            
                   

        html.Div([
                
      

        html.P('En 2015 la Ciudad de Buenos Aires generó '+ str(pregunta1) + ' toneladas de residuos domiciliarios'),


        html.P('Del total de residuos domiciliarios, 413634 toneladas son reciclables')

            ]),



        html.Div([

        html.H2((' ¿Cuáles son las comunas que generaron más residuos?')),
        html.H2(html.Li(' ¿Cuánto residuo generó cada comuna?')),

        dash_table.DataTable(
                     id='tabla2',
                     data=  rsu_por_comuna.head().to_dict('records'),
                     columns=[{'name': i, 'id': i } for i in rsu_por_comuna.head().columns ],
                     style_header={'backgroundColor': 'steelblue', 'color':'white', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     filter_action='native', 
                     page_current= 0,
                     page_size= 10,

                    )


            ]),

        html.Div([
        html.H2(html.Li(' Comuna que más residuos reciclables genera (Año 2015)')),

        dash_table.DataTable(
                     id='tabla3',
                     data=  pregunta3.to_dict('records'),
                     columns=[{'name': i, 'id': i } for i in pregunta3.columns ],
                     style_header={'backgroundColor': 'steelblue', 'color':'white', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     filter_action='native', 
                     page_current= 0,
                     page_size= 10,
                    )




            ]),

        html.Div([
        html.H2(html.Li(' ¿Cuántos residuos reciclables recibió cada comuna en sus puntos verdes? (Año 2015) ')),

        dash_table.DataTable(
                     id='tabla4',
                     data=  reciclado_por_comuna.to_dict('records'),
                     columns=[{'name': i, 'id': i } for i in reciclado_por_comuna.columns ],
                     style_header={'backgroundColor': 'steelblue', 'color':'white', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                     filter_action='native', 
                     page_current= 0,
                     page_size= 15,
                    )




            ]),


        html.Div([
        html.H1((' Residuos reciclables más generados y reciclados a nivel Ciudad')),
        html.H2(html.Li(html.Em('¿Cuál es el tipo de residuo que más se genera en la Ciudad? ¿Y el que menos?'))),



                dcc.Graph(id='grafico_51', figure=go.Figure(data=[go.Pie(labels=reciclables_por_comuna_bar.Componente, values=reciclables_por_comuna_bar.Toneladas, hole=.3)],
)







        )]), 
        html.Div([
        html.H2(html.Li(html.Em(' ¿Cuánto del total de cada tipo de residuos reciclables proviene de puntos verdes?'))),
      

                dcc.Graph(id='grafico_5b', figure=px.bar(residuos_merged, x=residuos_merged.recicladosiporc, y=residuos_merged.Tipo_de_residuo,       orientation='h',                               
 labels={'Tipo_de_residuo': 'Tipo de residuo','recicladosiporc' : '% recibido en puntos verdes'}, height=700, width=700 ,))

    

        ]),

        html.P('Desarrollado por Arguto,Fernández Bender, Florido y Pelaez '),       
        ]),
        
         dcc.Tab(id='conclusiones', label='Principales resultados',  children=[


         html.Iframe(id = 'conclu', srcDoc = open('tab_conclusiones.html', 'r').read(), width = '100%', height='600'), 
    
         ]),

     
    
    ]),
    
    

])


#Ejecutar
if __name__ == '__main__':
    app.run_server()

