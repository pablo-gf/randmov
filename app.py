from flask import Flask, request, render_template_string
from randmov_html_parser import fetch_watchlist
import random

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>RandMov – Random Letterboxd Movie</title>
  <link rel="icon" href="https://letterboxd.com/favicon.ico">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: linear-gradient(135deg, #232526 0%, #414345 100%); min-height: 100vh; color: #fff; }
    .container { max-width: 500px; margin-top: 5vh; }
    .card { background: #232526; border: none; box-shadow: 0 4px 24px rgba(0,0,0,0.2); }
    .form-label { font-weight: 500; }
    .btn-primary { background: #00e054; border: none; }
    .btn-primary:hover { background: #00b340; }
    .movie-card { background: #181a1b; border-radius: 1rem; padding: 1.5rem; margin-top: 2rem; }
    .movie-title { font-size: 1.4rem; font-weight: 600; }
    .movie-link { color: #00e054; text-decoration: none; }
    .movie-link:hover { text-decoration: underline; }
    .watchlist-toggle { color: #00e054; cursor: pointer; }
    .watchlist-list { max-height: 300px; overflow-y: auto; }
    .footer { margin-top: 3rem; color: #aaa; font-size: 0.95rem; text-align: center; }
    .movie-iframe { width: 100%; max-width: 400px; height: 600px; border: 0; margin: 1rem auto 0 auto; display: block; }
  </style>
</head>
<body>
  <div class="container">
    <div class="text-center mb-4">
      <h1 class="fw-bold">RandMov</h1>
      <p class="lead">Get a random movie from your Letterboxd watchlist</p>
    </div>
    <div class="card p-4">
      <form method="post">
        <div class="mb-3">
          <label for="username" class="form-label">Letterboxd Username</label>
          <input type="text" class="form-control" id="username" name="username" placeholder="e.g. confuoco" required value="{{ request.form.username or '' }}">
        </div>
        <button type="submit" class="btn btn-primary w-100">Get Random Movie</button>
      </form>
      {% if error %}
        <div class="alert alert-danger mt-3" role="alert">{{ error }}</div>
      {% endif %}
      {% if movies %}
        <div class="movie-card text-center">
          <div class="movie-title">
            <a href="{{ random_movie.url }}" class="movie-link" target="_blank">{{ random_movie.name }}</a>
          </div>
          <a href="{{ random_movie.url }}" target="_blank" class="btn btn-outline-success mt-3 mb-2">
            View Poster & Details on Letterboxd
          </a>
          <iframe src="{{ random_movie.url }}" class="movie-iframe"></iframe>
          <div class="mt-2">Randomly selected from your <b>{{ movies|length }}</b> movies.</div>
        </div>
        <div class="mt-4">
          <a class="watchlist-toggle" data-bs-toggle="collapse" href="#watchlistCollapse" role="button" aria-expanded="false" aria-controls="watchlistCollapse">
            <span class="me-1">&#9660;</span>Show/Hide Full Watchlist
          </a>
          <div class="collapse mt-2" id="watchlistCollapse">
            <ul class="list-group watchlist-list">
              {% for movie in movies %}
                <li class="list-group-item bg-dark text-light border-secondary py-2">
                  <a href="{{ movie.url }}" class="movie-link" target="_blank">{{ movie.name }}</a>
                </li>
              {% endfor %}
            </ul>
          </div>
        </div>
      {% endif %}
    </div>
    <div class="footer">
      <span>Made with <span style="color:#00e054;">&#9733;</span> using Flask & Letterboxd</span>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = None
    random_movie = None
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            try:
                movies = fetch_watchlist(username)
                if not movies:
                    error = 'No movies found for this user.'
                else:
                    random_movie = random.choice(movies)
            except Exception as e:
                error = f'Error fetching watchlist: {e}'
        else:
            error = 'Please enter a username.'
    return render_template_string(HTML_FORM, movies=movies, random_movie=random_movie, error=error, request=request)

if __name__ == '__main__':
    app.run(debug=True) 