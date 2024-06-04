import requests
import os
import sys
import pandas as pd
from loguru import logger
from bs4 import BeautifulSoup
from utils.parse_engineering_url import get_engineering_url


@logger.catch
def parse_table(table):
    # Инициализация списков для хранения данных таблицы
    headers = []
    rows = []
    datasheet_links = []
    product_links = []

    # Получение заголовков таблицы
    for th in table.find('thead').find_all('th'):
        headers.append(th.text.strip())

    # Получение строк таблицы
    for tr in table.find('tbody').find_all('tr'):
        row = []
        # наполняем содержимое основных столбцов
        for idx, td in enumerate(tr.find_all('td')):
            # Если ячейка "Photo", сохраняем ссылку на картинку
            if idx == headers.index('Photo'):
                cell_content = td.find('img')['src']

            # Если ячейка "MDS", сохраняем ссылку из нее
            elif idx == headers.index('MDS'):
                cell_content = td.find('a')['href']

            # Если ячейка "Design Files", сохраняем ссылку из нее, добавив домен
            elif idx == headers.index('Design Files'):
                cell_content = "https://www.bourns.com" + str(td.find('a')['href'])

            # Если ячейка "Engineering", то создадим ссылку на 3D модель и step файлы из аргументов вызова функции
            # onclick
            elif idx == headers.index('Engineering'):
                cell_content = get_engineering_url(td.find('span')['onclick'])

            # Если ячейка "Buy Now", сохраняем ссылку из нее, добавив домен
            elif idx == headers.index('Buy Now'):
                cell_content = "https://www.bourns.com" + str(td.find('a')['href'])

            # В остальных случаях просто сохраняем текст
            else:
                cell_content = td.text.strip()
            logger.debug(cell_content)
            row.append(cell_content)

            # создаем массивы со ссылками для дополнительных двух столбцов в конце
            # Если ячейка "Data sheet", сохраняем ссылку из нее в отдельный массив
            if idx == headers.index('Data Sheet'):
                datasheet_links.append(td.find('a')['href'] if td.find('a') else '')

            # Если ячейка "Size", сохраняем ссылку из нее в отдельный массив
            elif idx == headers.index('Size'):
                product_links.append(td.find('a')['href'] if td.find('a') else '')

        rows.append(row)
    headers[headers.index("Data Sheet")] = "Name"
    return rows, headers, datasheet_links, product_links


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

    soup = BeautifulSoup(page_content, 'html.parser')

    # Нахождение таблицы
    table = soup.find('table', {'class': 'productsTable'})

    rows, headers, datasheet_links, product_links = parse_table(table)
    logger.debug(rows)
    # Создание DataFrame с помощью pandas
    df = pd.DataFrame(rows, columns=headers)
    df['Datasheet Link'] = datasheet_links
    df['Product Link'] = product_links

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file = os.path.join(output_directory, f"{category}.csv")
    # Сохранение DataFrame в CSV файл
    df.to_csv(output_file, index=False, encoding='utf-8', lineterminator='\n')


if __name__ == '__main__':
    category = "thick-film-resistors"
    if os.path.exists(f"../output/{category}.html"):
        parse_page(
            category,
            f"../output/{category}.html",
            "../output/"
        )
    else:
        parse_page(
            category,
            f"https://www.bourns.com/products/resistors/{category}",
            "../output/"
        )
