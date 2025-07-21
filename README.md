# Real Estate AI Agent

<p align="center">
  <img src="./doc/resource/icon.png" alt="icon" width="800"/>
</p>

# 🏡 Real Estate AI Agent — Your Smart Real Estate Consultant
Property Agent is an intelligent assistant that helps prospective homebuyers analyze residential properties comprehensively — from physical attributes and legal status to community trends, risk factors, and personal financial fit. This project leverages LLMs, RAG (Retrieval-Augmented Generation), and web scraping to build a research and recommendation engine for real estate.

<div align="center">

[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square)](#)
</div>

---

## 🚀 What is Real Estate AI Agent?

**Real Estate AI Agent** is a private, AI-powered platform that assists homebuyers in understanding a property from every angle — legal, physical, financial, and community-based. It leverages a Retrieval-Augmented Generation (RAG) pipeline, NewsAPI, and LLM summarization to provide comprehensive property intelligence.

---

## ✨ Key Features
### 🧱 Building & Legal Insights
- Extracts and summarizes key **building attributes** from platforms like Redfin.
- Reviews **title status** and **ownership history** for red flags.
- Visualizes trends from **past transactions**.

### 🌍 Community & Location Intelligence
- Aggregates community data:
  - Local news (via **NewsAPI**)
  - School ratings
  - Crime records
  - Commute patterns
  - Climate and environmental risks
  - Nearby air traffic (airplane route analysis)

### 🔍 RAG-Powered Document Understanding
- Implements a **chunking + embedding + reranking** architecture for high-quality retrieval.
- Users can upload **disclosures** and other documents for analysis.

### 📊 Comparative Market Analysis
- Analyzes similar homes within **1 mile radius**:
  - Similar lot size, bedroom count, and property age
- Uses **recent 5-year sales history** to compute growth trends

### 🎯 Personalized Recommendations
- Suggests properties based on individual **needs and preferences**
- Offers **financial suggestions** by analyzing uploaded income data
- Calculates **estimated price** and monthly affordability

---

## 🧠 Tech Stack

| Component         | Tech/Service                      |
|------------------|-----------------------------------|
| LLM               | OpenAI                            |
| Embedding         | Sentence Transformers             |
| Reranking         | BGE-Reranker                      |
| News Aggregation  | NewsAPI                           |
| Document Parsing  | PyMuPDF, pdfplumber               |
| Vector Store      | FAISS                             |
| Frontend (optional) | Streamlit / React              |

---

## 📂 Example Outputs

Examples of processed Redfin listings, community analysis tables, and disclosure summaries are available in the [`examples/`](./examples) folder.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- NewsAPI key
- FAISS, PyMuPDF, LangChain, Transformers, etc.

### Installation

```bash
git clone https://github.com/yourusername/ai_agent.git
cd ai_agent
pip install -r requirements.txt
```

### 🔧 Configure Your .env File
```env
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_key
```
### 🧪 How It Works
End-to-End RAG Flow
Crawl property listings (e.g., Redfin)

Chunk and embed property-related documents

Retrieve top-k relevant chunks based on user queries

Rerank using cross-encoder

Feed to LLM for answer generation

### 📈 Roadmap

- [x] Redfin crawler & data parser

- [x] LLM-based document summarization

- [x] RAG-based Q&A system

- [x] Disclosure analysis with file upload

- [ ] Frontend UI (Streamlit)

- [ ] Mortgage and interest calculator

- [ ] Zillow & Realtor.com integration

### 🤝 Contributing
We welcome contributions! To get started:

```bash
git clone https://github.com/yourusername/ai_agent.git
cd ai_agent
Open an issue or feature request
```
Fork this repo and create your feature branch

Commit your changes and push

Submit a Pull Request 🙌

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. For models, please check their respective licenses.


