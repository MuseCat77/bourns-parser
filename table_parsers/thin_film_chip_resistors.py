from loguru import logger
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
        mds_cell = tr.find_all('td')[headers.index('MDS')]
        mds_links = mds_cell.find_all('a')
        # наполняем содержимое основных столбцов
        for link in mds_links:
            row = []
            # наполняем содержимое основных столбцов
            for idx, td in enumerate(tr.find_all('td')):
                # Если ячейка "Photo", сохраняем ссылку на картинку
                if idx == headers.index('Photo'):
                    cell_content = td.find('img')['src']

                # Если ячейка "MDS", сохраняем ссылку из нее
                elif idx == headers.index('MDS'):
                    cell_content = link['href']

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
                # logger.debug(cell_content)
                row.append(cell_content)

                # создаем массивы со ссылками для дополнительных двух столбцов в конце
                # Если ячейка "Data sheet", сохраняем ссылку из нее в отдельный массив
                if idx == headers.index('Data Sheet'):
                    datasheet_links.append(td.find('a')['href'] if td.find('a') else '')

                # Если ячейка "Series", сохраняем ссылку на продукт из нее в отдельный массив
                elif idx == headers.index('Series'):
                    product_links.append(td.find('a')['href'] if td.find('a') else '')

            rows.append(row)
    headers[headers.index("Data Sheet")] = "Name"
    return rows, headers, datasheet_links, product_links

