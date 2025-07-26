import os
import fitz  # PyMuPDF
import json
from rank_bm25 import BM25Okapi
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(__file__)  # Current script directory
GLOBAL_OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(GLOBAL_OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    texts = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        texts.append((page_num + 1, page.get_text()))
    return texts

def score_pages(pages, query):
    tokenized_corpus = [page[1].lower().split() for page in pages]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(query.lower().split())
    return scores

def process_collection(collection_path, collection_name):
    pdf_dir = os.path.join(collection_path, "PDFs")
    input_json_path = os.path.join(collection_path, "challenge1b_input.json")

    if not os.path.exists(pdf_dir) or not os.path.exists(input_json_path):
        print(f"⚠️ Skipping {collection_name} due to missing PDFs or input JSON.")
        return

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona_val = input_data.get("persona", "Default Persona")
    persona = persona_val if isinstance(persona_val, str) else json.dumps(persona_val)

    job_val = input_data.get("job_to_be_done", "Extract key insights")
    job = job_val.strip() if isinstance(job_val, str) else json.dumps(job_val)

    output = {
        "metadata": {
            "input_documents": [],
            "persona": persona,
            "job_to_be_done": job,
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for file in os.listdir(pdf_dir):
        if not file.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(pdf_dir, file)
        output["metadata"]["input_documents"].append(file)

        pages = extract_text_from_pdf(file_path)
        scores = score_pages(pages, "insight extract summary persona based")

        if len(scores) == 0:
            continue

        max_index = scores.tolist().index(max(scores))
        best_page_num, best_text = pages[max_index]

        output["extracted_sections"].append({
            "document": file,
            "page_number": best_page_num,
            "section_title": "Auto-Extracted Insight",
            "importance_rank": 1
        })

        output["subsection_analysis"].append({
            "document": file,
            "refined_text": best_text.strip()[:1000],
            "page_number": best_page_num
        })

    output_path = os.path.join(GLOBAL_OUTPUT_DIR, f"{collection_name}_challenge2b_output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

def main():
    for folder in os.listdir(BASE_DIR):
        if folder.lower().startswith("collection"):
            collection_path = os.path.join(BASE_DIR, folder)
            if os.path.isdir(collection_path):
                print(f"🔍 Processing {folder}...")
                process_collection(collection_path, folder)
    print("✅ Done. All outputs saved to the central 'output/' folder.")

if __name__ == "__main__":
    main()
