import pandas as pd
from loguru import logger
from parser.partnumber_parsers.metal import *


def parse_series(headers, products_row, partnumbers):
    rows = pd.DataFrame(columns=headers)
    for partnumbers_index, partnumbers_row in partnumbers.iterrows():

        resistance = tolerance = temperature = power = packaging = " "
        product = products_row["Series"]
        partnum = partnumbers_row["Part Number"]
        # print(f"product: {product}, partnum: {partnum}")
        # logger.debug(f"product -2: {product[-2:]}, partnum -2: {partnum[-2:]}")

        # # если в продукте есть "-", например 'CR0201A-AS'
        # if "-" in product:
        #     # если партнамбер начинается с части продукта до прочерка:
        #     if partnum.startswith(product.split("-")[0]) and product.split("-")[1] in partnum[-2:]:
        #         # если хвост после прочерка в продукте совпадает с концом партнамбера:
        #         if partnum[len(product.split("-")[0])] not in ["A", "Q"]:
        #             print(product, partnum, "ПРОДУКТ С ХВОСТОМ")
        #             resistance, tolerance, temperature, power, packaging = get_specs(partnum)
        #         elif partnum[len(product.split("-")[0])] in ["F", "J", "D"]:
        #             print(product, partnum, "продукт с дополнительной фичей, С ХВОСТОМ")
        #             resistance, tolerance, temperature, power, packaging = get_specs(partnum)
        #         else:
        #             continue
        #     else:
        #         continue
        # если партнамбер начинается с продукта
        # 'CRS1206-FX-1002ELF' начинается с 'CRS1206'
        # 'CRS1206AFX-1002ELF' начинается с 'CRS1206A'
        # также будет справедливо для пары 'CRS1206AFX-1002ELF' и 'CRS1206', это следует отсеить дополнительным условием
        if partnum.startswith(product):
            # следующий после названия продукта в партнамбере символ должен быть прочерк,
            # если буква A или Q - то это не наш вариант
            # потому что 'CRS1206AFX-1002ELF' не является партнамбером для продукта 'CRS1206', а для продукта 'CRS1206A'
            if partnum[len(product)] not in ["A", "Q"]:
                print(product, partnum, "продукт без хвоста")
                resistance, tolerance, temperature, power, packaging = get_specs(partnum)
            elif partnum[len(product)] in ["F", "J", "D", "C", "K", "R"]:
                print(product, partnum, "продукт с дополнительной фичей, без хвоста")
                resistance, tolerance, temperature, power, packaging = get_specs(partnum)
            # в остальных случаях идем на следующую итерацию
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

