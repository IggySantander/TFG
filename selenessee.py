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
    
    # Task 00: We open the main window
    #
    # For Firefox geckodriver must be running
    # For Chrome: chromedriver must be running
    # ---------------------------------------
    logger.info("Task 00: Launching the browser...")
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.ingrammicrocloud.com/')
    logger.info("page title: %s\n\n" % driver.title)

    # Task 01: Accepting cookies and saving main page
    # --------------------------------------
    logger.info("Task 01: Accepting the cookies and privacy policy...")
    COOKIES_CSS_SELECTOR = ".agree-button.btn.btn-secondary.btn-sm.custom_agree"
    prvcy = driver.find_element_by_css_selector(COOKIES_CSS_SELECTOR)
    prvcy.click()
    driver.save_screenshot("Pagina-principal.png")

    # Task 02: Getting all elements of menu
    # -------------------------------------
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

    # Task 03: We enter the blog
    # --------------------------
    logger.info("Going to blog page...")
    BLOG_CSS_SELECTOR = 'a[href*="blog"'
    time.sleep(1)
    menu=driver.find_element_by_css_selector(BLOG_CSS_SELECTOR)
    menu.click()
    time.sleep(1)

    # Task 04: Enter in a specific article
    # ------------------------------------

    # We click "Load More" untill we find the target article
    CSS_SELECTOR_TARGET_ARTICLE = "a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']"
    criteria_for_element_found = len(driver.find_elements_by_css_selector(CSS_SELECTOR_TARGET_ARTICLE))

    while(criteria_for_element_found == 0):
        NEXT_CSS_SELECTOR = 'a[rel="next"]'
        time.sleep(1)
        element1 =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,NEXT_CSS_SELECTOR)))
        logger.info("Element1: tag: %s text %s href %s" % (element1.tag_name, element1.text, element1.get_attribute("href")))
        element1.click()
        criteria_for_element_found = len(driver.find_elements_by_css_selector(CSS_SELECTOR_TARGET_ARTICLE))

    logger.debug("Found target CSS selector: Criteria: {}".format(criteria_for_element_found))

    go_to_the_top(driver)
    element2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_TARGET_ARTICLE)))
    logger.debug("Clicking on target element")
    element2.click()
    logger.info("Blog selected and displayed!")
    time.sleep(2)

    # Task 05:  Navigate back to the blog
    # -----------------------------------
    LOGO_CSS_SELECTOR = ".logo"
    logger.info("Going back to the blog")
    element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, LOGO_CSS_SELECTOR)))
    element.click()
    MAIN_MENU_COMPANY_CSS_SELECTOR = '#block-mainnavigation > div > ul > li:nth-child(4)'
    menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_MENU_COMPANY_CSS_SELECTOR)))
    menu.click()
    menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BLOG_CSS_SELECTOR)))
    menu.click()
    time.sleep(1)

    # Task 06: Finding blog entries with data March 2019
    # --------------------------------------------
    logger.info("Finding March 2019 Blogs...")

    # We need to accumulate ALL the entries.  We click next until there is no more next button
    criteria_for_load_more = len(driver.find_elements_by_css_selector(NEXT_CSS_SELECTOR))!=0
    while criteria_for_load_more :
        element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_CSS_SELECTOR)))
        logger.debug("Element1: tag: %s text %s href %s" % (element1.tag_name, element1.text, element1.get_attribute("href")))
        element1.click()
        time.sleep(1)
        criteria_for_load_more = len(driver.find_elements_by_css_selector(NEXT_CSS_SELECTOR))!=0

    # Now we select all entries
    BLOG_ENTRY_CSS_SELECTOR = ".blog-box"
    BLOG_ENTRY_TIME_CSS_SELECTOR = "a >  div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > time:nth-child(1)"
    entries = driver.find_elements_by_css_selector(BLOG_ENTRY_CSS_SELECTOR)
    blog_entries_march_2019 = []
    for entry in entries:
        element = entry.find_element_by_css_selector(BLOG_ENTRY_TIME_CSS_SELECTOR)
        if "March" in element.text:
            if "2019" in element.text:
                blog_entries_march_2019.append( OrderedDict([("title", element.text), ("url", entry.get_attribute("href") )]) )

    logger.info("March 2019 Blog entries:\n{}".format(json.dumps(blog_entries_march_2019, indent=4)))
    
    # Go back to top and origin
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
    time.sleep(1)
    element.click()

    # Task 07: Fill in contact form
    # -----------------------------
    logger.info("Requesting info...")

    menu=driver.find_element_by_css_selector(MAIN_MENU_COMPANY_CSS_SELECTOR)
    menu.click()
    time.sleep(1)
    CONTACT_CSS_SELECTOR = 'a[href*="contact"'
    menu=driver.find_element_by_css_selector(CONTACT_CSS_SELECTOR)
    menu.click()
    time.sleep(2)
    EMAIL_ELEMENT_CSS_SELECTOR = '[name*="email"'
    boton=driver.find_element_by_css_selector(EMAIL_ELEMENT_CSS_SELECTOR)
    boton.send_keys("test.1@hotmail.com")
    time.sleep(2)
    SUBMIT_BUTTON_CSS_SELECTOR = '[type*="submit"]'
    boton=driver.find_element_by_css_selector(SUBMIT_BUTTON_CSS_SELECTOR)
    boton.click()
    time.sleep(2)

    logger.info("Request info sent")
    
    # Back to main page
    element=driver.find_element_by_css_selector(LOGO_CSS_SELECTOR)
    element.click()
    time.sleep(2)

    # Task 08: Find all countries and selecting Spain
    # -----------------------------------------------
    COUNTRY_ELEMENT_CSS_SELECTOR = '.selected-country'
    
    lang=driver.find_element_by_css_selector(COUNTRY_ELEMENT_CSS_SELECTOR)
    lang.click()
    time.sleep(2)
    time.sleep(1)
    LANGS_CSS_SELECTOR = 'a[href*="www.ingrammicrocloud"]'
    langs=driver.find_elements_by_css_selector(LANGS_CSS_SELECTOR)
    countries = []
    for lang in langs:
        countries.append(OrderedDict([("country", lang.text), ("url", lang.get_attribute("href"))]))

    logger.info("Country info:\n{}".format(json.dumps(countries, indent=4)))

    SPAIN_COUNTRY_CSS_SELECTOR = 'a[href*=".com/es"]'
    lang=driver.find_element_by_css_selector(SPAIN_COUNTRY_CSS_SELECTOR)
    lang.click()
    time.sleep(3)
    
    # Task 09: We select all articles in category partner stories
    # -----------------------------------------------------------
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

def go_to_the_top(webdriver) :

    webdriver.execute_script("window.scrollTo(0,0);")

def go_to_the_botton(webdriver) :
    webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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
