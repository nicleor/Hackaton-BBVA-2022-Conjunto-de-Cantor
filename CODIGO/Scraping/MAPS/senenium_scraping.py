from argparse import Action
import time
from selenium import webdriver;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#def scraping_NomGaMaps(self):
#    try:
#        return self.driver.


website = 'https://www.google.com/maps/search/la+vaca+de+muchos+colores'
#website = 'https://www.google.com/maps/search/ESFM'
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



lista = driver.find_elements(By.XPATH,'//span[contains(@class,"wiI7pd")]')

for rev in lista:
    print(rev.text)

#print(driver.find_element(By.ID,lista[0]._id).text)

driver.quit()