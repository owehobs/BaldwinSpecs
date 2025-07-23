import json
from flask import Flask, request, jsonify

app = Flask(__name__)

with open("FullBaldwin.json") as f:
    baldwin_data = json.load(f)

@app.route("/get-part", methods=["GET"])
def get_part():
    part_number = request.args.get("part")
    if not part_number:
        return jsonify({"error": "part parameter is required"}), 400

    part_number = part_number.strip().upper()
    part_info = baldwin_data.get(part_number)
    if not part_info:
        return jsonify({"error": f"Part {part_number} not found"}), 404

    return jsonify({part_number: part_info})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
