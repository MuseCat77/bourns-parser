import os
import pandas as pd
import requests
import aiohttp
import aiofiles
import asyncio
from tqdm.asyncio import tqdm
from loguru import logger
from utils.text_operations import sanitize_filename
import os


async def download_file(sem, session: aiohttp.ClientSession, url: str, output_file):
    async with sem:
        try:
            if not os.path.exists(output_file):
                logger.info(f"связь с космосом {url}")
                async with session.get(url) as response:
                    if response.status == 200:
                        async with aiofiles.open(output_file, "wb") as f:
                            await f.write(await response.read())
        except Exception as e:
            logger.error(e)


async def download_photos(base_directory, df, column):
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as session:
        futures = []
        unique_links = df[column].unique()
        for url in unique_links:
            if pd.notnull(url) and url.strip():  # Проверка наличия URL и его содержимого
                logger.debug(f"{url}")
                basename = sanitize_filename(os.path.basename(url))
                output_file = os.path.join(base_directory, basename)
                futures.append(download_file(sem, session, url, output_file))
        else:
            logger.error(f"[-] Нет ссылки на {column} в ячейке {url}")

        for future in tqdm(asyncio.as_completed(futures), total=len(futures)):
            # await asyncio.sleep(0.1)
            await future


if __name__ == '__main__':
    df = pd.read_csv("../output/thick-film-resistors.csv")
    directory = "../output/Datasheets/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    asyncio.run(download_photos(directory, df, "Datasheet Link"))
