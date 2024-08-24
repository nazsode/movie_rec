import streamlit as st
import openai
import asyncio

# OpenAI API anahtarınızı buraya yerleştirin
openai.api_key = 'API_KEYINIZI_BURAYA_YERLEŞTİRİN'

async def get_movie_recommendations_async(genres, favorite_movies):
    prompt = f"""
    I am creating a movie recommendation system. The user has selected the following genres: {', '.join(genres)}.
    The user's top 3 favorite movies are: {', '.join(favorite_movies)}.
    Based on these preferences, please recommend 5 movies. Format the response as a table with columns: Movie Name, Genre, and Summary.
    """

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",  # veya "gpt-4" modelini kullanabilirsiniz
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()

def get_movie_recommendations(genres, favorite_movies):
    return asyncio.run(get_movie_recommendations_async(genres, favorite_movies))

# Streamlit arayüzü
st.title("🎥 Film Öneri Sistemi")

# Kullanıcıdan türleri ve sevdiği filmleri seçmesini isteyin
genres = st.multiselect("Sevdiğiniz Türleri Seçin:", ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller'])
favorite_movies = [
    st.text_input(f"En Sevdiğiniz {i+1}. Film:", "") for i in range(3)
]

# Öneri butonu
if st.button("Öneri Al"):
    if genres and all(favorite_movies):
        recommendations = get_movie_recommendations(genres, favorite_movies)
        st.subheader("Film Önerileri")
        st.text(recommendations)
    else:
        st.error("Lütfen tüm alanları doldurun.")
