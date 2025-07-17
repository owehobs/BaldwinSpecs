import os
import requests
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader

app = Flask(__name__)
PDF_PATH = "BaldwinFilterGuide.pdf"
PDF_URL = "https://drive.google.com/uc?export=download&id=1rFoOY6VKY5Ret3CWDxt1kgV0LS5_xn1Q"  # You'll host this somewhere

# Download the PDF once if not cached
if not os.path.exists(PDF_PATH):
    print("Downloading Baldwin PDF...")
    r = requests.get(PDF_URL)
    with open(PDF_PATH, "wb") as f:
        f.write(r.content)

@app.route("/get-pdf-text", methods=["GET"])
def get_pdf_text():
    part_number = request.args.get("part")
    if not part_number:
        return jsonify({"error": "part parameter is required"}), 400

    reader = PdfReader(PDF_PATH)
    matches = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if part_number in text:
            matches.append(i)

    if not matches:
        return jsonify({"error": f"{part_number} not found"}), 404

    start = max(0, matches[0] - 1)
    end = min(len(reader.pages), matches[0] + 2)

    excerpt = "\n".join(reader.pages[i].extract_text() for i in range(start, end))

    return jsonify({"partSpecText": excerpt.strip()})
