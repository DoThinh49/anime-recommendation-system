from flask import Flask, jsonify, render_template, request
from anime import AnimeRecommender

app = Flask(__name__)

CSV_PATH = "anime-standalone.csv"
recommender = AnimeRecommender(CSV_PATH)
all_titles = recommender.all_titles


@app.route("/")
def index():
    return render_template("index.html", anime_titles=all_titles)


@app.route("/recommend", methods=["POST"])
def recommend():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "")

    try:
        top_n = int(payload.get("top_n", 10))
    except (TypeError, ValueError):
        top_n = 10

    top_n = max(1, min(top_n, 50))

    recommendations, error = recommender.get_recommendations(title, top_n)
    if error:
        return jsonify({"error": error, "recommendations": []}), 404

    return jsonify({"recommendations": recommendations})


if __name__ == "__main__":
    app.run(debug=True)
