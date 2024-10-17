# Movie Analysis Website

Our project is movie data analysis using Flask, MongoDB, and ReactJS. It provides insights such as revenue by genre, top actors, and ROI (return on investment) for movies. The MongoDB database is sharded into three shards based on release date to ensure scalability.

## Features

- **Movie Data Query**: Filter movies by genre and language.
- **Detailed Movie Information**: View movie details like title, cast, genres, etc.
- **Data Analysis**:
  - Total revenue and average revenue per genre.
  - Top actors by total revenue.
  - Movies with the highest ROI.
  - Movies and revenue per year.
- **User Management**: Signup, login, and logout features.
- **Frontend**: Built with ReactJS, HTML, and CSS.

## Prerequisites

1. **Python 3.x**: Ensure you have Python installed.
2. **MongoDB**: MongoDB should be installed and sharded into three shards.
3. **Node.js and npm**: For managing the ReactJS frontend.
4. **Flask and MongoDB libraries**: Install necessary Python packages using `pip`.
   ```bash
   pip install Flask pymongo Flask-Cors
## MongoDB Sharding

The MongoDB database is sharded based on movie release dates. Ensure you have three shards configured and running.

## Setup Instructions

### 1. Backend (Flask)

- Clone the repository:
  ```bash
  git clone https://github.com/Kamesh54/ADS.git
  cd ADS
  ```
* Install the required dependencies

```bash
pip install -r requirements.txt
```

* Start the Flask server:

```bash
python app1.py
```

The Flask app runs on `http://localhost:8000`.

### 2. Frontend (ReactJS)

The frontend is served using Flask's static files feature. Ensure the ReactJS build is placed in the `frontend/build` directory.

If you're making changes to the React frontend:

* Navigate to the `frontend` folder:

```bash
cd frontend
```

* Install the dependencies:

```bash
npm install
```

* Build the project:

```bash
npm run build
```

* The build will be placed in `frontend/build`, and Flask will serve it.

### 3. Database (MongoDB)

* Make sure MongoDB is running on port `29027` as specified in the connection string inside `app1.py`.
* Use a MongoDB collection named `movies` and a collection for users named `users`.

## Running the Application

Once the Flask backend and MongoDB are set up and running:

* Access the app at `http://localhost:8000`.

## API Endpoints

* **Home**: `/`
   * Fetches and displays a list of movies, with optional filtering by genre and language.
* **Movie Details**: `/movie/<movie_id>`
   * Displays detailed information about a specific movie.
* **Analysis API**: `/api/analysis`
   * Returns aggregated movie data like revenue per genre, top actors, ROI, etc.
* **Signup**: `/signup`
   * User registration page.
* **Login**: `/login`
   * User login page.
* **Logout**: `/logout`
   * Logs the user out.

## Sharding

The MongoDB data is distributed across three shards, with each shard handling movies based on their `release_date`. Ensure your shards are properly set up before running the application.
