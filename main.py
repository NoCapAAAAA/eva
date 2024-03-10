import time
import pickle
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def main():
# Получаем путь к текущей директории
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Путь к папке с аккаунтами Twitter
    twitters_acc_folder_path = os.path.join(current_directory, 'twitters_acc')

    # Создание экземпляра браузера
    b = webdriver.Firefox()
    b.get('https://twitter.com/home')
    time.sleep(10)
    # Загрузка cookies из файла 'session'
    for cookie in pickle.load(open('session', 'rb')):
        b.add_cookie(cookie)
    b.refresh()


    # Получаем список файлов в папке twitters_acc
    files = os.listdir(twitters_acc_folder_path)

    # Перебираем файлы в папке twitters_acc
    for file_name in files:
        # Формируем полный путь к файлу
        file_path = os.path.join(twitters_acc_folder_path, file_name)
        
        # Проверяем, что файл имеет расширение .txt
        if file_name.endswith('.txt'):
            # Читаем имя пользователя из имени файла
            username = file_name.split('.')[0]
            
            # Открываем файл
            with open(file_path, 'r') as file:
                # Получаем имена пользователей, на которых подписан данный пользователь
                following_users = file.readlines()
                following_users = [user.strip() for user in following_users]
                
                # Переходим на профиль пользователя Twitter
                profile_url = f'https://twitter.com/{username}/following'
                b.get(profile_url)
                time.sleep(5)  # Ждем, чтобы страница полностью загрузилась
                b.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                
                # Перебираем элементы с помощью XPath
                for i in range(1, 50):
                    # Формируем XPath-выражение для каждого элемента
                    xpath_expression = f'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[{i}]/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span'
                    
                    try:
                    # Находим элемент с помощью XPath
                        element = b.find_element(By.XPATH, xpath_expression)
                        with open(file_path, 'a') as file:
                        # Записываем найденный элемент в файл
                            file.write(f"{element.text}\n")
                    except NoSuchElementException:
                        # Если элемент не найден, выводим сообщение об ошибке и продолжаем выполнение
                        print(f"Element with XPath {xpath_expression} not found.")
                        continue

# Закрываем браузер после завершения работы
    b.quit()

