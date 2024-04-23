import hhru
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import pickle
options = Options()

client = hhru.Client()
driver = webdriver.Chrome(options=options)
driver.get("https://hh.ru")       
cookies = pickle.load(open("hh_cookies.pkl", "rb"))
for cookie in cookies:
     driver.add_cookie(cookie)

vacancies = client.search_vacancies(
  text="Python",
  search_field="name",
  order_by="publication_time",
  schedule="remote"
)

if vacancies: 
    for vacancy in vacancies:
        print(f"Название: {vacancy['name']}")
        
        if vacancy['salary'] and vacancy['salary']['from'] and vacancy['salary']['to']:
            print(f"Зарплата: от {vacancy['salary']['from']} до {vacancy['salary']['to']} {vacancy['salary']['currency']}")
        else:
            print("Зарплата: информация не указана")

        print(f"Компания: {vacancy['employer']['name']}")
        print(f"URL: {vacancy['alternate_url']}")

    
        driver.get(vacancy['alternate_url'])
        try:
            response_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-qa='vacancy-response-link-top']"))
            )
            response_button.click()
            print("Первая кнопка отклика нажата.")
            time.sleep(2) 

        ь
            try:
                second_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-qa='relocation-warning-confirm']"))
                )
                second_button.click()
                print("Вторая кнопка отклика нажата.")
            except Exception as e:
                print("Вторая кнопка отклика не появилась.")

        except Exception as e:
            print(f"Не удалось откликнуться на вакансию: {e}") 
        time.sleep(5) 

        print() 

    driver.quit()
else:
    print("Нет доступных вакансий по заданным критериям.")
