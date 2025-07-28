# 🔍 Challenge 1b: Multi-Collection PDF Analysis

## 🧠 Problem Statement

Develop a PDF processing pipeline that takes multiple document collections, analyzes them based on specific personas and task requirements, and outputs structured JSON data identifying the most relevant sections and content for each use case.

---

## 🚀 Solution Overview

This project automates PDF content extraction across multiple collections by:

1. Reading structured input JSONs describing the persona and job-to-be-done.
2. Parsing PDF files and extracting meaningful content.
3. Scoring and ranking sections by relevance.
4. Generating a consistent, schema-compliant output JSON per collection.

---

## 📁 Folder Structure

Challenge_1b/
├── Collection 1/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ └── challenge1b_output.json
├── Collection 2/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ └── challenge1b_output.json
├── Collection 3/
│ ├── PDFs/
│ ├── challenge1b_input.json
│ └── challenge1b_output.json
├── output/ # Contains final merged output
│ └── challenge2b.json
├── process.py # Main script to run
└── README.md

---

## 📥 Input Format (challenge1b_input.json)

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_001",
    "test_case_name": "recipe_case"
  },
  "documents": [
    { "filename": "sample.pdf", "title": "Vegetarian Recipes" }
  ],
  "persona": { "role": "Food Contractor" },
  "job_to_be_done": { "task": "Prepare vegetarian buffet-style dinner menu for corporate gathering" }
}
{
  "metadata": {
    "input_documents": ["sample.pdf"],
    "persona": "Food Contractor",
    "job_to_be_done": "Prepare vegetarian buffet-style dinner menu for corporate gathering"
  },
  "extracted_sections": [
    {
      "document": "sample.pdf",
      "section_title": "Main Course Ideas",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "sample.pdf",
      "refined_text": "Paneer butter masala, stuffed capsicum, dal makhani...",
      "page_number": 3
    }
  ]
}

## 🧑‍💼 Key Features

- 🧠 **Persona-Aware Parsing**: Uses the role and task for targeted content extraction.
- 🗂 **Multi-Collection Handling**: Independently processes each folder (collection).
- 📈 **Section Ranking**: Prioritizes sections using keyword/task relevance scoring.
- ⚙️ **Configurable Pipeline**: Easily scalable and adaptable to different personas or document types.

## 🛠 How to Run

Install dependencies:

```bash
pip install pdfplumber
python process.py
