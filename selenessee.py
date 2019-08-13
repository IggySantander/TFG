#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding: utf8
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

class glb:
    logger = None

    
def main():

    glb.logger = setup_logging()
    # Task 00: We open the main window
    #
    # For Firefox geckodriver must be running
    # For Chrome: chromedriver must be running
    # ---------------------------------------
    driver = task_00_open_the_main_window()

    # Task 01: Accepting cookies and saving main page
    # --------------------------------------
    COOKIES_CSS_SELECTOR = ".agree-button.btn.btn-secondary.btn-sm.custom_agree"
    task_01_accepting_cookies(driver, COOKIES_CSS_SELECTOR)

    # Task 02: Getting all elements of menu
    # -------------------------------------
    XPATH_MAIN_MENU_ELEMENT_TO_CLICK = '#block-mainnavigation > div > ul > li:nth-child(%s)'  # %s is the number from 1 to 5
    FIELDS_CSS_SELECTOR = '.link-box.link-box-small'
    task_02_getting_all_elements_of_menu(driver, XPATH_MAIN_MENU_ELEMENT_TO_CLICK, FIELDS_CSS_SELECTOR)

    # Task 03: We enter the blog
    # --------------------------
    BLOG_CSS_SELECTOR = 'a[href*="blog"'
    task_03_enter_the_blog(driver, BLOG_CSS_SELECTOR) 

    # Task 04: Enter in a specific article
    # ------------------------------------
    CSS_SELECTOR_TARGET_ARTICLE = "a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']"
    NEXT_CSS_SELECTOR = 'a[rel="next"]'
    task_04_enter_in_a_specific_article(driver, CSS_SELECTOR_TARGET_ARTICLE, NEXT_CSS_SELECTOR)

    # Task 05:  Navigate back to the blog
    # -----------------------------------
    LOGO_CSS_SELECTOR = ".logo" 
    MAIN_MENU_COMPANY_CSS_SELECTOR = '#block-mainnavigation > div > ul > li:nth-child(4)'
    task_05_navigate_back_to_the_blog(driver, LOGO_CSS_SELECTOR, MAIN_MENU_COMPANY_CSS_SELECTOR, BLOG_CSS_SELECTOR)

    # Task 06: Finding blog entries with date March 2019
    # ---------------------------------------------------
    BLOG_ENTRY_CSS_SELECTOR = ".blog-box"
    BLOG_ENTRY_TIME_CSS_SELECTOR = "a >  div:nth-child(2) > div:nth-child(3) > span:nth-child(1) > time:nth-child(1)"
    task_06_finding_blog_entries_with_date_march_2019(driver, NEXT_CSS_SELECTOR, BLOG_ENTRY_CSS_SELECTOR, BLOG_ENTRY_TIME_CSS_SELECTOR)
    
    # Task 07: Fill in contact form
    # -----------------------------
    CONTACT_CSS_SELECTOR = 'a[href*="contact"'
    EMAIL_ELEMENT_CSS_SELECTOR = '[name*="email"'
    SUBMIT_BUTTON_CSS_SELECTOR = '[type*="submit"]'
    # task_07_fill_in_contact_form(driver, MAIN_MENU_COMPANY_CSS_SELECTOR, CONTACT_CSS_SELECTOR, EMAIL_ELEMENT_CSS_SELECTOR, SUBMIT_BUTTON_CSS_SELECTOR, LOGO_CSS_SELECTOR)

    # Task 08: Find all countries and selecting Spain
    # -----------------------------------------------
    COUNTRY_ELEMENT_CSS_SELECTOR = '.selected-country'
    LANGS_CSS_SELECTOR = 'a[href*="www.ingrammicrocloud"]'
    SPAIN_COUNTRY_CSS_SELECTOR = 'a[href*=".com/es"]'

    task_08_find_all_countries_and_select_spain(driver, COUNTRY_ELEMENT_CSS_SELECTOR, LANGS_CSS_SELECTOR, SPAIN_COUNTRY_CSS_SELECTOR)

    # Task 09: We select all articles in category partner stories
    # -----------------------------------------------------------
    element=driver.find_element_by_css_selector('a[href*="partner-stories"]')
    element.click()
    time.sleep(2)
    glb.logger.info("Partners of Ingram Micro:")
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
    glb.logger.info("Shutting down....")

    driver.quit()

def task_00_open_the_main_window():

    # Task 00: We open the main window
    #
    # For Firefox geckodriver must be running
    # For Chrome: chromedriver must be running
    # ---------------------------------------
    glb.logger.info("Task 00: Launching the browser...")
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://www.ingrammicrocloud.com/')
    glb.logger.info("page title: %s\n\n" % driver.title)

    return driver

def task_01_accepting_cookies(driver, COOKIES_CSS_SELECTOR) :

    # Task 01: Accepting cookies and saving main page
    # --------------------------------------
    glb.logger.info("Task 01: Accepting the cookies and privacy policy...")

    prvcy = driver.find_element_by_css_selector(COOKIES_CSS_SELECTOR)
    prvcy.click()
    driver.save_screenshot("Pagina-principal.png")


def task_02_getting_all_elements_of_menu(driver, XPATH_MAIN_MENU_ELEMENT_TO_CLICK, FIELDS_CSS_SELECTOR) :

    # Task 02: Getting all elements of menu
    # -------------------------------------
    glb.logger.info("Elements of main menu")
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

    glb.logger.info("Main menu information: %s\n\n" % json.dumps(menu_element_list, indent=4))


