from flask import Flask, jsonify, send_from_directory, request, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from pymongo import MongoClient
import os
from flask import jsonify
from bson import ObjectId

app = Flask(__name__, static_folder='frontend/build')
CORS(app)

   
app.secret_key = 'abcdef'

   
client = MongoClient('mongodb://localhost:29027/')
db = client['tmdb_db']     
movies_collection = db['movies']     
users_collection = db['users']       

   
@app.route('/')
def home():
    genre = request.args.get('genre', '')
    language = request.args.get('language', '')
    query = {}

    if genre:
        query['genres'] = genre
    if language:
        query['spoken_languages'] = language

    movies = list(movies_collection.find(query).limit(10))
    username = session.get('username')
    return render_template('index.html', movies=movies, username=username)


@app.route('/movie/<movie_id>')
def movie(movie_id):
       
    movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
    
    if movie is None:
        return "Movie not found", 404     
    
       
    movie['id'] = str(movie['_id'])     
    return render_template('movie_details.html', movie=movie)

   
@app.route('/analysis')
def analysis_redirect():
    return send_from_directory(app.static_folder, 'index.html')

   
@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

   
@app.route('/api/analysis')
def api_analysis():
       
    genre_revenue = list(movies_collection.aggregate([
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "totalRevenue": {"$sum": "$revenue"}}},
        {"$sort": {"totalRevenue": -1}}
    ]))

       
    average_genre_revenue = list(movies_collection.aggregate([
        {"$unwind": "$genres"},
        {"$group": {"_id": "$genres", "averageRevenue": {"$avg": "$revenue"}}},
        {"$sort": {"averageRevenue": -1}}
    ]))

       
    top_actors = list(movies_collection.aggregate([
        {"$unwind": "$cast"},
        {"$group": {"_id": "$cast.name", "totalRevenue": {"$sum": "$revenue"}}},
        {"$sort": {"totalRevenue": -1}},
        {"$limit": 10}
    ]))

       
    roi_data = list(movies_collection.aggregate([
        {"$match": {"budget": {"$gt": 0}, "revenue": {"$gt": 0}}}, 
        {"$project": {"title": 1, "budget": 1, "revenue": 1, "roi": {"$divide": ["$revenue", "$budget"]}}},
        {"$sort": {"roi": -1}},
        {"$limit": 10}
    ]))

       
    movies_per_year = list(movies_collection.aggregate([
        {"$match": {"release_date": {"$ne": "", "$exists": True}}},
        {"$addFields": {"releaseDateFormatted": {"$toDate": "$release_date"}}},
        {"$group": {"_id": {"year": {"$year": "$releaseDateFormatted"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id.year": -1}},
        {"$limit":30},
        
    ]))

       
    revenue_per_year = list(movies_collection.aggregate([
        {"$match": {"release_date": {"$ne": "", "$exists": True}}},
        {"$addFields": {"releaseDateFormatted": {"$toDate": "$release_date"}}},
        {"$group": {"_id": {"year": {"$year": "$releaseDateFormatted"}}, "totalRevenue": {"$sum": "$revenue"}}},
        {"$sort": {"_id.year": -1}},
        {"$limit":30}
    ]))

       
    def convert_object_id(data):
        if isinstance(data, list):
            return [convert_object_id(item) for item in data]
        elif isinstance(data, dict):
            return {k: convert_object_id(v) for k, v in data.items()}
        elif isinstance(data, ObjectId):
            return str(data)
        else:
            return data

       
    response_data = {
        "genreRevenue": convert_object_id(genre_revenue),
        "averageGenreRevenue": convert_object_id(average_genre_revenue),
        "topActors": convert_object_id(top_actors),
        "roiData": convert_object_id(roi_data),
        "moviesPerYear": convert_object_id(movies_per_year),
        "revenuePerYear": convert_object_id(revenue_per_year)
    }

       
    return jsonify(response_data)

   
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            flash('Username or Email already exists. Please choose another.')
            return redirect(url_for('signup'))

        users_collection.insert_one({'username': username, 'email': email, 'password': password})
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')

   
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

   
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

   
if __name__ == '__main__':
    app.run(debug=True, port=8000)
