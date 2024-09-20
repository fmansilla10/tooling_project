import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.impute import SimpleImputer

# Update the file path to where the movies.csv and ratings.csv files are stored on your local system
movies_file_path = "/app/movies.csv"
ratings_file_path = "/app/ratings.csv"

# Load the MovieLens dataset
movies_df = pd.read_csv(movies_file_path)
ratings_df = pd.read_csv(ratings_file_path)

# Extract year from title if it's embedded (e.g., "Toy Story (1995)")
movies_df["year"] = movies_df["title"].apply(
    lambda x: (
        re.search(r"\((\d{4})\)", x).group(1) if re.search(r"\((\d{4})\)", x) else None
    )
)
movies_df["year"] = pd.to_numeric(
    movies_df["year"], errors="coerce"
)  # Convert extracted year to numeric

# Sidebar for app configuration
st.sidebar.header("Movie Recommendation Settings")
min_ratings = st.sidebar.slider("Minimum Number of Ratings", 1, 100, 10)
min_similarity = st.sidebar.slider("Minimum Similarity Score", 0.0, 1.0, 0.5)

# Movie Filters
genre_filter = st.sidebar.multiselect(
    "Select Genres", options=movies_df["genres"].unique()
)
year_filter = st.sidebar.slider(
    "Select Release Year Range",
    int(movies_df["year"].min()),
    int(movies_df["year"].max()),
    (1980, 2020),
)

# Create a pivot table to represent user-item ratings
ratings_matrix = ratings_df.pivot_table(
    index="userId", columns="movieId", values="rating"
)

# Handle missing values (e.g., impute with mean)
imputer = SimpleImputer(strategy="mean")
ratings_matrix = imputer.fit_transform(ratings_matrix)

# Apply filters for genre and year dynamically
filtered_movies = movies_df.copy()
if genre_filter:
    filtered_movies = filtered_movies[
        filtered_movies["genres"].str.contains("|".join(genre_filter))
    ]
filtered_movies = filtered_movies[
    (filtered_movies["year"] >= year_filter[0])
    & (filtered_movies["year"] <= year_filter[1])
]

# Update the ratings matrix based on the filtered movies
filtered_ratings_df = ratings_df[ratings_df["movieId"].isin(filtered_movies["movieId"])]
filtered_ratings_matrix = filtered_ratings_df.pivot_table(
    index="userId", columns="movieId", values="rating"
)

# Impute missing values for the filtered ratings matrix
filtered_ratings_matrix = imputer.fit_transform(filtered_ratings_matrix)

# Calculate cosine similarity between users based on the filtered matrix
filtered_cosine_sim = cosine_similarity(filtered_ratings_matrix)


# Function to recommend movies based on user ratings and filters
def recommend_movies(user_id):
    # Convert user_id to an integer index
    try:
        user_id = int(user_id)
    except ValueError:
        st.error(f"Invalid user ID: {user_id}. Please enter a valid integer.")
        return []

    # Get the similarity scores for the user
    user_similarity = filtered_cosine_sim[user_id]

    # Sort the users by similarity (highest first)
    similar_users = user_similarity.argsort()[::-1]

    # Create an empty DataFrame to hold the recommendations
    movie_recommendations = pd.DataFrame()

    # Loop through similar users and get their ratings
    for similar_user in similar_users[1:]:
        # Check if the similarity score meets the min_similarity threshold
        if user_similarity[similar_user] < min_similarity:
            break
        similar_user_ratings = filtered_ratings_df[
            filtered_ratings_df["userId"] == similar_user
        ]
        movie_recommendations = pd.concat([movie_recommendations, similar_user_ratings])

        # Limit to a few users to avoid too many recommendations
        if len(movie_recommendations) >= min_ratings:
            break

    # Return the movie titles of the recommendations
    movie_ids = movie_recommendations["movieId"].unique()
    recommended_movies = movies_df[movies_df["movieId"].isin(movie_ids)]

    return recommended_movies["title"].tolist()


# Function to visualize popular movies with filters
def plot_popular_movies():
    movie_counts = filtered_ratings_df["movieId"].value_counts().nlargest(10)
    popular_movies = movies_df[movies_df["movieId"].isin(movie_counts.index)]
    popular_movies["rating_count"] = movie_counts.values

    st.write("### Most Popular Movies")
    fig = px.bar(
        popular_movies,
        x="rating_count",
        y="title",
        orientation="h",
        title="Top 10 Most Rated Movies",
    )
    st.plotly_chart(fig)


# Function to visualize user similarity as a heatmap
def plot_user_similarity():
    st.write("### User Similarity Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        filtered_cosine_sim[:50, :50], cmap="coolwarm", ax=ax
    )  # Plot for first 50 users
    st.pyplot(fig)


# Function to create a scatter plot of movies based on average rating and year
def plot_scatter_plot():
    # Calculate average rating for each movie
    avg_ratings = filtered_ratings_df.groupby("movieId")["rating"].mean().reset_index()
    avg_ratings = avg_ratings.rename(columns={"rating": "average_rating"})

    # Merge with movie data
    movie_ratings = pd.merge(avg_ratings, movies_df, on="movieId")

    # Apply the genre and year filters
    movie_ratings = movie_ratings[
        (movie_ratings["year"] >= year_filter[0])
        & (movie_ratings["year"] <= year_filter[1])
    ]

    # Plot scatter plot (average rating vs. year)
    st.write("### Scatter Plot: Average Rating vs. Release Year")
    fig = px.scatter(
        movie_ratings,
        x="year",
        y="average_rating",
        hover_name="title",
        title="Movies by Average Rating and Release Year",
        labels={"year": "Release Year", "average_rating": "Average Rating"},
    )
    st.plotly_chart(fig)


# Streamlit app
st.title("Interactive Movie Recommendation System")

# Display Popular Movies Bar Chart
plot_popular_movies()

# Display User Similarity Heatmap
plot_user_similarity()

# Display Scatter Plot for Average Rating vs. Year
plot_scatter_plot()

# User input
user_id = st.number_input("Enter your user ID", min_value=0, step=1)

# Recommend movies and display
if user_id:
    recommendations = recommend_movies(user_id)
    if recommendations:
        st.write("### Recommended Movies:")
        for movie in recommendations:
            st.write(movie)
    else:
        st.write("No recommendations found.")
