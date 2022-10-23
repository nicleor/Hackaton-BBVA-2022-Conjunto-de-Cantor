import  nltk
import pandas as pd
import math

nltk.download('vader_lexicon')
nltk.download('punkt')

df_analisis = pd.DataFrame(pd.read_csv(r"C:\Users\sentr\OneDrive\Escritorio\scraping_bbva\scraping_bbva_T30.csv",encoding='ISO-8859-1'))
df_analisis['Reviews'].fillna("",inplace=True)

Col = [i for i in range(len(df_analisis['Reviews']))]
for i in range(len(df_analisis['Reviews'])):
	
	palabras = df_analisis.iloc[i,3]

	import translators as ts
	if palabras != "":
		try:
			palabras = ts.google(palabras,from_lenguage="es",to_lenguage="en")
		except:
			palabras = ""
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	palabras = tokenizer.tokenize(palabras)

	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	from nltk import sentiment
	from nltk import word_tokenize

	analizador = SentimentIntensityAnalyzer()

	import statistics as st

	lista = []
	for palabra in palabras:
		scores = analizador.polarity_scores(palabra)
		if scores['compound'] != 0:
			lista.append(scores['compound'])

	if lista != []:
		Prom = st.mean(lista)
	else:	 
		Prom = 0

	Col[i] = Prom

df_analisis = df_analisis[['Nombre','PáginaWeb','Calificación','Reviews','FechaReviews']]
Col = pd.DataFrame({'sentimiento': Col})

#Col = Col.rename(columns={'': 'Sentimiento'})

Base = pd.concat([df_analisis,Col], axis=1)
#Base.set_axis(['Nombre','PáginaWeb','Calificación','Reviews','FechaReviews','Sentimientos'], axis=1)
Base.to_csv(r"C:\Users\sentr\OneDrive\Escritorio\scraping_bbva\scraping_bva_T30_A.csv",encoding='ISO-8859-1')