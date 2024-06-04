import os
import pandas as pd
import requests
import aiohttp
import aiofiles
import asyncio
from tqdm.asyncio import tqdm
import logging
import os
from datetime import datetime


log_directory = "logs/"

log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
log_filepath = os.path.join(log_directory, log_filename)

# Создание директории для логов
os.makedirs(log_directory, exist_ok=True)

# Настройка логирования
# Имя лог-файла на основе времени и даты запуска программы
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', handlers=[
    logging.FileHandler(log_filepath, encoding='utf-8'),
    logging.StreamHandler()
])


# Вывод сообщения в консоль через логгер
def log_message(message):
    logging.info(message)
    # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # log_message()(f"[{current_time}] {message}")


async def download_file(sem, session: aiohttp.ClientSession, url: str, output_file):
    async with sem:
        try:
            if not os.path.exists(output_file):
                log_message(f"связь с космосом {url}")
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(output_file, "wb") as f:
                            await f.write(await response.read())
        except Exception as e:
            log_message(e)


async def download_photos(base_directory, df, column):
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as session:
        futures = []
        unique_links = df[column].unique()
        for url in unique_links:
            if pd.notnull(url) and url.strip():  # Проверка наличия URL и его содержимого
                log_message(f"{url}")
                basename = os.path.basename(url)
                output_file = os.path.join(base_directory, basename)
                futures.append(download_file(sem, session, url, output_file))
        else:
            log_message(f"[-] Нет ссылки на {column} в ячейке {url}")

        for future in tqdm(asyncio.as_completed(futures), total=len(futures)):
            # await asyncio.sleep(0.1)
            await future


if __name__ == '__main__':
    df = pd.read_csv("output/cgsubCeramicCapacitors/merged.csv")
    directory = "output/cgsubCeramicCapacitors/Datasheets/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    asyncio.run(download_photos(directory, df, "datasheets"))
