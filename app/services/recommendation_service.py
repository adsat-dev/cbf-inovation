import pandas as pd
# import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..config.firebase_config import db
from ..utils.text_processing import preprocess_text
from ..models.recommendation import RecommendationResponse


class RecommendationEngine:
    def __init__(self):
        self.df = None
        self.tfidf = None
        self.cosine_sim = None
        self.initialize_model()

    def initialize_model(self):
        innovations_ref = db.collection('innovations')
        docs = innovations_ref.stream()

        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data["id"] = doc.id
            data.append(doc_data)

        self.df = pd.DataFrame(data)

        # Preprocess text
        self.df['combined_features'] = (
            self.df['deskripsi'] + ' ' + self.df['kategori']
        )

        self.df['processed_text'] = self.df['combined_features'] \
            .apply(preprocess_text)

        # Initialize TF-IDF Vectorizer
        self.tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.9)
        tfidf_matrix = self.tfidf.fit_transform(self.df['processed_text'])

        # Compute cosine similarity matrix
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(
        self, innovation_id: str, top_n: int = 5
    ) -> list[RecommendationResponse]:
        if self.df is None or self.cosine_sim is None:
            return []
        try:
            idx = self.df[self.df['id'] == innovation_id].index[0]
        except IndexError:
            return []

        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n + 1]

        recommendations = []
        try:
            for i, score in sim_scores:
                row = self.df.iloc[i]
                # 1. Images: default [] jika nan atau tidak ada
                raw_images = row.get("images", [])
                if isinstance(raw_images, float) and pd.isna(raw_images):
                    images: list[str] = []
                else:
                    images = raw_images if isinstance(raw_images, list) else []

                # 2. Tahun dibuat: default None jika nan atau tidak ada, else cast ke str
                raw_year = row.get("tahunDibuat", None)
                if isinstance(raw_year, float) and pd.isna(raw_year):
                    tahun = None
                else:
                    tahun = str(raw_year) if raw_year is not None else None
                rec = RecommendationResponse(
                    id=row["id"],
                    inovasi=row["namaInovasi"],
                    kategori=row["kategori"],
                    deskripsi=row["deskripsi"],
                    namaInnovator=row["namaInnovator"],
                    images=images,
                    tahunDibuat=tahun,
                    similarity_score=round(score, 2),
                )
                recommendations.append(rec)
        except KeyError as e:
            print(f"Error processing recommendation: {str(e)}")
            return []
        return recommendations


recommendation_engine = RecommendationEngine()
