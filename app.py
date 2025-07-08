from flask import Flask, request, render_template_string
from randmov_html_parser import fetch_watchlist
import random

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<title>Random Letterboxd Movie</title>
<h1>Enter your Letterboxd username</h1>
<form method="post">
  <input type="text" name="username" required>
  <input type="submit" value="Get Random Movie">
</form>
{% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
{% if movies %}
  <h2>Watchlist ({{ movies|length }} movies):</h2>
  <ul>
    {% for movie in movies %}
      <li><a href="{{ movie.url }}" target="_blank">{{ movie.name }}</a></li>
    {% endfor %}
  </ul>
  <h2>Your random movie is:</h2>
  <p><b><a href="{{ random_movie.url }}" target="_blank">{{ random_movie.name }}</a></b></p>
{% endif %}
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
    return render_template_string(HTML_FORM, movies=movies, random_movie=random_movie, error=error)

if __name__ == '__main__':
    app.run(debug=True) 