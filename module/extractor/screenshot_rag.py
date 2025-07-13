import os
from PIL import Image
import pytesseract
from datetime import datetime
import json
from langchain.schema import Document
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# === Load .env variables ===
load_dotenv()

def main():
    # === Load Screenshot and Extract Text ===
    image = Image.open("./emoji-chat.png")
    ocr_text = pytesseract.image_to_string(image)

    # === Timestamp ===
    collected_time = datetime.now().isoformat()

    os.environ["OPENAI_API_KEY"]
    # === LLM Setup ===
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # === Prompt Template for Extraction ===
    prompt_template = ChatPromptTemplate.from_template("""
    You are an intelligent document extractor.

    Given the following raw OCR text, extract the following structured information:
    1. Datatext: Reconstruct the cleaned version of the full content
    2. Dataabstract: 1–2 sentence summary
    3. Subject: The main topic or theme
    4. Summary: Bullet-point summary
    5. Keywords: Relevant keywords
    6. attachedLink: any link if it appears in the content

    OCR Text:
    \"\"\"{ocr_text}\"\"\"

    Return your response as a JSON object with keys:
    Datatext, Dataabstract, Subject, Summary, Keywords, attachedLink.
    """)

    # === Send to LLM ===
    messages = prompt_template.format_messages(ocr_text=ocr_text)
    response = llm(messages)

    # === Attempt to Parse JSON from LLM Output ===
    try:
        parsed_llm = json.loads(response.content)
    except Exception as e:
        print("⚠️ Failed to parse JSON from LLM. Raw output will be saved.")
        parsed_llm = {
            "Datatext": "",
            "Dataabstract": "",
            "Subject": "",
            "Summary": "",
            "Keywords": [],
            "attachedLink": "",
            "LLM_raw": response.content
        }

    # === Combine Final Output ===
    final_output = {
        "OCRtext": ocr_text.strip(),
        "Datatext": parsed_llm.get("Datatext", ""),
        "Dataabstract": parsed_llm.get("Dataabstract", ""),
        "Subject": parsed_llm.get("Subject", ""),
        "Summary": parsed_llm.get("Summary", ""),
        "Keywords": parsed_llm.get("Keywords", []),
        "CollectedTime": collected_time,
        "dataCategory": "",
        "attachedLink": parsed_llm.get("attachedLink", "")
    }

    # === Save as JSON ===
    with open("extracted_info.json", "w") as f:
        json.dump(final_output, f, indent=2, ensure_ascii=False)

    print("✅ Done! Saved to extracted_info.json")

import bs4
from PIL import Image
import pytesseract
from datetime import datetime
from langchain.schema import Document
from langchain import hub
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# PDF/website

def PDF_llm():

    #### INDEXING ####

    # Load Documents
    # loader = WebBaseLoader(
    #     web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    #     bs_kwargs=dict(
    #         parse_only=bs4.SoupStrainer(
    #             class_=("post-content", "post-title", "post-header")
    #         )
    #     ),
    # )
    # docs = loader.load()
    import os
    os.environ["OPENAI_API_KEY"]
    os.environ["USER_AGENT"] = os.getenv("USER_AGENT", "my-app-name/1.0")


    from langchain_community.document_loaders import PyPDFLoader

    # Load Documents from PDF
    loader = PyPDFLoader("./2409.17140v2.pdf")
    docs = loader.load()


    # Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Embed
    vectorstore = Chroma.from_documents(documents=splits, 
                                        embedding=OpenAIEmbeddings())

    retriever = vectorstore.as_retriever()

    #### RETRIEVAL and GENERATION ####

    # Prompt
    prompt = hub.pull("rlm/rag-prompt")

    
    # LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Question
    answer = rag_chain.invoke("Can you help me to summarize this main idea of paper?")
    print(answer)

if __name__ == "__main__":
    main()
    # PDF_llm()

