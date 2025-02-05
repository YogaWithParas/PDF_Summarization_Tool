import os
import fitz  # PyMuPDF for PDF text extraction
import pandas as pd
import requests
import time
import re
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# **Constants**
DATA_FOLDER = r"C:\Users\prate\OneDrive\Desktop\Pyhton Projects\PDF_Summarization_Tool\data"
OUTPUT_PATH = r"C:\Users\prate\OneDrive\Desktop\Pyhton Projects\PDF_Summarization_Tool\output\summaries_simpler.xlsx"

API_KEY = os.getenv("API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-distill-llama-70b:free"

# **Function to extract text from PDF**
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

# **Function to get AI response**
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
    """
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt + text}],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    for attempt in range(max_retries):
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Attempt {attempt + 1} failed: {response.status_code} - {response.text}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Failed to get AI response after multiple attempts")

# **Main function**
def main():
    summaries = []
    
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_FOLDER, filename)
            print(f"Processing: {filename}")
            
            text = extract_text_from_pdf(pdf_path)
            try:
                summary = get_ai_response(text)
                summaries.append({"File Name": filename, "Summary": summary})
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    df = pd.DataFrame(summaries)
    df.to_excel(OUTPUT_PATH, index=False)
    print(f"Processing completed! Data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()