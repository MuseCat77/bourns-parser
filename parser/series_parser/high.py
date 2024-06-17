import pandas as pd
from loguru import logger
from parser.partnumber_parsers.high import *


def parse_series(headers, products_row, partnumbers):
    rows = pd.DataFrame(columns=headers)
    for partnumbers_index, partnumbers_row in partnumbers.iterrows():

        resistance = packaging = " "
        product = products_row["Name"]
        partnum = partnumbers_row["Part Number"]
        # print(f"product: {product}, partnum: {partnum}")
        # logger.debug(f"product -2: {product[-2:]}, partnum -2: {partnum[-2:]}")

        if product.split("-")[1] in partnum:
            if product.split("-")[2] == "0" and (partnum[-2:] == "00" or partnum[-2:] == "T0"):
                resistance, packaging = get_specs(partnum)
            elif product.split("-")[2] == "1" and (partnum[-2:] == "01" or partnum[-2:] == "T1"):
                resistance, packaging = get_specs(partnum)
            elif product.split("-")[2] == "2" and (partnum[-2:] == "02" or partnum[-2:] == "T2"):
                resistance, packaging = get_specs(partnum)
            elif product.split("-")[2] == "x0" and (partnum[-2:] == "20" or partnum[-2:] == "30"):
                resistance, packaging = get_specs(partnum)
            elif product.split("-")[2] == "x1" and (partnum[-2:] == "21" or partnum[-2:] == "31"):
                resistance, packaging = get_specs(partnum)
            elif product.split("-")[2] == "x2" and (partnum[-2:] == "22" or partnum[-2:] == "32"):
                resistance, packaging = get_specs(partnum)
            else:
                continue
        # если текущая ячейка не подходит не под одно правило, то идем на следующую итерацию
        else:
            # logger.debug("skip")
            continue

        # добавление данных в новую строку датасета через словарь
        new_row = {
            "Part Number": partnumbers_row["Part Number"],
            "Series": products_row["Series"],
            "Model": partnumbers_row["Model"],
            "Category": partnumbers_row["Category"],
            "Photo": products_row["Photo"],
            "Resistance": resistance,
            "Tolerance": products_row["Tolerances"],
            "Temperature Coefficient": products_row["Temperature Coefficient"],
            "Power (Watts)": products_row["Power per Resistor"],
            "Profile/Package Style": packaging,
            "MDS": products_row["MDS"].replace("\n", " "),
            "Design Files": products_row["Design Files"],
            "Engineering": products_row["Engineering"],
            "Buy Now": products_row["Buy Now"],
            "Datasheet Link": products_row["Datasheet Link"],
        }
        logger.debug(new_row)
        # добавляем новую строку к датасету
        rows = rows._append(new_row, ignore_index=True)
    return rows

