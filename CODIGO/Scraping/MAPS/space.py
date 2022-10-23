#install googlemaps pip install -U googlemaps
import googlemaps as gm
import pandas as pd
import json

#sentiment analysis
from nltk.sentiment import SentimentIntensityAnalyzer as sia

gmaps = gm.Client(key='AIzaSyDutpd8aWodj-mQ-qUvBrapIWp5KzcC8D4')

#parametrizar ruta
PATH = 'C:\\Users\\nicle\\OneDrive\\Documentos\\PROYECTOS\\HACKATON BBVA 2022\\DATOS\\DB\\'

#este no se usa en la ejecucion
df = pd.read_csv(PATH+'Final_Data_Hackathon_2022.csv')

#caso muestra: en produccion deberia ser el csv enviado por el dashboard
#load 10 casos
csv = pd.read_csv(PATH+'Empresas_cercanas.csv',encoding="ISO-8859-1")
csv_10 = csv.iloc[0:11:1]

#funciones
def places(busqueda):
    places_result_x = gmaps.places(busqueda)
    try:
        place_id_x = places_result_x['results'][0]['place_id']
        place_x = gmaps.place(place_id = place_id_x)
    except IndexError:
        place_x = []
    return places_result_x, place_x

#construye frases de busqueda
def busquedas(data):
    lista =[]
    for name in range(len(data.index)):
        #busqueda = muestra.iloc[name]['NombComp']+', '+muestra.iloc[name]['Direccion1']+', '+muestra.iloc[name]['Colonia']+', '+muestra.iloc[name]['MunicipioDel']
        busqueda = data.iloc[name]['Nombre']+', '+data.iloc[name]['municipio.y']+', '+data.iloc[name]['entidad']
        lista.append(busqueda)
    return lista

#itera las busquedas
def itera_busquedas(lista_busquedas, data, limit):
    results_10 = {Nombre:[] for Nombre in data['Nombre']}
    for name in range(limit):
        busqueda = lista_busquedas[name]
        results_10[data.iloc[name]['Nombre']] = list(places(busqueda))
    return results_10

#acotamos seaches para el ejemplo
searches = busquedas(csv)
searches_1 = searches[:11]

#ejecucion de la funcion
resultados = itera_busquedas(searches, csv, 68)

#construccion del output
output = dict()
for k in resultados.keys():
    dic_aun = {ka:resultados[k][0]['results'][0][ka] for ka in resultados[k][0]['results'][0] if ka in ['types','user_ratings_total','rating','name','formatted_address','business_status']}
    dic_aun2 = {ka:resultados[k][1]['result'][ka] for ka in resultados[k][1]['result'] if ka in ['opening_hours','formatted_phone_number','reference','reviews','types','vicinity','website']}
    if 'reviews' in dic_aun2.keys():
        for rev in range(len(dic_aun2['reviews'])):
            texto = dic_aun2['reviews'][rev]['text']
            dic_aun2['reviews'][rev]['sentiment'] = sia().polarity_scores(texto)['compound']
    output[k] = [dic_aun,dic_aun2]

#creando el json de salida
with open(PATH+'output.json','w') as f:
    json.dump(output,f)