from flask import Flask, jsonify, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

CSV_PATH = "anime-standalone.csv"
PLACEHOLDER_IMAGE = "https://via.placeholder.com/300x450?text=No+Image"


def _find_column(df, candidates, required=True, default=None):
    for col in candidates:
        if col in df.columns:
            return col
    if required:
        raise ValueError(f"Missing required column. Expected one of: {candidates}")
    return default


def load_data(csv_path):
    df = pd.read_csv(csv_path)

    title_col = _find_column(df, ["title", "name", "anime_title"])
    genres_col = _find_column(df, ["genres", "genre"])
    image_col = _find_column(df, ["image_url", "image", "poster_url"], required=False)

    cleaned = pd.DataFrame(
        {
            "title": df[title_col].astype(str).fillna(""),
            "genres": df[genres_col].astype(str).fillna(""),
            "image_url": df[image_col].astype(str).fillna("") if image_col else "",
        }
    )

    cleaned = cleaned[cleaned["title"].str.strip() != ""].reset_index(drop=True)
    cleaned["genres"] = cleaned["genres"].fillna("").astype(str)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(cleaned["genres"])

    return cleaned, tfidf_matrix


df_anime, tfidf_matrix = load_data(CSV_PATH)
all_titles = sorted(df_anime["title"].dropna().astype(str).unique().tolist())


def get_recommendations(title, top_n=10):
    if not title:
        return [], "Vui long nhap ten anime."

    title_lower = title.strip().lower()
    if not title_lower:
        return [], "Vui long nhap ten anime."

    exact_matches = df_anime[df_anime["title"].str.lower() == title_lower]
    if exact_matches.empty:
        contains_matches = df_anime[df_anime["title"].str.lower().str.contains(title_lower, na=False)]
        if contains_matches.empty:
            return [], "Khong tim thay anime trong dataset."
        anime_index = contains_matches.index[0]
    else:
        anime_index = exact_matches.index[0]

    sim_scores = cosine_similarity(tfidf_matrix[anime_index], tfidf_matrix).flatten()
    similar_indices = sim_scores.argsort()[::-1]
    similar_indices = [idx for idx in similar_indices if idx != anime_index][:top_n]

    recs = []
    for idx in similar_indices:
        row = df_anime.iloc[idx]
        image_url = str(row.get("image_url", "")).strip()
        if not image_url or image_url.lower() == "nan":
            image_url = PLACEHOLDER_IMAGE

        recs.append(
            {
                "title": str(row.get("title", "")),
                "genres": str(row.get("genres", "")),
                "image_url": image_url,
            }
        )

    return recs, None


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

    recommendations, error = get_recommendations(title, top_n)
    if error:
        return jsonify({"error": error, "recommendations": []}), 404

    return jsonify({"recommendations": recommendations})


if __name__ == "__main__":
    app.run(debug=True)
