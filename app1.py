from flask import Flask, render_template, request
import pymongo  # Assuming MongoDB for your Movie Analysis App
from bson.objectid import ObjectId 

app = Flask(__name__)

# MongoDB connection (assuming MongoDB)
client = pymongo.MongoClient('mongodb://localhost:29027/')
db = client['tmdb_db']
movies_collection = db['movies']

@app.route('/')
def home():
    # Retrieve movie data from MongoDB (example query)
    movies = list(movies_collection.find().limit(7))
    return render_template('index.html', movies=movies)  # Pass movies to the template

@app.route('/movie')
def movie_details():
    try:
        # Retrieve specific movie details by ID from MongoDB
        movie = movies_collection.find_one({'_id': ObjectId('670bf4bf9e6cd6bc8aae84c9')})
        if movie:
            return render_template('movie_details.html', movie=movie)
        else:
            return "Movie not found", 404
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return "An error occurred", 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
