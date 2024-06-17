import os
import pandas as pd
import shutil
from urllib.parse import urlparse
import asyncio
import csv
from tqdm import tqdm

unique_rows = set()

async def get_filename_from_url(url):
    path = urlparse(url).path
    path = path.split('/')[-1]
    return path.split("?")[0]


async def process_new_datasheet_dir(series, base_dir):
    new_dir_path = os.path.join(base_dir, "sorted", series)
    os.makedirs(new_dir_path, exist_ok=True)
    return new_dir_path


async def add_row_to_csv(row, new_dir, filename):
    global unique_rows
    csv_file = os.path.join(new_dir, f"{filename}.csv")
    fieldnames = row.keys()

    # Составляем уникальный ключ для строки (например, Part Number)
    unique_key = row['Part Number']

    # Проверяем, есть ли уже такой ключ в множестве уникальных строк
    if unique_key in unique_rows:
        return  # Если строка уже есть, не добавляем её повторно
    else:
        unique_rows.add(unique_key)  # Добавляем ключ в множество уникальных строк

    is_new_file = not os.path.exists(csv_file)

    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        if is_new_file:
            writer.writeheader()

        writer.writerow(row)


async def copy_files_semaphore(semaphore, row, base_dir):
    async with semaphore:
        part_number = row['Part Number']
        series = row['Series']
        print(part_number)
        new_dir = await process_new_datasheet_dir(series, base_dir)

        if pd.notnull(row['Datasheet Link']):
            datasheet = await get_filename_from_url(row['Datasheet Link'])
            old_datasheet_path = os.path.join(base_dir, "Datasheets", str(datasheet))
            if os.path.exists(old_datasheet_path):
                if not os.path.exists(os.path.join(new_dir, str(datasheet))):
                    shutil.copy2(old_datasheet_path, os.path.join(new_dir, str(datasheet)))

        if pd.notnull(row['Photo']):
            image = await get_filename_from_url(row['Photo'])
            old_image_path = os.path.join(base_dir, "Images", str(image))
            if os.path.exists(old_image_path):
                if not os.path.exists(os.path.join(new_dir, str(image))):
                    shutil.copy2(old_image_path, os.path.join(new_dir, str(image)))


async def copy_csv(row, index, base_dir):
    part_number = row['Part Number']
    print("csv", part_number)
    series = row["Series"]
    new_dir = await process_new_datasheet_dir(series, base_dir)
    await add_row_to_csv(row, new_dir, series)


async def copy():
    categories = ["thin-film-chip-resistors", "thick-film-chip-resistors", "metal-strip-chip-resistors"]
    for category in categories:
        csv_file_path = f'../output/{category}/merged.csv'
        df = pd.read_csv(f'../output/{category}/merged.csv', sep=";")
        base_dir = f'../output/{category}/'

        # Определение семафора для ограничения количества одновременных задач
        semaphore = asyncio.Semaphore(10)  # Предположим, что вы хотите выполнить не более 10 задач одновременно

        tasks = []
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for index, row in tqdm(enumerate(reader), total=len(df)):
                tasks.append(copy_files_semaphore(semaphore, row, base_dir))
                tasks.append(copy_csv(row, index, base_dir))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(copy())
