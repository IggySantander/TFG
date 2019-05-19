from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://www.ingrammicrocloud.com/')
print(driver.title)
prvcy = driver.find_element_by_css_selector(".agree-button.btn.btn-secondary.btn-sm.custom_agree")
prvcy.click()
driver.save_screenshot("Pagina-principal.png")
print ("Elements of main menu")
for i in range(1,5):
    menu=driver.find_element_by_css_selector('#block-mainnavigation > div > ul > li:nth-child(%s)' %i)
    menu.click()
    time.sleep(1)
    campos=driver.find_elements_by_css_selector('.link-box.link-box-small')
    for campo in campos:
        if campo.text != "":
            print campo.text
            print campo.get_attribute('href')
time.sleep(1)
menu=driver.find_element_by_css_selector('a[href*="blog"')
menu.click()
time.sleep(1)
print ("Finding specific blog....")
while(len(driver.find_elements_by_css_selector("a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']"))== 0):
    time.sleep(1)
    element1 =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[rel="next"]')))
    element1.click()
element2= driver.find_element_by_css_selector("a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']")
element2.click()
print ("Blog selected and displayed!")
time.sleep(2)
element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
element.click()
menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#block-mainnavigation > div > ul > li:nth-child(4)')))
menu.click()
menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[href*="blog"')))
menu.click()
time.sleep(1)
print ("Finding March 2019 Blogs...")
while(len(driver.find_elements_by_css_selector('a[rel="next"]'))!=0):
    element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[rel="next"]')))
    element1.click()
    time.sleep(1)
entries=driver.find_elements_by_css_selector(".blog-box")
print ("March 2019 Blogs:")
for entrie in entries:
    element=entrie.find_element_by_css_selector("a >  div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > time:nth-child(1)")
    if "March" in element.text:
        if "2019" in element.text:
            print element.text
            print entrie.get_attribute('href')

driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
time.sleep(1)
element.click()
print ("Requesting info...")
menu=driver.find_element_by_css_selector("#block-mainnavigation > div > ul > li:nth-of-type(4)")
menu.click()
time.sleep(1)
menu=driver.find_element_by_css_selector('a[href*="contact"')
menu.click()
time.sleep(2)
boton=driver.find_element_by_css_selector('[name*="email"')
boton.send_keys("test.1@hotmail.com")
time.sleep(2)
boton=driver.find_element_by_css_selector('[type*="submit"]')
boton.click()
time.sleep(2)

element=driver.find_element_by_css_selector('.logo')
element.click()
time.sleep(2)

lang=driver.find_element_by_css_selector('.selected-country')
lang.click()
time.sleep(2)
print ("Countries available:")
time.sleep(1)
langs=driver.find_elements_by_css_selector('a[href*="www.ingrammicrocloud"]')
for lang in langs:
    print lang.text
    print lang.get_attribute('href')
lang=driver.find_element_by_css_selector('a[href*=".com/es"]')
lang.click()
time.sleep(3)

#Caso 1 , recogemos todos los href y titulos de los desplegables
element=driver.find_element_by_css_selector('a[href*="partner-stories"]')
element.click()
time.sleep(2)
print ("Partners of Ingram Micro:")
time.sleep(1)
for i in range(2,5):
    menu= driver.find_element_by_css_selector('body > div.dialog-off-canvas-main-canvas > div.wrapper.background-light > div > div:nth-child(2) > div > ul > li:nth-child(%s)' %i)
    menu.click()
    time.sleep(2)
    element = driver.find_element_by_css_selector("body > div.dialog-off-canvas-main-canvas > div.wrapper.background-light > div > div:nth-child(2) > div > ul > li:nth-child(%s) > a" %i)
    print element.text
    campos = driver.find_elements_by_css_selector('.partner-box')
    for campo in campos:
        if campo.text != "":
            print campo.text
            print campo.get_attribute('href')


driver.quit()