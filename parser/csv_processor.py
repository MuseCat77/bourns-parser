import pandas as pd
import os
from loguru import logger
from series_parser import wirewound, thin


# Объединяет xlsx файлы страниц скачанные с сайта в один большой CSV.
# Сортирует по part number
def join_partnumbers(category):
    xlsx_temp_path = f'../output/{category}/partnumbers/'
    merged_csv_path = f'../output/{category}/partnumbers.csv'

    # Список для хранения данных из всех файлов
    all_data = []

    # Чтение данных из каждого файла XLSX и добавление их в список
    for filename in os.listdir(xlsx_temp_path):
        if filename.endswith(".xlsx"):
            filepath = os.path.join(xlsx_temp_path, filename)
            df = pd.read_excel(filepath)
            all_data.append(df)
            logger.info(f"Обработан файл {filename}")

    # Объединение данных из всех файлов в один DataFrame
    merged_df = pd.concat(all_data, ignore_index=True)
    logger.info("Импорт данных в датафрейм...")

    # Сортировка данных по столбцу "Series"
    merged_df = merged_df.sort_values(by=['Part Number'])
    logger.info("Сортировка данных...")

    # Удаление дубликатов
    merged_df = merged_df.drop_duplicates()
    logger.info("Удаление дубликатов...")

    # Сохранение отсортированного DataFrame в файл CSV с точкой с запятой в качестве разделителя
    merged_df.to_csv(merged_csv_path, index=False)
    logger.success(f"Объединенный и отсортированный файл сохранен в формате CSV: {merged_csv_path}")


@logger.catch
def create_small_csv(products_list, partnumbers_list, category):
    small_csv_headers = ["Part Number", "Series", "Model", "Category", "Photo", "Resistance", "Tolerance",
                         "Temperature Coefficient", "Power (Watts)", "Profile/Package Style", "MDS", "Design Files",
                         "Engineering", "Buy Now", "Datasheet Link", "Product Link"
                         ]
    products = pd.read_csv(products_list)
    partnumbers = pd.read_csv(partnumbers_list)
    small_csv = pd.DataFrame(columns=small_csv_headers)

    for products_index, products_row in products.iterrows():
        if category == "wirewound-resistors":
            small_csv = small_csv._append(wirewound.parse_series(small_csv_headers, products_row, partnumbers))
        elif category == "thin-film-chip-resistors":
            small_csv = small_csv._append(thin.parse_series(small_csv_headers, products_row, partnumbers))

    return small_csv


if __name__ == "__main__":
    category = "thin-film-chip-resistors"

    # объединяет все xlsx партнамбер файлы в один csv
    # join_partnumbers(category)

    # генерирует маленькие csv для всех категорий
    small_csv = create_small_csv(
        f"../output/{category}/{category}.csv",
        f"../output/{category}/partnumbers.csv",
        category
    )
    output_file = f"../output/{category}/small_csv.csv"
    small_csv.to_csv(output_file, index=False)
    logger.success(f"CSV file has been saved to {output_file}")
