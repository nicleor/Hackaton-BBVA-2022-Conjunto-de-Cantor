from __future__ import unicode_literals
import numpy as np
import pandas as pd
import time
from selenium import webdriver;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import emoji

def deEmojify(text):
    return emoji.replace_emoji(text," ")
    #get_emoji_regexp().sub(r'', text.decode('utf8'))

#def scraping_NomGaMaps(self):
#    try:
#        return self.driver.

#Formato de la URL para busqueda en Google Maps

#website = 'https://www.google.com/maps/search/la+vaca+de+muchos+colores'
#website = 'https://www.google.com/maps/search/ESFM'
#website = 'https://www.google.com/maps/search/PERFIHERRAJES+IMMSA'
website = 'https://www.google.com/maps/search/financiera+sustentable'
path=r"C:\Users\nicle\OneDrive\Documentos\Drivers\chromedriver.exe"

#abre ventana de chrome
driver=webdriver.Chrome(executable_path=path)
driver.get(website)
wait = WebDriverWait(driver,5)

time.sleep(5)
#nombre=driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1');
nombre=driver.find_element(By.XPATH,'//h1[contains(@class,"fontHeadlineLarge")]').text
print(nombre)
red_social = driver.find_element(By.XPATH,'//a[contains(@data-value,"Abrir el sitio web")]').get_attribute('href')
print(red_social)
calif = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]').text
print(calif)

link_review = driver.find_element(By.XPATH,'//button[contains(@aria-label,"opiniones")]')
link_review.click()

while True:
    time.sleep(2)
    #
    try:
        elemCarga = driver.find_element(By.XPATH,'//div[contains(@class,"lXJj5c Hk4XGb")]')
        actions = ActionChains(driver)

        actions.move_to_element(elemCarga).perform()
    except:
        break



lista_rev = driver.find_elements(By.XPATH,'//span[contains(@class,"wiI7pd")]')

lista_fecha = driver.find_elements(By.XPATH,'//span[contains(@class,"rsqaWe")]')

lista_rev_txt = []
for rev in lista_rev:
    lista_rev_txt.append(rev.text)
    #print(lista_rev_txt)

lista_fecha_txt=[]
for fecha in lista_fecha:
    lista_fecha_txt.append(fecha.text)
    #print(lista_fecha_txt)
#print(driver.find_element(By.ID,lista[0]._id).text)

driver.quit()
v_registro = {'Nombre':[nombre],'PáginaWeb':[red_social],'Calificación':[calif],'Reviews':deEmojify([",".join(lista_rev_txt)]),'FechaReviews':[",".join(lista_fecha_txt)]}
print(v_registro)
df_datMaps = pd.DataFrame(data=v_registro)



#print(deEmojify([",".join(lista_rev_txt)]))

#Valores que regresa
df_datMaps.to_csv(r"C:\Users\nicle\OneDrive\Documentos\scraping_Maps2.csv",encoding='UTF-8')


#Ejemplo----No pelar
#def scrapingMAPS(nom_empresa,direccion):
#    return 