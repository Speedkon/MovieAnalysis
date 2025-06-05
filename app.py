import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🎬 Movie Rating Analysis and Genre Comparison")

API_KEY = "bff0848e79a71a719886e08586df4a8c"  

@st.cache_data
def get_genre_mapping():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    genres = response.json()["genres"]
    return {genre["id"]: genre["name"] for genre in genres}

@st.cache_data
def get_movies(pages=5):
    movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        response = requests.get(url)
        data = response.json()
        for movie in data.get("results", []):
            movie["genre_ids"] = list(set(movie.get("genre_ids", [])))  
            movies.append(movie)
    return movies

genre_dict = get_genre_mapping()
movies = get_movies()
df = pd.DataFrame(movies)

df["genres"] = df["genre_ids"].apply(lambda ids: ", ".join([genre_dict.get(i, "Unknown") for i in ids]))
df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df.dropna(subset=["release_year", "vote_average", "vote_count"])
df = df.astype({"release_year": "int", "vote_average": "float", "vote_count": "int"})

st.sidebar.header("🔎 Filters")
years = sorted(df["release_year"].unique())
selected_year = st.sidebar.slider("Select year range", int(min(years)), int(max(years)), (int(min(years)), int(max(years))))

all_genres = sorted(set(g for genre_list in df["genres"].str.split(", ") for g in genre_list))

select_all = st.sidebar.checkbox("Select all genres", value=True)

if select_all:
    selected_genres = all_genres
else:
    selected_genres = st.sidebar.multiselect("Select genres", all_genres, default=all_genres[:3]) 

min_rating = st.sidebar.slider("Minimum movie rating for Top 5", 0.0, 10.0, 7.0, 0.1)

filtered_df = df[
    (df["release_year"] >= selected_year[0]) &
    (df["release_year"] <= selected_year[1]) &
    (df["genres"].apply(lambda g: any(genre in g for genre in selected_genres)))
]

genre_ratings = []
for genre in all_genres:
    genre_movies = df[df["genres"].str.contains(genre)]
    if not genre_movies.empty:
        genre_ratings.append({"genre": genre, "avg_rating": genre_movies["vote_average"].mean()})
genre_df = pd.DataFrame(genre_ratings).sort_values(by="avg_rating", ascending=False)

with st.expander("📊 Average Rating by Genre"):
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=genre_df, x="genre", y="avg_rating", ax=ax1, palette="coolwarm")
    ax1.set_title("Average Rating by Genre")
    ax1.set_xlabel("Genre")
    ax1.set_ylabel("Average Rating")
    plt.xticks(rotation=45)
    st.pyplot(fig1, use_container_width=True)

with st.expander("📈 Average Rating Over Time"):
    year_avg = filtered_df.groupby("release_year")["vote_average"].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=year_avg, x="release_year", y="vote_average", marker="o", ax=ax2)
    ax2.set_title("Average Rating by Release Year")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Average Rating")
    st.pyplot(fig2, use_container_width=True)

with st.expander("📉 Impact of Vote Count on Rating"):
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=filtered_df, x="vote_count", y="vote_average", alpha=0.6, ax=ax3)
    ax3.set_title("Impact of Vote Count on Rating")
    ax3.set_xlabel("Vote Count")
    ax3.set_ylabel("Rating")
    st.pyplot(fig3, use_container_width=True)

st.subheader("🎥 Top 5 Movies")

top_movies = filtered_df[filtered_df["vote_average"] >= min_rating].sort_values(by="vote_average", ascending=False).drop_duplicates(subset=["title"]).head(5)

cols = st.columns(len(top_movies))
for col, (_, movie) in zip(cols, top_movies.iterrows()):
    with col:
        st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", use_container_width=True)
        st.markdown(f"**{movie['title']}**")
        st.markdown(f"⭐ Rating: {movie['vote_average']}")
        st.markdown(f"📆 Year: {movie['release_year']}")
        st.markdown(f"🎭 Genres: {movie['genres']}")
