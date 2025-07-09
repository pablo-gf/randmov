from flask import Flask, request, render_template_string, send_from_directory
from randmov_html_parser import fetch_watchlist
from qrng import qrng
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Create static directory for images if it doesn't exist
os.makedirs('static', exist_ok=True)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title> RandMov </title>
  <link rel="icon" type="image/jpeg" href="/static/logo_small.jpg">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: linear-gradient(135deg, #232526 0%, #414345 100%); min-height: 100vh; color: #fff; }
    .container { max-width: 600px; margin-top: 5vh; }
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
    .quantum-info { background: #181a1b; border-radius: 1rem; padding: 1.5rem; margin-top: 1rem; }
    .circuit-image { max-width: 100%; height: auto; border-radius: 0.5rem; margin-top: 1rem; }
    .quantum-details { font-size: 0.9rem; color: #fff; margin-top: 0.5rem; }
    .loading { display: none; text-align: center; margin-top: 1rem; }
    .loading-spinner { border: 3px solid #f3f3f3; border-top: 3px solid #00e054; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .movie-title, .quantum-info h5, .quantum-info h6, .text-white, .movie-card .mt-2, .quantum-info { color: #fff !important; }
  </style>
</head>
<body>
  <div class="container">
    <div class="text-center mb-4">
      <img src="/static/logo.jpg" alt="RandMov Logo" border-radius:12px; box-shadow:0 2px 8px #0006; margin-bottom:10px;">
      <p class="lead">Get a random movie from your Letterboxd watchlist using a simulated quantum random number generator</p>
    </div>
    <div class="card p-4">
      <form method="post">
        <div class="mb-3">
          <label for="username" class="form-label">Letterboxd Username</label>
          <input type="text" class="form-control" id="username" name="username" placeholder="e.g. your_username" required value="{{ request.form.username or '' }}">
        </div>
        <button type="submit" class="btn btn-primary w-100" id="submitBtn">Get Random Movie</button>
      </form>
      <div class="loading" id="loading">
        <div class="loading-spinner"></div>
        <p class="mt-2">Fetching your watchlist and generating quantum randomness...</p>
      </div>
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
          <div class="mt-2 text-white">Randomly selected from the <b>{{ movies|length }} in the watchlist</b> movies.</div>
        </div>
        {% if quantum_info %}
        <div class="quantum-info text-center">
          <h5 class="text-white">Quantum Circuit Used (<strong>{{ quantum_info.num_qubits }} qubits</strong>):</h5>
          {% if circuit_image %}
          <div class="mt-3">
            <img src="data:image/png;base64,{{ circuit_image }}" alt="Quantum Circuit" class="circuit-image">
          </div>
          {% endif %}
        </div>
        {% endif %}
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
      <span>Made with <span style="color:#00e054;">&#9733;</span> using Flask, Letterboxd & Qiskit. Developed by <a href="https://github.com/pablo-gf" target="_blank" style="color:#00e054; text-decoration:underline;">Pablo Gutiérrez Félix</a></span>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    document.querySelector('form').addEventListener('submit', function() {
      document.getElementById('submitBtn').disabled = true; 
      document.getElementById('submitBtn').textContent = 'Processing...';
      document.getElementById('loading').style.display = 'block';
    });
  </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = None
    random_movie = None
    error = None
    quantum_info = None
    circuit_image = None
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if username:
            try:
                movies = fetch_watchlist(username)
                if not movies:
                    error = 'No movies found for this user.'
                else:
                    # Use quantum random number generator instead of random.choice
                    quantum_result = qrng(len(movies) - 1)
                    random_movie = movies[quantum_result.random_number]
                    
                    # Generate quantum circuit visualization
                    try:
                        # Create the circuit image using matplotlib
                        fig, ax = plt.subplots(figsize=(10, 6))
                        quantum_result.qc.draw('mpl', ax=ax)
                        plt.tight_layout()
                        
                        # Convert plot to base64 string for embedding in HTML
                        img_buffer = BytesIO()
                        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                                  facecolor='#232526', edgecolor='none')
                        img_buffer.seek(0)
                        circuit_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                        plt.close()
                        
                        # Create quantum info object
                        quantum_info = {
                            'random_number': quantum_result.random_number,
                            'num_qubits': quantum_result.qc.num_qubits
                        }
                    except Exception as e:
                        # If circuit visualization fails, continue without it
                        print(f"Circuit visualization error: {e}")
                        quantum_info = {
                            'random_number': quantum_result.random_number,
                            'num_qubits': quantum_result.qc.num_qubits
                        }
                        
            except Exception as e:
                error = f'Error fetching watchlist: {e}'
        else:
            error = 'Please enter a username.'
    
    return render_template_string(HTML_FORM, movies=movies, random_movie=random_movie, 
                                error=error, quantum_info=quantum_info, 
                                circuit_image=circuit_image, request=request)

if __name__ == '__main__':
    app.run(debug=True) 