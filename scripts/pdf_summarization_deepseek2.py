import os
import fitz  # PyMuPDF for PDF text extraction
import pandas as pd
import requests
import time
import re

# **Constants**
DATA_FOLDER = r"C:\Users\prate\OneDrive\Desktop\Pyhton Projects\PDF_Summarization_Tool\data"
OUTPUT_PATH = r"C:\Users\prate\OneDrive\Desktop\Pyhton Projects\PDF_Summarization_Tool\output\summaries_simpler.xlsx"

API_KEY = "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"
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
    - Conclusion
    - Methodology Used (qualitative, quantitative, mixed-methods)
    - Hypothesis Tested
    - Literature Review
    - Limitations
    - Keywords (one line)
    - Type of Study (one line)
    - Country/Region (one line)
    - Sample Size & Population (one line)
    - Entrepreneurial Intention Model Used (one line)
    - Key Findings (one line)
    - Relevance to Our Research (one line)

    Provide a **clean, structured response** in simple text format.

    **Research Paper Text**:
    {text[:10000]}  # Limiting input to prevent API issues
    """
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # Raise error if request fails

            ai_response = response.json()["choices"][0]["message"]["content"].strip()
            
            print(f"\n🔍 AI Response:\n{ai_response}\n")  # Print full AI response
            return ai_response  # Return plain text response

        except requests.exceptions.RequestException as e:
            print(f"⚠️ API Error on attempt {attempt+1}: {e}")
            time.sleep(5)  # Wait before retrying
    
    return "❌ Error in AI response"

# **Function to parse AI response into structured data**
def parse_ai_response(ai_response):
    structured_data = {"File Name": "", "AI Raw Response": ai_response}  # Store raw AI response
    expected_fields = [
        "Title", "Abstract", "Introduction", "Methodology", "Conclusion", "Methodology Used",
        "Hypothesis Tested", "Literature Review", "Limitations", "Keywords", "Type of Study", 
        "Country/Region", "Sample Size & Population", "Entrepreneurial Intention Model Used",
        "Key Findings", "Relevance to Our Research"
    ]
    
    # **Regex Pattern to Detect Headers (e.g., "**Title**")**
    pattern = re.compile(r"\*\*(.*?)\*\*")  # Looks for text between ** **
    
    # **Split AI response into sections**
    sections = pattern.split(ai_response)
    
    current_field = None

    for section in sections:
        section = section.strip()

        # If the section matches an expected field, store its name
        if section in expected_fields:
            current_field = section
            structured_data[current_field] = ""
        elif current_field:
            # Append text to the current field
            structured_data[current_field] += section + " "

    # Ensure all fields are present
    for field in expected_fields:
        structured_data.setdefault(field, "Not Available")

    return structured_data

# **Function to process all PDFs**
def process_pdfs(folder_path):
    pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
    data = []

    for file in pdf_files:
        print(f"📄 Processing: {file}")
        text = extract_text_from_pdf(file)
        ai_response = get_ai_response(text)

        # **Parse AI response into structured data**
        parsed_data = parse_ai_response(ai_response)
        parsed_data["File Name"] = os.path.basename(file)  # Add file name

        # **Store structured data**
        data.append(parsed_data)

    return data

# **Main function**
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
