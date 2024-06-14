import pandas as pd
from loguru import logger
from parser.partnumber_parsers.thin import *


def parse_series(headers, products_row, partnumbers):
    rows = pd.DataFrame(columns=headers)
    for partnumbers_index, partnumbers_row in partnumbers.iterrows():

        resistance = tolerance = temperature = power = packaging = " "
        product = products_row["Series"]
        partnum = partnumbers_row["Part Number"]
        logger.info(f"product: {product}, partnum: {partnum}")
        logger.debug(f"product -2: {product[-2:]}, partnum -2: {partnum[-2:]}")

        # проверяем текущую строку из партнамберов на серию
        # CRT
        # если текущий продукт начинается на crt и не заканчивается на as
        # если текущий партнамбер начинается на crt и не заканчивается на AS
        # если совпадают типоразмеры:
        if product[0:3] == "CRT" and not product[-2:] == "AS" and partnum[0:3] == "CRT" and not partnum[-2:] == "AS" and product[3:7] == partnum[3:7]:
            logger.debug("CRT")
            resistance, tolerance, temperature, power, packaging = crt_series(partnum)

        # CRT-AS парсится по тем же правилам
        # если текущий продукт начинается на crt и не заканчивается на as
        # если текущий партнамбер начинается на crt и не заканчивается на AS
        # если совпадают типоразмеры
        elif product[0:3] == "CRT" and product[-2:] == "AS" and partnum[0:3] == "CRT" and partnum[-2:] == "AS" and product[3:7] == partnum[3:7]:
            logger.debug("CRT-AS")
            resistance, tolerance, temperature, power, packaging = crt_series(partnum)

        # если текущая ячейка не подходит не под одно правило, то идем на следующую итерацию
        else:
            logger.debug("skip")
            continue

        # добавление данных в новую строку датасета через словарь
        new_row = {
            "Part Number": partnumbers_row["Part Number"],
            "Series": products_row["Series"],
            "Model": partnumbers_row["Model"],
            "Category": partnumbers_row["Category"],
            "Photo": products_row["Photo"],
            "Resistance": resistance,
            "Tolerance": tolerance,
            "Temperature Coefficient": temperature,
            "Power (Watts)": power,
            "Profile/Package Style": packaging,
            "MDS": products_row["MDS"],
            "Design Files": products_row["Design Files"],
            "Engineering": products_row["Engineering"],
            "Buy Now": products_row["Buy Now"],
            "Datasheet Link": products_row["Datasheet Link"],
            "Product Link": products_row["Product Link"]
        }
        logger.debug(new_row)
        # добавляем новую строку к датасету
        rows = rows._append(new_row, ignore_index=True)
    return rows