def task_03_enter_the_blog(driver, BLOG_CSS_SELECTOR) :

    # Task 03: We enter the blog
    # --------------------------
    glb.logger.info("Going to blog page...")
    time.sleep(1)
    menu=driver.find_element_by_css_selector(BLOG_CSS_SELECTOR)
    menu.click()
    time.sleep(1)

def task_04_enter_in_a_specific_article(driver, CSS_SELECTOR_TARGET_ARTICLE, NEXT_CSS_SELECTOR) :

    # Task 04: Enter in a specific article
    # ------------------------------------

    # We click "Load More" untill we find the target article
    criteria_for_element_found = len(driver.find_elements_by_css_selector(CSS_SELECTOR_TARGET_ARTICLE))

    while(criteria_for_element_found == 0):
        time.sleep(1)
        element1 =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,NEXT_CSS_SELECTOR)))
        glb.logger.info("Element1: tag: %s text %s href %s" % (element1.tag_name, element1.text, element1.get_attribute("href")))
        element1.click()
        criteria_for_element_found = len(driver.find_elements_by_css_selector(CSS_SELECTOR_TARGET_ARTICLE))

    glb.logger.debug("Found target CSS selector: Criteria: {}".format(criteria_for_element_found))

    go_to_the_top(driver)
    element2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_TARGET_ARTICLE)))
    glb.logger.debug("Clicking on target element")
    element2.click()
    glb.logger.info("Blog selected and displayed!")
    time.sleep(2)

def task_05_navigate_back_to_the_blog(driver, LOGO_CSS_SELECTOR, MAIN_MENU_COMPANY_CSS_SELECTOR, BLOG_CSS_SELECTOR):
    
    glb.logger.info("Going back to the blog")
    element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, LOGO_CSS_SELECTOR)))
    element.click()

    menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, MAIN_MENU_COMPANY_CSS_SELECTOR)))
    menu.click()
    menu=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BLOG_CSS_SELECTOR)))
    menu.click()
    time.sleep(1)


def task_06_finding_blog_entries_with_date_march_2019(driver, NEXT_CSS_SELECTOR, BLOG_ENTRY_CSS_SELECTOR, BLOG_ENTRY_TIME_CSS_SELECTOR   ) :
    
    # Task 06: Finding blog entries with date March 2019
    # ---------------------------------------------------
    glb.logger.info("Finding March 2019 Blogs...")

    # We need to accumulate ALL the entries.  We click next until there is no more next button
    criteria_for_load_more = len(driver.find_elements_by_css_selector(NEXT_CSS_SELECTOR))!=0
    while criteria_for_load_more :
        element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, NEXT_CSS_SELECTOR)))
        glb.logger.debug("Element1: tag: %s text %s href %s" % (element1.tag_name, element1.text, element1.get_attribute("href")))
        element1.click()
        time.sleep(1)
        criteria_for_load_more = len(driver.find_elements_by_css_selector(NEXT_CSS_SELECTOR))!=0

    # Now we select all entries
    entries = driver.find_elements_by_css_selector(BLOG_ENTRY_CSS_SELECTOR)
    blog_entries_march_2019 = []
    for entry in entries:
        element = entry.find_element_by_css_selector(BLOG_ENTRY_TIME_CSS_SELECTOR)
        if "March" in element.text:
            if "2019" in element.text:
                blog_entries_march_2019.append( OrderedDict([("title", element.text), ("url", entry.get_attribute("href") )]) )

    glb.logger.info("March 2019 Blog entries:\n{}".format(json.dumps(blog_entries_march_2019, indent=4)))
    
    # Go back to top and origin
#    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    go_to_the_top(driver)
    element=WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.logo')))
    time.sleep(1)
    element.click()


def task_07_fill_in_contact_form(driver, MAIN_MENU_COMPANY_CSS_SELECTOR, CONTACT_CSS_SELECTOR, EMAIL_ELEMENT_CSS_SELECTOR, SUBMIT_BUTTON_CSS_SELECTOR, LOGO_CSS_SELECTOR) :

    # Task 07: Fill in contact form
    # -----------------------------
    glb.logger.info("Requesting info...")

    menu=driver.find_element_by_css_selector(MAIN_MENU_COMPANY_CSS_SELECTOR)
    menu.click()
    time.sleep(1)
    menu=driver.find_element_by_css_selector(CONTACT_CSS_SELECTOR)
    menu.click()
    time.sleep(2)
    boton=driver.find_element_by_css_selector(EMAIL_ELEMENT_CSS_SELECTOR)
    boton.send_keys("test.1@hotmail.com")
    time.sleep(2)
    boton=driver.find_element_by_css_selector(SUBMIT_BUTTON_CSS_SELECTOR)
    boton.click()
    time.sleep(2)

    glb.logger.info("Request info sent")
    
    # Back to main page
    element=driver.find_element_by_css_selector(LOGO_CSS_SELECTOR)
    element.click()
    time.sleep(2)

def task_08_find_all_countries_and_select_spain(driver, COUNTRY_ELEMENT_CSS_SELECTOR, LANGS_CSS_SELECTOR, SPAIN_COUNTRY_CSS_SELECTOR) :

    lang=driver.find_element_by_css_selector(COUNTRY_ELEMENT_CSS_SELECTOR)
    lang.click()
    time.sleep(2)
    langs=driver.find_elements_by_css_selector(LANGS_CSS_SELECTOR)
    countries = []
    for lang in langs:
        countries.append(OrderedDict([("country", lang.text), ("url", lang.get_attribute("href"))]))

    glb.logger.info("Country info:\n{}".format(json.dumps(countries, indent=4)))

    lang=driver.find_element_by_css_selector(SPAIN_COUNTRY_CSS_SELECTOR)
    lang.click()
    time.sleep(3)
    


    
    
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
