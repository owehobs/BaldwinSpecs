from flask import Flask, request, jsonify
from PyPDF2 import PdfReader

app = Flask(__name__)
PDF_PATH = "BaldwinFilterGuide.pdf"

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

    # Extract 1 page before and after the first match (3-page window)
    start = max(0, matches[0] - 1)
    end = min(len(reader.pages), matches[0] + 2)

    excerpt = "\n".join(reader.pages[i].extract_text() for i in range(start, end))

    return jsonify({"partSpecText": excerpt.strip()})
