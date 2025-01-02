import asyncio
import logging
import ssl
from datetime import datetime

import aiohttp
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler

from async_db import DbAccess
from config import configuration
from monitor import Monitor

# Database connection details
# DATABASE_URL = "postgresql://postgres@localhost:5432/liveurl"

# Get config values
db_name, db_user, looptime, appid, sendmsgid = configuration()

log = Logger.with_default_handlers(level=logging.INFO)
file_handler = AsyncFileHandler(filename='app.log', mode='w')
log.add_handler(file_handler)


# Main function to run the scraping process
async def main():
    dt = datetime.now()
    await log.info(f"Starting at {dt}.")

    db = DbAccess(log, db_name, db_user, appid, sendmsgid)
    dm_monitor = Monitor(log, appid, sendmsgid)

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # This flag tells the app to load all the domains to be monitored even if their status flags equal 0
    load_data = True

    domains_list = []

    # Loop forever unless an error happens
    while True:
        try:
            # Discover if there are any new or modified domains
            invalidate = await db.invalidate_queue()

            # If there are new / modified domains or if this is the first time since this app started
            # then load the domains_list list.
            if load_data or invalidate:
                domains_list = await db.select_all_tasks()
                if len(domains_list) > 0:
                    await db.change_status(domains_list)
                    load_data = False

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                tasks = [dm_monitor.scrape_url(session, row) for row in domains_list]
                await asyncio.gather(*tasks)

        except RuntimeError as r:
            # Handle the error
            dt = datetime.now()
            await log.error(f"An error occurred in run(): {r} at {dt}")
        except Exception as x:
            # Handle the error
            dt = datetime.now()
            await log.error(f"An error occurred in run(): {x} at {dt}")
        finally:
            domains_list.clear()

            t = await db.shut_down()
            if t:
                # Close the logger and release resources
                dt = datetime.now()
                await log.info(f"Done at {dt}")
                await log.shutdown()
                break

        dt = datetime.now()
        await log.info(f"Loop sleep at {dt}")
        await asyncio.sleep(looptime)


if __name__ == "__main__":
    asyncio.run(main())

