import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load data
user_data = pd.read_csv('user_data.csv')
item_data = pd.read_csv('item_data.csv')

# Collaborative filtering
user_item_matrix = pd.pivot_table(user_data, values='rating', index=['user_id'], columns=['item_id'])
user_item_matrix.fillna(0, inplace=True)

def get_collab_score(user_id, item_id):
    user_row = user_item_matrix.loc[user_id].values.reshape(1, -1)
    item_col = user_item_matrix[item_id].values.reshape(-1, 1)
    return cosine_similarity(user_row, item_col)[0][0]

# Content-based filtering
tfidf = TfidfVectorizer(stop_words='english')
item_data['description'] = item_data['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(item_data['description'])
content_similarities = cosine_similarity(tfidf_matrix)

def get_content_score(item_id_1, item_id_2):
    idx_1 = item_data[item_data['item_id'] == item_id_1].index[0]
    idx_2 = item_data[item_data['item_id'] == item_id_2].index[0]
    return content_similarities[idx_1, idx_2]

# Hybrid model
def normalize(scores):
    max_score = np.max(scores)
    min_score = np.min(scores)
    return (scores - min_score) / (max_score - min_score)

def recommend_items(user_id, num_recommendations=10):
    user_items = user_data[user_data['user_id'] == user_id]['item_id']
    scores = []
    for item_id in item_data['item_id']:
        if item_id in user_items:
            score = 0
        else:
            collab_score = get_collab_score(user_id, item_id)
            content_score = get_content_score(item_id, item_id)
            hybrid_score = collab_score + content_score
            score = normalize(hybrid_score)
        scores.append(score)
    item_data['score'] = scores
    sorted_items = item_data.sort_values(by=['score'], ascending=False)[:num_recommendations]
    return sorted_items['item_id'].tolist()

# Example usage
recommendations = recommend_items(user_id=123, num_recommendations=10)
print(recommendations)
