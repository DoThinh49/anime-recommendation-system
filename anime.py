import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PLACEHOLDER_IMAGE = "https://via.placeholder.com/300x450?text=No+Image"


class AnimeRecommender:
    def __init__(self, csv_path):
        self.df_anime, self.tfidf_matrix = self._load_data(csv_path)
        self.all_titles = sorted(self.df_anime["title"].dropna().astype(str).unique().tolist())

    @staticmethod
    def _find_column(df, candidates, required=True, default=None):
        for col in candidates:
            if col in df.columns:
                return col
        if required:
            raise ValueError(f"Missing required column. Expected one of: {candidates}")
        return default

    def _load_data(self, csv_path):
        df = pd.read_csv(csv_path)

        title_col = self._find_column(df, ["title", "name", "anime_title"])
        genres_col = self._find_column(df, ["genres", "genre"])
        image_col = self._find_column(df, ["image_url", "image", "poster_url"], required=False)

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

    def get_recommendations(self, title, top_n=10):
        if not title:
            return [], "Vui long nhap ten anime."

        title_lower = str(title).strip().lower()
        if not title_lower:
            return [], "Vui long nhap ten anime."

        exact_matches = self.df_anime[self.df_anime["title"].str.lower() == title_lower]
        if exact_matches.empty:
            contains_matches = self.df_anime[self.df_anime["title"].str.lower().str.contains(title_lower, na=False)]
            if contains_matches.empty:
                return [], "Khong tim thay anime trong dataset."
            anime_index = contains_matches.index[0]
        else:
            anime_index = exact_matches.index[0]

        sim_scores = cosine_similarity(self.tfidf_matrix[anime_index], self.tfidf_matrix).flatten()
        similar_indices = sim_scores.argsort()[::-1]
        similar_indices = [idx for idx in similar_indices if idx != anime_index][:top_n]

        recs = []
        for idx in similar_indices:
            row = self.df_anime.iloc[idx]
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
