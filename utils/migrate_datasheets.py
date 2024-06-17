import pandas as pd
import os
import shutil
from urllib.parse import urlparse
import asyncio
from tqdm import tqdm


async def get_filename_from_url(url):
    path = urlparse(url).path
    path = path.split('/')[-1]
    return path.split("?")[0]


async def process_new_datasheet_dir(series, base_dir):
    new_dir_path = os.path.join(base_dir, "sorted", series)
    os.makedirs(new_dir_path, exist_ok=True)
    return new_dir_path


async def add_row_to_csv(row, new_dir, filename):
    csv_file = os.path.join(new_dir, f"{filename}.csv")
    df = pd.DataFrame(columns=row.keys())
    df = df._append(row, ignore_index=True)
    # Проверяем, существует ли файл
    if os.path.exists(csv_file):
        # Если файл существует, загружаем его в DataFrame
        existing_df = pd.read_csv(csv_file, sep=";")
        # Добавляем новый DataFrame к существующему
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    else:
        # Если файл не существует, создаем DataFrame только из новых данных
        combined_df = df
    combined_df.to_csv(csv_file, index=False, sep=";")


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


async def copy_csv(df, index, row, base_dir):
    part_number = row['Part Number']
    print("csv", part_number)
    series = row["Series"]
    new_dir = await process_new_datasheet_dir(series, base_dir)
    await add_row_to_csv(row, new_dir, series)


async def copy():
    categories = ["thin-film-chip-resistors", "thick-film-chip-resistors", "metal-strip-chip-resistors"]
    for category in categories:
        df = pd.read_csv(f'../output/{category}/merged.csv', sep=";")
        base_dir = f'../output/{category}/'

        # Определение семафора для ограничения количества одновременных задач
        semaphore = asyncio.Semaphore(10)  # Предположим, что вы хотите выполнить не более 10 задач одновременно

        tasks = []
        for index, row in tqdm(df.iterrows(), total=len(df)):
            tasks.append(copy_files_semaphore(semaphore, row, base_dir))
            tasks.append(copy_csv(df, index, row, base_dir))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(copy())
