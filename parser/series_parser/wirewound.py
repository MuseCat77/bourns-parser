import pandas as pd
import os
from loguru import logger
from utils.text_operations import extract_base_datasheet_filename
from parser.partnumber_parsers.wirewound import *


@logger.catch
def create_small_csv(products_list, partnumbers_list):
    small_csv_headers = ["Part Number", "Series", "Model", "Category", "Photo", "Resistance", "Tolerance",
                         "Temperature Coefficient", "Power (Watts)", "Profile/Package Style", "MDS", "Design Files",
                         "Engineering", "Buy Now", "Datasheet Link", "Product Link"
                         ]
    products = pd.read_csv(products_list)
    partnumbers = pd.read_csv(partnumbers_list)
    small_csv = pd.DataFrame(columns=small_csv_headers)

    for products_index, products_row in products.iterrows():
        for partnumbers_index, partnumbers_row in partnumbers.iterrows():

            resistance = tolerance = temperature = power = " "

            # проверяем текущую строку из партнамберов на серию
            # FW
            if products_row["Series"] == "FW Series Fusible" and partnumbers_row["Part Number"][0:2] == "FW":
                resistance, tolerance, temperature, power = fw_series(partnumbers_row["Part Number"])

            # W
            elif products_row["Series"] == "W Series" and partnumbers_row["Part Number"][0:1] == "W" and not partnumbers_row["Part Number"][0:2] == "WS":
                resistance, tolerance, temperature, power = w_series(partnumbers_row["Part Number"])

            # WS
            elif products_row["Series"] == "WS Series Surge Withstand" and partnumbers_row["Part Number"][0:2] == "WS":
                resistance, tolerance, temperature, power = ws_series(partnumbers_row["Part Number"])

            # PWR2010
            elif products_row["Series"] == "PWR2010" and "PWR2010" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2010_series(partnumbers_row["Part Number"])

            # PWR3014
            elif products_row["Series"] == "PWR3014" and "PWR3014" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2010_series(partnumbers_row["Part Number"])

            # PWR4318
            elif products_row["Series"] == "PWR4318" and "PWR4318" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2010_series(partnumbers_row["Part Number"])

            # PWR5322
            elif products_row["Series"] == "PWR5322" and "PWR5322" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2010_series(partnumbers_row["Part Number"])

            # PWR2615
            elif products_row["Series"] == "PWR2615" and "PWR2615" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2615_4525_series(partnumbers_row["Part Number"])

            # PWR4525
            elif products_row["Series"] == "PWR4525" and "PWR4525" in partnumbers_row["Part Number"]:
                resistance, tolerance, temperature, power = pwr2615_4525_series(partnumbers_row["Part Number"])

            # если текущая ячейка не подходит не под одно правило, то идем на следующую итерацию
            else:
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
                "Profile/Package Style": products_row["Profile/Package Style"],
                "MDS": products_row["MDS"],
                "Design Files": products_row["Design Files"],
                "Engineering": products_row["Engineering"],
                "Buy Now": products_row["Buy Now"],
                "Datasheet Link": products_row["Datasheet Link"],
                "Product Link": products_row["Product Link"]
            }
            logger.debug(new_row)
            # добавляем новую строку к датасету
            small_csv = small_csv._append(new_row, ignore_index=True)

    return small_csv


if __name__ == "__main__":
    small_csv = create_small_csv(
        "../../output/wirewound-resistors/wirewound-resistors.csv",
        "../../output/wirewound-resistors/partnumbers.csv"
    )
    output_file = "../../output/wirewound-resistors/small_csv_output.csv"
    small_csv.to_csv(output_file, index=False)
    logger.success(f"CSV file has been saved to {output_file}")
