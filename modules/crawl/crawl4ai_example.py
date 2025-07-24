import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.redfin.com/CA/Redwood-City/595-Shoal-Cir-94065/home/1520331",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())