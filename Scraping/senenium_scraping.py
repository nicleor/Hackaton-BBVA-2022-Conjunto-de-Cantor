import time
from selenium import webdriver;
from selenium.webdriver.common.by import By

#def scraping_NomGaMaps(self):
#    try:
#        return self.driver.


website = 'https://www.google.com/maps/search/la+vaca+de+muchos+colores';
path=r"C:\Users\nicle\OneDrive\Documentos\Drivers\chromedriver.exe";

#abre ventana de chrome
driver=webdriver.Chrome(executable_path=path);
driver.get(website);
#nombre=driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1');
nombre=driver.find_element(By.XPATH,'//h1[contains(@class,"fontHeadlineLarge")]');

print(nombre.text)


#time.sleep(5);
#driver.quit();

