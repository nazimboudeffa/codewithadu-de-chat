from flask import Flask, jsonify, render_template, request
from rag_posts import load_index, retrieve, format_results, DEFAULT_INDEX_PATH

app = Flask(__name__)

index_data = None


def get_index():
    global index_data
    if index_data is None:
        index_data = load_index(DEFAULT_INDEX_PATH)
    return index_data


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()
    top_k = int(data.get("top_k", 5))

    if not question:
        return jsonify({"error": "Question vide."}), 400

    try:
        idx = get_index()
    except Exception as exc:
        return jsonify({"error": f"Index introuvable : {exc}"}), 500

    results = retrieve(idx, question, top_k=top_k)
    if not results:
        return jsonify({"answer": "Aucun contexte pertinent trouvé.", "sources": []})

    sources = []
    for item in results:
        sources.append({
            "title": item.get("title") or "Sans titre",
            "date": item.get("iso_date") or "inconnue",
            "text": item.get("text", ""),
            "url": item.get("url"),
            "score": round(item.get("score", 0), 4),
        })

    return jsonify({
        "answer": format_results(results),
        "sources": sources,
    })


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
