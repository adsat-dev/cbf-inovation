import pandas as pd
import numpy as np
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
        