import pandas as pd
import os
import glob
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from config import WEBDRIVER_PATH
import time
from loguru import logger


# Поиск файла, который только что скачали. Ищем не по времени, а какой-либо уже существующий начинающийся
# на part-numbers-, потому что иногда случается рассинхрон времени. Какой файл вернет, если в директории
# будет несколько файлов - не знаю
# part-numbers-061024-0101.xlsx
# part-numbers-mmddyy-hhmm.xlsx
def find_file_with_prefix(directory, prefix):
    search_pattern = os.path.join(directory, f"{prefix}*")
    files = glob.glob(search_pattern)
    if files:
        return files[0]
    return None


def get_chromium_driver(download_dir):
    options = Options()
    # путь к исполняемому файлу Chromium
    options.binary_location = WEBDRIVER_PATH

    # Настройки профиля браузера
    prefs = {
        "download.default_directory": "E:\\bourns-parser\\output\\partnumbers\\",  # Указываем папку для загрузок
        "download.prompt_for_download": False,  # Отключаем запрос на место сохранения файлов
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True  # Включаем безопасный поиск
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    return driver


@logger.catch()
def get_partnumbers_from_search(names_array, output_directory):
    driver = get_chromium_driver(output_directory)

    try:
        export_page_url = "https://www.bourns.com/products/resistors"
        driver.get(export_page_url)
        for name in names_array:
            # Серию вводить только символами до знака "-". Как правило поиск CR0201A включит и CR0201A-AS
            # CR0201A-AS - Part number is not in the database.
            if not "-" in name:
                # если текущая серия скачана, то нет смысла делать это заново
                # возможно стоит проверять на nop файл
                if not os.path.exists(os.path.join(output_directory, name + ".xlsx")):
                    logger.info(name)

                    def search_name():
                        # Раскрыть меню со всеми формами, если окно маленькое
                        try:
                            element = driver.find_element(By.CLASS_NAME, 'family_available_lines')
                            element.click()
                        except NoSuchElementException:
                            logger.debug("Меню раскрыто")

                        driver.execute_script("window.scrollTo(0, 1000)")
                        time.sleep(0.1)
                        # Текстовое поле поиска
                        text_field = driver.find_element(By.ID, 'C044_txtPartNumCheck')
                        text_field.clear()
                        text_field.send_keys(name)
                        logger.debug("вставил текст")
                        time.sleep(0.1)
                        # Кнопка поиска
                        submit_button = driver.find_element(By.ID, 'C044_btnSubmitPartNumCheck')
                        logger.debug("нажал на кнопку поиска")
                        submit_button.click()

                    def click_export():
                        driver.execute_script("window.scrollTo(0, 1000)")
                        try:
                            download_button = driver.find_element(By.ID, 'C044_btnExportPNList')
                            download_button.click()
                            logger.debug("нажал на кнопку экспорта")
                            # time.sleep(1)
                        except NoSuchElementException:
                            # если нет кнопки экспорта, то создадим файл с расширением nop (no part number)
                            with open(name + ".nop", "w", encoding="utf-8") as file:
                                file.write("no such part number")

                    search_name()
                    # time.sleep(1)
                    click_export()

                    while find_file_with_prefix(output_directory, "part-numbers-") is None:
                        # скрипт виснет где-то здесь, если кнопки экспорта на странице нет
                        time.sleep(0.1)
                        if driver.current_url != export_page_url:
                            logger.info("поймал кд, жду пока вернут на старую страницу")
                            logger.info(driver.current_url)
                            logger.info(export_page_url)
                            while driver.current_url != export_page_url:
                                time.sleep(0.1)
                            logger.info("пытаюсь найти заново")
                            # можно в принципе было все объединить в одну функцию
                            search_name()
                            click_export()
                            # иногда скрипт зависал здесь или чуть ниже
                    old_filename = find_file_with_prefix(output_directory, "part-numbers-")
                    logger.debug("экспортировалось, пытаюсь переименовать")
                    try:
                        os.rename(os.path.join(old_filename), os.path.join(output_directory, name + ".xlsx"))
                    except FileExistsError:
                        os.remove(os.path.join(output_directory, name + ".xlsx"))
                        os.rename(os.path.join(old_filename), os.path.join(output_directory, name + ".xlsx"))

    except NoSuchElementException as e:
        logger.error(e)
        html_code = driver.page_source

        # Сохранение HTML-страницы, в которой нет нужного элемента в файл
        # (если поймали исключение где-то кроме функции click_export()
        with open(output_directory + "page.html", "w", encoding="utf-8") as file:
            file.write(html_code)
    finally:
        driver.quit()


def get_names(file_path):
    df = pd.read_csv(file_path)
    names = df['Name'].tolist()
    return names


if __name__ == "__main__":
    # Пример использования
    file_path = '../output/thick-film-resistors.csv'
    names_array = get_names(file_path)
    logger.debug(names_array)
    output_directory = '../output/partnumbers/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    get_partnumbers_from_search(names_array, output_directory)
