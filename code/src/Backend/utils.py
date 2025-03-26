from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

duplicate_store = []

def detect_duplicate(text, threshold=0.9):
    """Detect duplicates using TF-IDF"""
    global duplicate_store
    if not duplicate_store:
        duplicate_store.append(text)
        return False
    vectorizer = TfidfVectorizer().fit_transform([text] + duplicate_store)
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:])[0]
    is_duplicate = any(score > threshold for score in similarity)
    if not is_duplicate:
        duplicate_store.append(text)
    return is_duplicate