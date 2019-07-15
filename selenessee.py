import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

import json

from collections import OrderedDict
import logging

def main():

    logger = setup_logging()
    
    # We open the main window
    #
    # For Firefox geckodriver must be running
    # For Chrome: chromedriver must be running
    # ---------------------------------------
    logger.info("Launching the browser...")
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.ingrammicrocloud.com/')
    logger.info("page title: %s\n\n" % driver.title)

    # Accepting cookies and saving main page
    # --------------------------------------
    COOKIES_CSS_SELECTOR = ".agree-button.btn.btn-secondary.btn-sm.custom_agree"
    logger.info("Accepting the cookies and privacy policy...")
    prvcy = driver.find_element_by_css_selector(COOKIES_CSS_SELECTOR)
    prvcy.click()
    driver.save_screenshot("Pagina-principal.png")

    # Going through the menu to capture the elements
    # ----------------------------------------------
    XPATH_MAIN_MENU_ELEMENT_TO_CLICK = '#block-mainnavigation > div > ul > li:nth-child(%s)'  # %s is the number from 1 to 5
    FIELDS_CSS_SELECTOR = '.link-box.link-box-small'
    logger.info("Elements of main menu")
    menu_element_list = []
    for i in range(1, 5) :
        xpath_element_main_menu = XPATH_MAIN_MENU_ELEMENT_TO_CLICK % i
        menu = driver.find_element_by_css_selector(xpath_element_main_menu)
        menu.click()
        time.sleep(1)
        fields = driver.find_elements_by_css_selector(FIELDS_CSS_SELECTOR)
        menu_element_info = OrderedDict([ ("xpath_element", xpath_element_main_menu),
                                          ("element", str(menu)),
                                          ("fields", [] ) ])
        for field in fields:
            if field.text != "":
                menu_element_info["fields"].append( OrderedDict([("text", field.text), ("href", field.get_attribute("href") ) ]) )

        menu_element_list.append(menu_element_info)

    logger.info("Main menu information: %s\n\n" % json.dumps(menu_element_list, indent=4))

    # We enter the blog
    # -----------------
    logger.info("Going to blog page...")
    CSS_SELECTOR_BLOG = 'a[href*="blog"'
    time.sleep(1)
    menu=driver.find_element_by_css_selector(CSS_SELECTOR_BLOG)
    menu.click()
    time.sleep(1)

    # We click next untill no more articles are found
    CSS_SELECTOR_ALL_ARTICLES = "a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']"
    while(len(driver.find_elements_by_css_selector(CSS_SELECTOR_ALL_ARTICLES))== 0):
        NEXT_CSS_SELECTOR = 'a[rel="next"]'
        time.sleep(1)
        element1 =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,NEXT_CSS_SELECTOR)))
        logger.info("Element1: tag: %s text %s href %s" % (element1.tag_name, element1.text, element1.get_attribute("href")))
        element1.click()
    logger.debug("Finishing clicking in element 1")

    
    element2= driver.find_element_by_css_selector(CSS_SELECTOR_ALL_ARTICLES)
    logger.debug("Clicking on element2")
    element2.click()
    logger.info("Blog selected and displayed!")
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


def setup_logging() :

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

    
if __name__ == "__main__" :
    main()
