from selenium import webdriver
import pickle
import time

driver = webdriver.Chrome()
driver.get('https://hh.ru')


time.sleep(60)  # Увеличьте время, если нужно больше времени на вход

# Сохранение cookies после входа
pickle.dump(driver.get_cookies(), open("hh_cookies.pkl", "wb"))

driver.quit()