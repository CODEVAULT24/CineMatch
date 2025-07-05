import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load cleaned data
df = pd.read_csv("cleaned_movie_data.csv")
df['Genres'] = df['Genres'].apply(eval)  # Convert stringified list back to list

# 1. Genre Lookup
def get_movie_genres(title, df=df):
    movie = df[df['Title'].str.lower() == title.lower()]
    if not movie.empty:
        return movie.iloc[0]['Genres']
    return "Movie not found."

# 2. Top-N by Genre
def top_n_movies_by_genre(genre, df=df, n=5):
    filtered = df[df['Genres'].apply(lambda genres: genre.lower() in [g.lower() for g in genres])]
    top_movies = filtered.sort_values(by='Rating', ascending=False).head(n)
    return top_movies[['Title', 'Rating']]

# 3. TF-IDF Similarity
def build_similarity_matrix(df=df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['Plot'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = build_similarity_matrix()

def get_similar_movies(title, df=df, cosine_sim=cosine_sim, top_n=5):
    try:
        idx = df[df['Title'].str.lower() == title.lower()].index[0]
    except IndexError:
        return "Movie not found."
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return df.iloc[movie_indices][['Title', 'Plot']]
