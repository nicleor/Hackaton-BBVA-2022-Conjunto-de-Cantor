from __future__ import unicode_literals
import numpy as np
import pandas as pd
import time
#import emoji #pip install emoji
from cleantext import clean
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
    
# Pendientes: {seleccionar la empresa por dirección si hay ambiguedad (i = 3) más rápido
#              caso cuando tarda mucho en ejecutar (i = 4)
#              posiblemente traer más datos de maps
#              arquitectura}
# DEFINIR CUNADO HAYA MÁS DE UNA EMPRESA

df_base = pd.read_csv("C:/Users/nicle/OneDrive/Documentos/Empresas_cercanas.csv",encoding="ISO-8859-1")
df_base['nom_estab'] = df_base['nom_estab'].replace(' ','+')
#df_base['Dirección'] = str(df_base['Direccion1']) + ' ' + str(df_base['Direccion2']) + ' ' + str(df_base['Colonia']) + ' ' + str(df_base['MunicipioDel']) + ' ' + str(df_base['CP']) + ' ' + str(df_base['Estado'])
#df_base['Dirección'] = df_base['Dirección'].replace(' ','+')
    
#Formato de la URL para busqueda en Google Maps
path = 'C:/Users/nicle/OneDrive/Documentos/Drivers/chromedriver.exe'
    
def scraping_NomGaMaps(i,website_nombre,website_lugar):
    #abre ventana de chrome
    driver = webdriver.Chrome(executable_path=path)
    driver.get(website_nombre)
    
    time.sleep(2)
    empresa = driver.find_elements(By.XPATH,'//div[contains(@class,"W4Efsd")]')
    print("longitud de la cadena " + str(len(empresa))) # ejemplo
    
    if len(empresa) > 1:
    
        driver.quit()
    
        #abre ventana de chrome
        driver = webdriver.Chrome(executable_path=path)
        driver.get(website_lugar)

        time.sleep(2) # time.sleep(5)
    
        empresas = driver.find_elements(By.XPATH,'//span[contains(@jstcache,"341")]')
        empresas_txt=[]
        for empresa in empresas:
            empresas_txt.append(empresa.text.lower())
          
        indice = empresas_txt.index(str(df_base.iloc[i,12]).lower())  

        empresa = driver.find_elements(By.XPATH,'//div[contains(@class,"W4Efsd")]')[indice]
        empresa.click()
        #driver.quit()

        time.sleep(3) # time.sleep(5)

        #nombre=driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1');
        nombre=driver.find_element(By.XPATH,'//h1[contains(@class,"fontHeadlineLarge")]').text
        #print(nombre)
        try:
            red_social = driver.find_element(By.XPATH,'//a[contains(@data-value,"Abrir el sitio web")]').get_attribute('href')
        except:
            red_social = ""
        
        try:
            calif = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]').text
        except:
            calif = ""

        try:    
            link_review = driver.find_element(By.XPATH,'//button[contains(@aria-label,"opiniones")]')
        except:
            link_review = ""

        if link_review != "":    
            link_review.click()
            
        #método untill_show
        
        if link_review != "":
            Bool = True
            count = 0
            while Bool and count < 15:
                time.sleep(0.5) # time.sleep(2) # se forza con 0.25

                try:
                    elemCarga = driver.find_element(By.XPATH,'//div[contains(@class,"lXJj5c Hk4XGb")]')
                    actions = ActionChains(driver)

                    actions.move_to_element(elemCarga).perform()
                except:
                    Bool = False
                    count += 1

        try:
            lista_rev = driver.find_elements(By.XPATH,'//span[contains(@class,"wiI7pd")]')
        except:
            lista_rev = ""
        
        try:
            lista_fecha = driver.find_elements(By.XPATH,'//span[contains(@class,"rsqaWe")]')
        except:
            lista_fecha = ""
    
        #try:
        #    lista_graf = driver.find_elements(By.XPATH,'//div[contains(@aria-label,"concurrido")]')
        #except:
        #    graficas = ""

        try:    
            telefono = driver.find_element(By.XPATH,'//div[contains(@jstcache,"opiniones")]')
        except:
            telefono = ""

        lista_rev_txt = []
        for rev in lista_rev:
            lista_rev_txt.append(rev.text)
            #print(lista_rev_txt)

        lista_fecha_txt=[]
        for fecha in lista_fecha:
            lista_fecha_txt.append(fecha.text)
            
        #lista_graf_txt=[]
        #for graf in lista_graf:
        #    lista_graf_txt.append(graf.text)
            #print(lista_fecha_txt)   


        driver.quit()
        v_registro = {'Nombre':[nombre],'PáginaWeb':[red_social],'Calificación':[calif],'Reviews':[",".join(lista_rev_txt)],'FechaReviews':[",".join(lista_fecha_txt)],'Telefono':[telefono]}
        #print(v_registro['Reviews'])
        df_datMaps = pd.DataFrame(data=v_registro)
    
    else:
        #nombre=driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1')
        nombre=driver.find_element(By.XPATH,'//h1[contains(@class,"fontHeadlineLarge")]').text
        #print(nombre)
        
        try:
            red_social = driver.find_element(By.XPATH,'//a[contains(@data-value,"Abrir el sitio web")]').get_attribute('href')
        except:
            red_social = ""
    
        try:
            calif = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]').text
        except:
            calif = "",
            
        try:    
            link_review = driver.find_element(By.XPATH,'//button[contains(@aria-label,"opiniones")]')
        except:
            link_review = ""
    
        if link_review != "":    
            link_review.click()
    
        #método untill_show
    
        if link_review != "": 
            Bool = True
            count = 0
            while Bool and count < 20:
                time.sleep(0.25) # time.sleep(2) # se forza con 0.25

                try:
                    elemCarga = driver.find_element(By.XPATH,'//div[contains(@class,"lXJj5c Hk4XGb")]')
                    actions = ActionChains(driver)
    
                    actions.move_to_element(elemCarga).perform()
                except:
                    Bool = False
                count += 1

        try:
            lista_rev = driver.find_elements(By.XPATH,'//span[contains(@class,"wiI7pd")]')
        except:
            lista_rev = "",

        try:
            lista_fecha = driver.find_elements(By.XPATH,'//span[contains(@class,"rsqaWe")]')
        except:
            lista_fecha = ""
        
        #try:
        #    lista_graf = driver.find_elements(By.XPATH,'//div[contains(@aria-label,"concurrido")]')
        #except:
        #    graficas = ""
        
        try:    
            telefono = driver.find_element(By.XPATH,'//div[contains(@jstcache,"opiniones")]')
        except:
            telefono = ""
        
        lista_rev_txt = []
        for rev in lista_rev:
            lista_rev_txt.append(rev.text)
            #print(lista_rev_txt)

        lista_fecha_txt=[]
        for fecha in lista_fecha:
            lista_fecha_txt.append(fecha.text)
            #print(lista_fecha_txt)
        #print(driver.find_element(By.ID,lista[0]._id).text)
        
        #lista_graf_txt=[]
        #for graf in lista_graf:
        #    lista_graf_txt.append(graf.text)
        #print(lista_fecha_txt)
    
        driver.quit()
        v_registro = {'Nombre':[nombre],'PáginaWeb':[red_social],'Calificación':[calif],'Reviews':[",".join(lista_rev_txt)],'FechaReviews':[",".join(lista_fecha_txt)],'Telefono':[telefono]}
        #print(v_registro['Reviews'])       
        df_datMaps = pd.DataFrame(data=v_registro)
    return df_datMaps

