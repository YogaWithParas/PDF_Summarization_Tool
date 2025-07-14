import os
from pathlib import Path
import fitz  # PyMuPDF for PDF text extraction
import pandas as pd
import requests
import time
import re
from dotenv import load_dotenv

# **Load API Key from .env File**
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FOLDER = BASE_DIR / "data"
OUTPUT_PATH = BASE_DIR / "output" / "summaries.xlsx"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"

# **Extract Text from PDF**
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join([page.get_text("text") for page in doc])

# **Get AI Response**
def get_ai_response(text, max_retries=3):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    prompt = f"""
    Extract and summarize the following sections from the research paper:
    - Title
    - Abstract
    - Introduction
    - Methodology
    - Results
    - Conclusion
    - Methodology Used
    - Hypothesis Tested
    - Literature Review
    - Limitations
    - Keywords
    - Type of Study
    - Country/Region
    - Sample Size & Population
    - Entrepreneurial Intention Model Used
    - Key Findings
    - Relevance to Our Research

    Provide a **clean, structured response** in simple text format.

    **Research Paper Text**:
    {text[:10000]}  # Limiting input to avoid API overflow
    """

    data = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}]}

    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Raise error if request fails

            ai_response = response.json()["choices"][0]["message"]["content"].strip()
            
            print(f"\n🔍 AI Response:\n{ai_response[:500]}...\n")  # Print first 500 chars
            return ai_response  

        except requests.exceptions.RequestException as e:
            print(f"⚠️ API Error on attempt {attempt+1}: {e}")
            time.sleep(5)

    return "❌ Error in AI response"

# **Extract Structured Sections Using Regex**
def parse_ai_response(ai_response):
    fields = {
        "Title", "Abstract", "Introduction", "Methodology", "Results", "Conclusion",
        "Methodology Used", "Hypothesis Tested", "Literature Review", "Limitations",
        "Keywords", "Type of Study", "Country/Region", "Sample Size & Population",
        "Entrepreneurial Intention Model Used", "Key Findings", "Relevance to Our Research"
    }

    structured_data = {field: "Not Available" for field in fields}
    structured_data["Summary"] = ai_response
    structured_data["File Name"] = ""

    if not isinstance(ai_response, str) or len(ai_response.strip()) < 50:
        return structured_data  # Skip bad/empty summaries

    # Match markdown-like headings with variations: **Title**, ### Title, #### Abstract
    pattern = re.compile(r"(?:\*\*|#{2,4})\s*(.+?)\s*(?:\*\*|:)?\n", re.IGNORECASE)
    splits = pattern.split(ai_response)

    for i in range(1, len(splits), 2):
        key = splits[i].strip().lower().replace(":", "")
        value = splits[i + 1].strip() if i + 1 < len(splits) else ""

        # Match fuzzy keys to correct field names
        for field in fields:
            if key in field.lower() or field.lower() in key:
                structured_data[field] = value
                break

    return structured_data

# **Process PDFs**
def process_pdfs(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
    data = []

    for file in pdf_files:
        print(f"📄 Processing: {file}")
        text = extract_text_from_pdf(file)
        ai_response = get_ai_response(text)

        # **Store both parsed data & full AI response**
        parsed_data = parse_ai_response(ai_response)
        parsed_data["File Name"] = os.path.basename(file)  
        data.append(parsed_data)

    return data

# **Main Function**
def main():
    extracted_data = process_pdfs(DATA_FOLDER)

    # **Convert Data to DataFrame**
    df = pd.DataFrame(extracted_data)

    # **Save Data to Excel**
    df.to_excel(OUTPUT_PATH, index=False, engine="xlsxwriter")

    print(f"\n✅ Processing completed! Data saved to {OUTPUT_PATH}")

# **Run the script**
if __name__ == "__main__":
    main()