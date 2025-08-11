import asyncio
import os
import json
# import webbrowser
# from PIL import Image
# import pytesseract
# from datetime import datetime   
from langchain.schema import Document
# from newsapi import NewsApiClient
from crawl4ai import AsyncWebCrawler
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from crawl4ai import *


# === Load .env variables ===
load_dotenv()


# import os
# import json
# import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any, List

import os
import json
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from crawl4ai import AsyncWebCrawler
from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI
# from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI


@dataclass
class ScraperConfig:
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0


class PropertyScraper:
    def __init__(self, config: Optional[ScraperConfig] = None):
        self.config = config or ScraperConfig()
        self._llm: Optional[ChatOpenAI] = None

    async def fetch_property_info(self, url: str) -> Dict[str, Any]:
        """抓取网页 → 传给 LLM → 返回提取后的结构化信息"""
        text = await self._fetch_redfin_text(url)
        return self._extract_info_from_text_content(text)

    async def _fetch_redfin_text(self, url: str) -> str:
        """抓取网页 Markdown 文本"""
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
            print(f"✅ Crawled {url}")
            return result.markdown or ""

    def _extract_info_from_text_content(self, text: str) -> Dict[str, Any]:
        """用 LLM 从文本中提取结构化信息"""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("❌ OPENAI_API_KEY is not set in environment variables.")

        if self._llm is None:
            self._llm = ChatOpenAI(model_name=self.config.model_name, temperature=self.config.temperature)

        prompt_template = ChatPromptTemplate.from_template("""
            You are an intelligent document extractor.

            Given the following raw Redfin text, extract the following structured information:

            1. Address – Full property address
            2. Price – Sale price in USD
            3. Bedrooms – Number of bedrooms
            4. Bathrooms – Number of bathrooms
            5. Size – Living area size in square feet
            6. LotSize – Lot size in square feet (or specify units if different)
            7. YearBuilt – Year the property was built
            8. PropertyType – Type of property (e.g., Single Family Home, Condo)
            9. GarageSpaces – Number of garage spaces (if specified)
            10. Realtor – Listing agent name and agency
            11. URL – Link to the Redfin listing (if provided)
            12. HOA – HOA fee and description (if applicable)
            13. ClimateFactors – Summary of local climate or environmental risks (e.g., flood zone, fire risk)
            14. SchoolRatings – Ratings and names of nearby schools:
                - PrimarySchool:  ("name": ..., "rating": ...)
                - MiddleSchool:  ("name": ..., "rating": ...) 
                - HighSchool: ("name": ..., "rating": ...) 
            15. PricePerSqft – Calculate this as: `price / size`, rounded to 2 decimal places
            16. Description – A brief, cleaned summary of the full listing description

            Redfin Text crawl from website:
            \"\"\"{text}\"\"\" 

            Return your response as a JSON object with keys.
            """)

        messages = prompt_template.format_messages(text=text)
        response = self._llm.invoke(messages)

        try:
            return json.loads(response.content)
        except Exception:
            print("⚠️ JSON parsing failed. Returning raw LLM output.")
            return {"LLM_raw": response.content}


if __name__ == "__main__":
    scraper = PropertyScraper()
    url = "https://www.redfin.com/CA/Sunnyvale/822-Julian-Ter-94085/unit-4/home/172929985"

    data = asyncio.run(scraper.fetch_property_info(url))
    print(json.dumps(data, indent=2, ensure_ascii=False))
