from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.ingrammicrocloud.com/')
print(driver.title)
"""driver.save_screenshot("Pagina-principal.png")"""
menu=driver.find_element_by_css_selector("#block-mainnavigation > div > ul > li:nth-of-type(4)")
menu.click()
time.sleep(3)
menu=driver.find_element_by_css_selector('a[href*="blog"')
menu.click()
time.sleep(3)
prvcy = driver.find_element_by_css_selector(".agree-button.btn.btn-secondary.btn-sm.custom_agree")
prvcy.click()
while(len(driver.find_elements_by_css_selector("a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']"))== 0):
    time.sleep(1)
    element1 = driver.find_element_by_css_selector('a[rel="next"]')
    element1.click()
element2= driver.find_element_by_css_selector("a[href*='blogs/newly-relaunched-ingram-micro-cloud-website-and-blog-are-live']")
element2.click()
time.sleep(2)

driver.get('https://www.ingrammicrocloud.com/')
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
driver.quit()