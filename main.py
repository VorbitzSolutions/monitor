import asyncio
import aiohttp
import logging
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler
import ssl
from async_db import DbAccess
from monitor import Monitor
from config import configuration

# Database connection details
RESULT_ERROR = False
RESULT_OK =True
#DATABASE_URL = "postgresql://postgres@localhost:5432/liveurl"

# Get config values
db_name,db_user,looptime,appid,sendmsgid = configuration()

log = Logger.with_default_handlers(
    level=logging.INFO
)

file_handler = AsyncFileHandler(filename='app.log', mode='w')
log.add_handler(file_handler)

db = DbAccess(log,db_name,db_user,appid,sendmsgid)
dm_monitor = Monitor(log,appid,sendmsgid)

# Main function to run the scraping process
async def main():
    await log.info("Starting.")

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

#            rows = await db.get_all_rows_sql

            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                tasks = [dm_monitor.scrape_url(session, row) for row in domains_list]
                await asyncio.gather(*tasks)

        except RuntimeError as r:
            # Handle the error
            await log.error(f"An error occurred in run(): {r}")
        except Exception as x:
            # Handle the error
            await log.error(f"An error occurred in run(): {x}")
        finally:
            domains_list.clear()

        await log.info("Done")
        await asyncio.sleep(looptime)

if __name__ == "__main__":
    asyncio.run(main())
    # Close the logger and release resources
    log.shutdown()
