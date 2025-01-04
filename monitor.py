from datetime import datetime
from dbfields import Fields


class Monitor:

    def __init__(self, log, appid, sendmsgid):
        self.log = log
        self.appid = appid
        self.sendmsgid = sendmsgid

    async def build_msg(self) -> str:
        s: str = '{ "firstname" : "Claire","location" : "United Kingdom","blog" : [{ "id" : "1","title" : "Welcome to my blog" },{ "id" : "2", "title" : "My first programming language" }]}'
        return s

    async def validate(self, web_text: str, key_word: str, any_words: [], no_words: []) -> bool:
        txt = str(web_text).lower()
        val_status: bool = key_word in txt and any(word in txt for word in any_words) and not any(
            word in txt for word in no_words)
        return val_status

    # Function to scrape a single URL
    async def scrape_url(self, session, row):
        """Scrapes the given URL using aiohttp."""
        v_status: bool = False
        code:int = 0

        try:
            '''
            # https://docs.aiohttp.org/en/stable/client_advanced.html
            # use proxy when ready
            proxy_auth = aiohttp.BasicAuth('user', 'pass')
            async with session.get("http://python.org",
                                   proxy="http://proxy.com",
                                   proxy_auth=proxy_auth) as response:
            '''
            url = row[Fields.url.value]
            async with session.get(url) as response:
                # response.raise_for_status()  # Raise an exception for bad status codes
                code = response.status
                html = response.text()
                txt = html.lower()
                if code <= 299 and html is not None:
                    v_status = await self.validate(txt, row[Fields.kword.value],
                                                   row[Fields.awords.value],
                                                   row[Fields.nwords.value])
                elif html is None:
                    dt = datetime.now()
                    await self.log.error(f"Http Code = {code} for {url} at {dt}")
                    v_status = False
                else:
                    v_status = True

                # Extract data from the scraped page (example: extract all links)
                # v_status = True if the page returned for the url meets the criteria defined for the page
                # or when the domain name does not resolve to an active page
                dt = datetime.now()
                await self.log.info(f"Scraped {row[Fields.url.value]} Validate: {v_status} Http Code = {code} at {dt}")

        except Exception as e:
            dt = datetime.now()
            await self.log.error(f"Error scraping {row[Fields.url.value]}: {e} at {dt}")
        finally:
            return v_status, code
