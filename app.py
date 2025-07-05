import streamlit as st
import pandas as pd

# Import your backend functions
from recommender import get_similar_movies, get_movie_genres, top_n_movies_by_genre

# Load the cleaned data
df = pd.read_csv("cleaned_movie_data.csv")

# Optional: create a lowercase map for robust title search
title_map = {title.lower(): title for title in df['Title']}

st.set_page_config(page_title="CineMatch", layout="wide")
st.title("🎬 CineMatch – AI Movie Recommender")

st.markdown("Search by movie title to get plot-based recommendations.")

# Movie selection
movies_list = sorted(df['Title'].tolist())
selectvalue = st.selectbox("🎥 Choose a movie:", movies_list)

if st.button("🔁 Recommend Similar Movies"):
    # Get similar movies using your backend function
    similar_movies_df = get_similar_movies(selectvalue)
    
    if isinstance(similar_movies_df, str):
        st.error(similar_movies_df)
    else:
        st.subheader(f"🎯 Movies similar to *{selectvalue}*:")
        cols = st.columns(2)
        for i, (_, row) in enumerate(similar_movies_df.head(5).iterrows()):
            with cols[i % 2]:
                st.markdown(f"**{row['Title']}**")
                st.caption(f"⭐ Rating: {row.get('Rating', 'N/A')} | 📂 Genre(s): {row.get('clean_genres', 'N/A')}")
                st.write(row['Plot'][:300] + "...")

# Divider
st.markdown("---")
st.subheader("📂 Explore by Genre")

genre_input = st.text_input("Type a genre (e.g., sci-fi, thriller, romance):")

if genre_input:
    genre_movies_df = top_n_movies_by_genre(genre_input, n=5)
    if genre_movies_df.empty:
        st.warning("No movies found for that genre.")
    else:
        st.markdown(f"### Top-rated *{genre_input.title()}* Movies:")
        for _, row in genre_movies_df.iterrows():
            st.markdown(f"- **{row['Title']}** – ⭐ {row['Rating']}")

# Divider
st.markdown("---")
st.subheader("🔎 Check a Movie's Genre")

title_query = st.text_input("Enter a movie title to find its genre:")

if title_query:
    genre_result = get_movie_genres(title_query)
    if isinstance(genre_result, list):
        st.success(f"**Genres for {title_query.title()}**: {', '.join(genre_result)}")
    else:
        st.error(genre_result)
