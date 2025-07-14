# PDF Summarization Tool 📝📄

## 📌 About the Project
"""
📚 PDF Summarization Tool using LLMs (OpenRouter API)

Extracts and summarizes key research paper sections (title, abstract, methodology, results, etc.)
from PDFs using DeepSeek's open LLM via OpenRouter.

Outputs structured summaries in Excel format.
"""


## 🔥 Features
- **AI-powered extraction** of structured research paper summaries.
- **Automated data handling** with Pandas.
- **Saves results to Excel** for easy access.
- **API integration** with OpenRouter for NLP processing.

## 📂 Project Structure

│   README.md
│   requirements.txt
│
├───data
│       2017-Entrepreneurial intention and the effects of entrepreneurial education.pdf
│
├───output
│       summaries.xlsx
│       summaries2.xlsx
│       summaries_simpler_unparsed output.xlsx
│
└───scripts
    │   pdf_summarization_deepseek2.py
    │   pdf_summarization_tool.py
    │   test_api.py
    │
    └───output

## 🚀 Setup & Usage
### **1️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
2️⃣ Run the Tool
python scripts/pdf_summarization_deepseek2.py
3️⃣ Output Files
Summarized results: output/summaries_simpler.xlsx
Raw AI response: output/summaries_simpler_unparsed.xlsx
🔧 Dependencies
requests
fitz (PyMuPDF)
pandas
openpyxl
xlsxwriter
