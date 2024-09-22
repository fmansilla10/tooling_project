# Interactive Movie Recommendation System

This project is an **Interactive Movie Recommendation System** built using **Streamlit**, which allows users to visualize movie data, explore user similarities, and get movie recommendations based on user input. The system uses the MovieLens dataset and offers several dynamic visualizations, including heatmaps, scatter plots, and bar charts.

The project has been **containerized using Docker**, making it easy to deploy in any environment. It includes proper documentation for setting up, running, and exploring the app.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [How to Use the App](#how-to-use-the-app)
- [Containerization with Docker](#containerization-with-docker)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [References](#references)

---

## Project Overview

The **Interactive Movie Recommendation System** allows users to explore the MovieLens dataset, discover patterns in movie ratings, and receive personalized movie recommendations. The system utilizes **cosine similarity** to recommend movies to users based on their ratings and the ratings of similar users.

Users can:
- Filter movies by genre and year.
- Visualize the most popular movies.
- Explore user similarity through a heatmap.
- View movie rating patterns via scatter plots.

The project also showcases a personalized recommendation system that suggests movies based on user ratings and selected similarity thresholds.

## Features

- **Movie Recommendation**: Suggest movies to users based on cosine similarity and minimum rating thresholds.
- **Interactive Filtering**: Filter movies based on genres and release year range.
- **Popular Movies Bar Chart**: Visualize the top 10 most-rated movies.
- **User Similarity Heatmap**: Explore user similarity using a heatmap.
- **Movie Rating Scatter Plot**: See the relationship between movie release year and average rating.
- **Dynamic Controls**: Adjust the minimum number of ratings and similarity scores via sliders.

## Installation and Setup

### Prerequisites

- Python 3.9 or higher
- Docker (optional, if running with Docker)

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/streamlit_project.git
cd streamlit_project
```
### Step 2: Set Up a Virtual Environment
It's recommended to set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 4: Place Dataset Files
Ensure the following files are in the root directory:

- `movies.csv`
- `ratings.csv`

You can download these from the [MovieLens website](https://grouplens.org/datasets/movielens/).

### Step 5: Run the App Locally
To start the Streamlit app, run the following command:

```bash
streamlit run project_tooling.py
```

Open your browser and navigate to [http://localhost:8501](http://localhost:8501) to view the app.

---

### How to Use the App

#### Sidebar Settings

The sidebar allows users to filter the recommendations and visualizations dynamically:

- **Minimum Number of Ratings**: Select the minimum number of ratings for recommendations.
- **Minimum Similarity Score**: Adjust the similarity score threshold for user similarity calculations.
- **Genre Filter**: Filter movies based on genres.
- **Year Filter**: Set a range for the release year of movies.

### Popular Movies

The app displays the top 10 most-rated movies in the dataset, visualized as a bar chart. This gives users an overview of popular movies in the dataset.

### User Similarity Heatmap

The app includes a heatmap showing user similarities based on cosine similarity, allowing users to explore how similar their ratings are to other users.

### Scatter Plot of Movies

The scatter plot displays the relationship between movie release years and their average ratings. You can filter the movies by genres and year using the sidebar controls.

### Personalized Recommendations

Enter a **User ID** in the input box to receive personalized movie recommendations based on user similarity. The system will compare the entered user ID with similar users and recommend movies that meet the similarity and rating thresholds.

---

### Containerization with Docker

The app has been containerized using Docker to ensure it runs consistently across different environments.

#### Step-by-Step Guide to Running the App with Docker

##### Step 1: Build the Docker Image

First, make sure you're in the root of the project directory, then build the Docker image:

```bash
docker build -t streamlit-app .
```

##### Step 2: Run the Docker Container

Once the image is built, you can run it with the following command:

```bash
docker run -p 8501:8501 streamlit-app
```

##### Step 3: Stop the Container

To stop the container, use the following command:

```bash
docker stop [container_id]
```

---

### Project Structure

```bash
streamlit_project/
│
├── project_tooling.py        # Main Streamlit application
├── Dockerfile                # Docker configuration file
├── requirements.txt          # Python dependencies
├── movies.csv                # MovieLens movies dataset
├── ratings.csv               # MovieLens ratings dataset
├── README.md                 # Project documentation
```

---

### Future Improvements

- Add more complex recommendation algorithms such as **collaborative filtering**.
- Include more user interactivity with advanced filters and visualizations.
- Implement a user registration system to allow personalized movie preferences.

---

### References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)


