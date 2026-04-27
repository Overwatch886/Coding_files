from selenium import webdriver
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
browser.get('https://keep.google.com')
links = browser.find_elements(By.TAG_NAME, 'a')
print(links[0].text)
browser.quit()