lista_fallos = []
lista = range(0,67)

for i in lista:
    Cadena_nombre = str(df_base.iloc[i,13])
    website_nombre = 'https://www.google.com/maps/search/' + Cadena_nombre
    Cadena_direccion =  str(df_base.iloc[i,4]) + ' ' + str(df_base.iloc[i,5]) + ' ' + str(df_base.iloc[i,7]) + ' ' + str(df_base.iloc[i,8]) + ' ' + str(df_base.iloc[i,9]) + ' ' + str(df_base.iloc[i,12])
    Cadena_direccion = Cadena_direccion.replace(' ','+')
    website_direccion = 'https://www.google.com/maps/search/' + Cadena_direccion
    print(website_direccion)
    if i == lista[0]:
        try:
            df_datMaps_res = scraping_NomGaMaps(i,website_nombre,website_direccion)
            #df_datMaps_res.iloc[0,0] = str(i) + ".-" + str(df_datMaps_res.iloc[0,0])
            df_datMaps_res.iloc[0,3] = clean(str(df_datMaps_res.iloc[0,3]), no_emoji=True)
        except:
            lista_fallos = [Cadena_nombre]
    else:
        try:
            df_datMaps_res1 = scraping_NomGaMaps(i,website_nombre,website_direccion)
            #df_datMaps_res1.iloc[0,0] = str(i) + ".-" + str(df_datMaps_res1.iloc[0,0])
            df_datMaps_res1.iloc[0,3] = clean(str(df_datMaps_res1.iloc[0,3]), no_emoji=True)
            df_datMaps_res = pd.concat([df_datMaps_res,df_datMaps_res1])
            print(i)
        except:
            lista_fallos.append(str(i) + ".-" + Cadena_nombre)
    
print(lista_fallos)
print(len(lista_fallos)) 

#df_datMaps_res

print(len(df_datMaps_res))

df_datMaps_res.to_csv(r"C:\Users\nicle\OneDrive\Documentos\Hackaton\BBVA 2022\scraping_bva_cercanas.csv",encoding='ISO-8859-1')