import os
from PIL import Image
import pytesseract
from datetime import datetime
import json
import webbrowser   
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# === Load .env variables ===
load_dotenv()

def txt_llm():
    # === Load your OpenAI key (make sure it’s set) ===
    os.environ["OPENAI_API_KEY"]

    # === Load Redfin .txt file ===
    loader = TextLoader("/Users/yebingcong/code/ai_agent/data/example1/raw/redfin.txt")
    docs = loader.load()
    text = docs[0].page_content

    # === LLM setup ===
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # === Prompt Template ===
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
    response = llm.invoke(messages)
        

    # === Parse JSON output ===
    try:
        parsed_llm = json.loads(response.content)
    except Exception as e:
        print("⚠️ Failed to parse JSON from LLM. Saving raw output.")
        parsed_llm = {
            "Address": "",
            "Price": None,
            "Bedrooms": None,
            "Bathrooms": None,
            "Size": None,
            "LotSize": None,
            "YearBuilt": None,
            "PropertyType": "",
            "GarageSpaces": None,
            "Realtor": "",
            "URL": "",
            "HOA": "",
            "ClimateFactors": "",
            "SchoolRatings": {
                "PrimarySchool": {"name": "", "rating": None},
                "MiddleSchool": {"name": "", "rating": None},
                "HighSchool": {"name": "", "rating": None}
            },
            "PricePerSqft": None,
            "Description": "",
            "LLM_raw": response.content
        }

    with open("extracted_info.json", "w") as f:
        json.dump(parsed_llm, f, indent=2, ensure_ascii=False)

    print("✅ Done! Saved to extracted_info.json")


if __name__ == "__main__":
    txt_llm()