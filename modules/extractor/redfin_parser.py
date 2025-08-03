# import os
# from PIL import Image
# import pytesseract
# from datetime import datetime
# import json
# import webbrowser   
# from langchain.schema import Document
# from langchain_community.document_loaders import TextLoader
# from langchain_community.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from dotenv import load_dotenv

# # === Load .env variables ===
# load_dotenv()

# def txt_llm():
#     # === Load your OpenAI key (make sure it’s set) ===
#     os.environ["OPENAI_API_KEY"]

#     # === Load Redfin .txt file ===
#     loader = TextLoader("/Users/yebingcong/code/ai_agent/data/example1/raw/redfin.txt")
#     docs = loader.load()
#     text = docs[0].page_content

#     # === LLM setup ===
#     llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

#     # === Prompt Template ===
#     prompt_template = ChatPromptTemplate.from_template("""
#     You are an intelligent document extractor.

#     Given the following raw Redfin text, extract the following structured information:
    
#     1. Address – Full property address
#     2. Price – Sale price in USD
#     3. Bedrooms – Number of bedrooms
#     4. Bathrooms – Number of bathrooms
#     5. Size – Living area size in square feet
#     6. LotSize – Lot size in square feet (or specify units if different)
#     7. YearBuilt – Year the property was built
#     8. PropertyType – Type of property (e.g., Single Family Home, Condo)
#     9. GarageSpaces – Number of garage spaces (if specified)
#     10. Realtor – Listing agent name and agency
#     11. URL – Link to the Redfin listing (if provided)
#     12. HOA – HOA fee and description (if applicable)
#     13. ClimateFactors – Summary of local climate or environmental risks (e.g., flood zone, fire risk)
#     14. SchoolRatings – Ratings and names of nearby schools:
#         - PrimarySchool:  ("name": ..., "rating": ...)
#         - MiddleSchool:  ("name": ..., "rating": ...) 
#         - HighSchool: ("name": ..., "rating": ...) 
#     15. PricePerSqft – Calculate this as: `price / size`, rounded to 2 decimal places
#     16. Description – A brief, cleaned summary of the full listing description

#     Redfin Text crawl from website:
#     \"\"\"{text}\"\"\"                                          

#     Return your response as a JSON object with keys.
#     """)

#     messages = prompt_template.format_messages(text=text)
#     response = llm.invoke(messages)
        

#     # === Parse JSON output ===
#     try:
#         parsed_llm = json.loads(response.content)
#     except Exception as e:
#         print("⚠️ Failed to parse JSON from LLM. Saving raw output.")
#         parsed_llm = {
#             "Address": "",
#             "Price": None,
#             "Bedrooms": None,
#             "Bathrooms": None,
#             "Size": None,
#             "LotSize": None,
#             "YearBuilt": None,
#             "PropertyType": "",
#             "GarageSpaces": None,
#             "Realtor": "",
#             "URL": "",
#             "HOA": "",
#             "ClimateFactors": "",
#             "SchoolRatings": {
#                 "PrimarySchool": {"name": "", "rating": None},
#                 "MiddleSchool": {"name": "", "rating": None},
#                 "HighSchool": {"name": "", "rating": None}
#             },
#             "PricePerSqft": None,
#             "Description": "",
#             "LLM_raw": response.content
#         }

#     with open("extracted_info.json", "w") as f:
#         json.dump(parsed_llm, f, indent=2, ensure_ascii=False)

#     print("✅ Done! Saved to extracted_info.json")


# if __name__ == "__main__":
#     txt_llm()


import asyncio
import os
import json
import webbrowser
from PIL import Image
import pytesseract
from datetime import datetime   
from langchain.schema import Document
from newsapi import NewsApiClient
from crawl4ai import AsyncWebCrawler
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# === Load .env variables ===
load_dotenv()


def fetch_property_news(keyword: str, save_path: str = None):
    newsapi = NewsApiClient(api_key=os.environ["NEWSAPI_KEY"])

    # search for the articles
    articles = newsapi.get_everything(q=keyword, language='en', sort_by='relevancy', page_size=10)

    if articles.get("status") != "ok" or not articles.get("articles"):
        print(f"❌ No news found for '{keyword}'")
        print(articles)

    result = {
        "query": keyword,
        "articles": []
    }

    for article in articles.get("articles", []):
        result["articles"].append({
            "title": article["title"],
            "source": article["source"]["name"],
            "publishedAt": article["publishedAt"],
            "summary": article["description"],
            "url": article["url"]
        })

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"✅ News saved to {save_path}")

    return result


async def fetch_redfin_text(url: str, save_path: str):
    """Crawl the Redfin URL and save content as .txt"""
    # Ensure the folder exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(result.markdown)
        print(f"✅ Crawled and saved to {save_path}")

def extract_info_from_text(txt_path: str, output_json_path: str):
    """Load .txt and extract structured info with LLM"""
    # Load environment key
    os.environ["OPENAI_API_KEY"]

    # Load Redfin text
    loader = TextLoader(txt_path)
    docs = loader.load()
    text = docs[0].page_content

    # LLM setup
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Prompt Template
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

    # Run LLM
    messages = prompt_template.format_messages(text=text)
    response = llm.invoke(messages)

    try:
        parsed = json.loads(response.content)
    except Exception as e:
        print("⚠️ JSON parsing failed. Saving raw response.")
        parsed = {
            "LLM_raw": response.content
        }

    # Save result
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"✅ Extracted structured data saved to {output_json_path}")

# === Main Function ===
async def main():
    url = "https://www.redfin.com/CA/Redwood-City/561-Anchor-Cir-94065/home/1618613"
    txt_path = "data/redfin.txt"
    output_path = "data/extracted_info.json"
    news_path = "data/news_info.json"

    # await fetch_redfin_text(url, txt_path)
    # extract_info_from_text(txt_path, output_path)
    fetch_property_news("Redwood Shores properties", news_path)

if __name__ == "__main__":
    asyncio.run(main())
