import requests
import os
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from table_parser import parse_table


@logger.catch
def parse_page(category: str, url: str, output_directory: str):
    page_content = ""
    if "http" not in url:
        logger.info(f"Файл уже скачан, открываем {url}")
        with open(url, 'r', encoding='utf-8') as file:
            page_content = file.read()
    else:
        # Получение содержимого страницы
        logger.info(f"Ждем ответ от {url}")
        response = requests.get(url)
        response.encoding = 'utf-8'

        # Проверка успешности запроса
        if response.status_code == 200:
            logger.info("Начинаем парсинг")
            # Парсинг HTML с помощью BeautifulSoup
            page_content = response.text
            output_file = os.path.join(output_directory, f'{category}.html')
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(page_content)
        else:
            logger.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    page_content = page_content.replace(';', ',').replace("<br>", " ")
    soup = BeautifulSoup(page_content, 'html.parser')

    # Нахождение таблицы
    table = soup.find('table', {'class': 'productsTable'})
    if table is not None:
        rows, headers, datasheet_links, product_links = parse_table(table)
        logger.debug(rows)
        # Создание DataFrame с помощью pandas
        df = pd.DataFrame(rows, columns=headers)
        nothing_burger = []
        if not datasheet_links == nothing_burger:
            df['Datasheet Link'] = datasheet_links
        if not product_links == nothing_burger:
            df['Product Link'] = product_links

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file = os.path.join(output_directory, f"{category}.csv")
        # Сохранение DataFrame в CSV файл
        df.to_csv(output_file, index=False, encoding='utf-8', lineterminator='\n')
    else:
        logger.error(f"Таблица не найдена на заданной странице: {url}")
        if os.path.exists(os.path.join(output_directory, f'{category}.html.bad')):
            os.remove(os.path.join(output_directory, f'{category}.html.bad'))
        os.rename(
            os.path.join(output_directory, f'{category}.html'),
            os.path.join(output_directory, f'{category}.html.bad')
        )


def init_parser(category):
    if os.path.exists(f"../output/{category}/{category}.html"):
        parse_page(
            category,
            f"../output/{category}/{category}.html",
            f"../output/{category}/"
        )
    else:
        if not os.path.exists(f"../output/{category}/"):
            os.makedirs(f"../output/{category}/")
        parse_page(
            category,
            f"https://www.bourns.com/products/resistors/{category}",
            f"../output/{category}"
        )


if __name__ == '__main__':
    init_parser("high-power-shunts")
    # init_parser("thick-film-chip-resistors")
