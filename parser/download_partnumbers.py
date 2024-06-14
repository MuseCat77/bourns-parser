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
        "download.default_directory": os.path.abspath(download_dir),  # Указываем папку для загрузок
        # "download.default_directory": "E:\\bourns-parser\\output\\partnumbers\\",  # Указываем папку для загрузок
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
        driver.set_window_size(1600, 900)
        driver.get(export_page_url)
        driver.execute_script("document.body.style.zoom = '60%'")
        for name in names_array:
            # если в названии есть черта, то ищем все что до нее. Справедливо для metal-strip-chip-resistors,
            # high-power-shunts, chip-resistor-arrays
            if "-" in name:
                name = name.split("-")[0]

            # Серию вводить только символами до знака "-". Как правило поиск CR0201A включит и CR0201A-AS
            # CR0201A-AS - Part number is not in the database. УБРАТЬ ДЛЯ metal-strip-chip-resistors,
            # там результаты поиска будут. Например для CSS2H-2512
            # Если есть nop файл, то скипаем тоже
            # if not "-" in name and not os.path.exists(os.path.join(output_directory, name + ".nop")):
            if not os.path.exists(os.path.join(output_directory, name + ".nop")):

                # если текущая серия скачана, то нет смысла делать это заново
                # возможно стоит проверять на nop файл
                if not os.path.exists(os.path.join(output_directory, name + ".xlsx")):
                    logger.info(name)

                    def search_name():
                        driver.execute_script("document.body.style.zoom = '60%'")
                        # Раскрыть меню со всеми формами, если окно маленькое
                        # try:
                        #     element = driver.find_element(By.CLASS_NAME, 'family_available_lines')
                        #     element.click()
                        # except NoSuchElementException:
                        #     logger.debug("Меню раскрыто")

                        time.sleep(0.1)
                        # Текстовое поле поиска
                        text_field = driver.find_element(By.ID, 'C044_txtPartNumCheck')
                        text_field.clear()
                        text_field.send_keys(name)
                        logger.debug("вставил текст")
                        time.sleep(0.1)
                        # Кнопка поиска
                        submit_button = driver.find_element(By.ID, 'C044_btnSubmitPartNumCheck')
                        driver.execute_script("arguments[0].click();", submit_button)
                        # валится в ElementClickInterceptedException
                        # submit_button.click()
                        logger.debug("нажал на кнопку поиска")

                    def click_export():
                        driver.execute_script("document.body.style.zoom = '60%'")
                        # driver.execute_script("window.scrollTo(0, 1000)")
                        try:
                            download_button = driver.find_element(By.ID, 'C044_btnExportPNList')
                            driver.execute_script("arguments[0].click();", download_button)
                            # валится в ElementClickInterceptedException
                            # download_button.click()
                            logger.debug("нажал на кнопку экспорта")
                            # time.sleep(1)
                        except NoSuchElementException:
                            # если нет кнопки экспорта, то создадим файл с расширением nop (no part number)
                            with open(os.path.join(output_directory, name + ".nop"), "w", encoding="utf-8") as file:
                                file.write("no such part number")
                            return
                    search_name()
                    element = driver.find_element(By.ID, "C044_lblPartNumCheck")
                    if "Part number is not in the database. Please contact Bourns Customer Service/Inside Sales" in element.text:
                        try:
                            with open(os.path.join(output_directory, name + ".nop"), "w", encoding="utf-8") as file:
                                file.write("no such part number")
                        except FileExistsError:
                            os.remove(os.path.join(output_directory, name + ".nop"))
                            with open(os.path.join(output_directory, name + ".nop"), "w", encoding="utf-8") as file:
                                file.write("no such part number")
                        continue
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
    try:
        if df['Name'].isnull().any().any():
            logger.info("Names пустые")
            return get_series(file_path)
        else:
            return df['Name'].tolist()
    except KeyError:
        logger.info("нет Names вообще")
        return get_series(file_path)


def get_series(file_path):
    df = pd.read_csv(file_path)
    series = df['Series'].tolist()
    # for i in range(len(series)):
    #     if " Series".lower() in series[i].lower():
    #         series[i] = series[i].split(" Series")[0]
    #         logger.debug(series[i])
    return series


if __name__ == "__main__":
    # Пример использования
    category = 'chip-resistor-arrays'
    file_path = f'../output/{category}/{category}.csv'

    # достаем кривые имена из даташитов сами
    hardcode_names = []
    # wirewound resistors FW Series Fusible
    hardcode_names.extend([
        'FW10A',
        'FW20A',
        'FW30A',
        'FW50A',
        'FW70A'
    ])
    # wirewound resistors W Series
    hardcode_names.extend(["W" + str(i) + "M" + str(j) for i in range(1, 11) for j in range(10, 100)])
    # wirewound resistors WS Series
    hardcode_names.extend(["WS" + str(i) + "M" + str(j) for i in range(1, 11) for j in range(1, 11)])

    names_array = get_names(file_path)
    # names_array.extend(hardcode_names)
    logger.debug(names_array)
    output_directory = f'../output/{category}/partnumbers/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    get_partnumbers_from_search(names_array, output_directory)
