#install googlemaps pip install -U googlemaps
import googlemaps as gm
import pandas as pd
import json

#sentiment analysis
from nltk.sentiment import SentimentIntensityAnalyzer as sia

gmaps = gm.Client(key='')

#parametrizar ruta
PATH = 'F:\hackaton\Hackaton-BBVA-2022-Conjunto-de-Cantor\DATOS\DB\\'

#este no se usa en la ejecucion
df = pd.read_csv(PATH+'Final_Data_Hackathon_2022.csv')

#caso muestra: en produccion deberia ser el csv enviado por el dashboard
#load 10 casos
csv = pd.read_csv(PATH+'lista_coincidencias_DINUE.csv')
csv_10 = csv.iloc[0:11:1]

#cercanas
cercanas = pd.read_csv(PATH+)

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
        busqueda = data.iloc[name]['Nombre1']+', '+data.iloc[name]['MunicipioDel']+', '+data.iloc[name]['Estado']
        lista.append(busqueda)
    return lista

#itera las busquedas
def itera_busquedas(lista_busquedas, data, limit):
    results_10 = {Nombre:[] for Nombre in data['Nombre1']}
    for name in range(limit):
        busqueda = lista_busquedas[name]
        results_10[data.iloc[name]['Nombre1']] = list(places(busqueda))
    return results_10

#acotamos seaches para el ejemplo
searches = busquedas(csv_10)
searches_1 = searches[:11]

#ejecucion de la funcion
resultados = itera_busquedas(searches_1, csv_10, 11)

#construccion del output
output = dict()
for k in resultados.keys():
    if resultados[k][0]['status'] == 'OK':
        dic_aun = {ka:resultados[k][0]['results'][0][ka] for ka in resultados[k][0]['results'][0] if ka in ['types','user_ratings_total','rating','name','formatted_address','business_status']}
        dic_aun2 = {ka:resultados[k][1]['result'][ka] for ka in resultados[k][1]['result'] if ka in ['formatted_phone_number','reference','reviews','types','vicinity','website']}
        if 'reviews' in dic_aun2.keys():
            for rev in range(len(dic_aun2['reviews'])):
                texto = dic_aun2['reviews'][rev]['text']
                dic_aun2['reviews'][rev]['sentiment'] = sia().polarity_scores(texto)['compound']
        if 'opening_hours' in resultados[k][1]['result'].keys():
            dic_aun2['weekday_text'] = resultados[k][1]['result']['opening_hours']['weekday_text']
        output[k] = [dic_aun,dic_aun2]
    else:
        output[k] = [dict(),dict()]

#creando el json de salida
with open(PATH+'output.json','w') as f:
    json.dump(output,f)


#empresas cercanas
cercanas = pd.read_csv(PATH+'Empresas_cercanas.csv',index_col=0, encoding='latin-1')

#Nombre Colonia localidad.y entidad
cercanas['search'] = cercanas['Nombre']+', '+cercanas['localidad.y']+', '+cercanas['entidad']
close_search = list(cercanas['search'])

#resultados de la busqueda de empresas cercanas
results_close = dict()
for c in close_search:
    results_close[c] = list(places(c))

#creando objeto de salida
output_c = dict()
for k in results_close.keys():
    if results_close[k][0]['status'] == 'OK':
        dic_aun = {ka:results_close[k][0]['results'][0][ka] for ka in results_close[k][0]['results'][0] if ka in ['types','user_ratings_total','rating','name','formatted_address','business_status']}
        dic_aun2 = {ka:results_close[k][1]['result'][ka] for ka in results_close[k][1]['result'] if ka in ['formatted_phone_number','reference','reviews','types','vicinity','website']}
        if 'reviews' in dic_aun2.keys():
            for rev in range(len(dic_aun2['reviews'])):
                texto = dic_aun2['reviews'][rev]['text']
                dic_aun2['reviews'][rev]['sentiment'] = sia().polarity_scores(texto)['compound']
        if 'opening_hours' in results_close[k][1]['result'].keys():
            dic_aun2['weekday_text'] = results_close[k][1]['result']['opening_hours']['weekday_text']
        output_c[k] = [dic_aun,dic_aun2]
    else:
        output_c[k] = [dict(),dict()]

#creando el json de salida para empresas cercanas
with open(PATH+'output_cercanos.json','w') as f:
    json.dump(output_c,f)

