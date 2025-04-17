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
            data.append(doc.to_dict())

        self.df = pd.DataFrame(data)

        # Preprocess text
        self.df['combined_features'] = (
            self.df['deskripsi'] + ' ' + self.df['kategori']
        )

        self.df['processed_text'] = self.df['combined_features'] \
            .apply(preprocess_text)

        # Initialize TF-IDF Vectorizer
        self.tfidf = TfidfVectorizer(max_features=5000)
        tfidf_matrix = self.tfidf.fit_transform(self.df['processed_text'])

        # Compute cosine similarity matrix
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(
        self, title: str, top_n: int = 5
    ) -> list[RecommendationResponse]:
        if self.df is None or self.cosine_sim is None:
            return []
        try:
            if 'namaInovasi' in self.df.columns:
                idx = self.df[self.df['namaInovasi'] == title].index[0]
            else:
                return []
        except IndexError:
            return []

        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n + 1]

        recommendations = []
        for i, score in sim_scores:
            rec = RecommendationResponse(
                inovasi=self.df.iloc[i]['namaInovasi'],
                kategori=self.df.iloc[i]['kategori'],
                deskripsi=self.df.iloc[i]['deskripsi'],
                similarity_score=round(score, 2),
            )
            recommendations.append(rec)

        return recommendations


recommendation_engine = RecommendationEngine()
