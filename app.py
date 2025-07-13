from flask import Flask, request, render_template_string, send_from_directory, jsonify
from randmov_html_parser import fetch_watchlist
from qrng import qrng
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import requests
import json

app = Flask(__name__)

# Create static directory for images if it doesn't exist
os.makedirs('static', exist_ok=True)

def fetch_movie_details(json_endpoint):
    """Fetch movie details from Letterboxd JSON endpoint"""
    try:
        url = f"https://letterboxd.com{json_endpoint}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return None

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
    .container { max-width: 800px; margin-top: 5vh; }
    .card { background: #232526; border: none; box-shadow: 0 4px 24px rgba(0,0,0,0.2); }
    .form-label { font-weight: 500; }
    .btn-primary { background: #00e054; border: none; }
    .btn-primary:hover { background: #00b340; }
    .movie-card { background: #181a1b; border-radius: 1rem; padding: 1.5rem; margin-top: 2rem; }
    .movie-title { font-size: 1.4rem; font-weight: 600; }
    .movie-link { color: #00e054; text-decoration: none; }
    .movie-link:hover { text-decoration: underline; }
    .watchlist-toggle { color: #00e054; cursor: pointer; }
    .watchlist-list { max-height: 400px; overflow-y: auto; }
    .footer { margin-top: 3rem; color: #aaa; font-size: 0.95rem; text-align: center; }
    .movie-iframe { width: 100%; max-width: 400px; height: 600px; border: 0; margin: 1rem auto 0 auto; display: block; }
    .quantum-info { background: #181a1b; border-radius: 1rem; padding: 1.5rem; margin-top: 1rem; }
    .circuit-image { max-width: 100%; height: auto; border-radius: 0.5rem; margin-top: 1rem; }
    .quantum-details { font-size: 0.9rem; color: #fff; margin-top: 0.5rem; }
    .loading { display: none; text-align: center; margin-top: 1rem; }
    .loading-spinner { border: 3px solid #f3f3f3; border-top: 3px solid #00e054; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; margin: 0 auto; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .movie-title, .quantum-info h5, .quantum-info h6, .text-white, .movie-card .mt-2, .quantum-info { color: #fff !important; }
    .movie-selection { background: #181a1b; border-radius: 1rem; padding: 1.5rem; margin-top: 1rem; }
    .movie-checkbox { margin-right: 15px; }
    .movie-grid-item { 
      background: #2a2d2e; 
      border-radius: 0.5rem; 
      padding: 1rem; 
      margin-bottom: 0.5rem; 
      border: 1px solid #444;
      transition: all 0.2s ease;
    }
    .movie-grid-item:hover { 
      background: #323536; 
      border-color: #00e054;
    }
    .movie-info { display: flex; flex-direction: column; }
    .movie-title { font-weight: 600; margin-bottom: 0.5rem; }
    .movie-details { 
      font-size: 0.85rem; 
      color: #aaa; 
      font-style: italic;
    }
    .loading-text { color: #666; }
    .select-all-section { background: #2a2d2e; border-radius: 0.5rem; padding: 1rem; margin-bottom: 1rem; }
    .form-check-input:checked { background-color: #00e054; border-color: #00e054; }
    .form-check-label { color: #fff; cursor: pointer; }
    .selection-summary { background: #2a2d2e; border-radius: 0.5rem; padding: 1rem; margin-top: 1rem; }
    .filters-section { 
      background: #2a2d2e; 
      border-radius: 0.5rem; 
      padding: 1rem; 
      margin-bottom: 1rem;
      border: 1px solid #444;
    }
    .form-select { 
      background-color: #181a1b; 
      border-color: #444; 
      color: #fff;
    }
    .form-select:focus { 
      background-color: #181a1b; 
      border-color: #00e054; 
      color: #fff;
      box-shadow: 0 0 0 0.2rem rgba(0, 224, 84, 0.25);
    }
    .form-select option { 
      background-color: #181a1b; 
      color: #fff;
    }
    .movie-grid-item.hidden { 
      display: none !important; 
    }
    .watchlist-grid { 
      max-height: 500px; 
      overflow-y: auto; 
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 0.5rem;
      padding: 0.5rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="text-center mb-4">
      <img src="/static/logo.jpg" alt="RandMov Logo" style="max-width:100%; height:auto; max-height:200px; border-radius:12px; box-shadow:0 2px 8px #0006; margin-bottom:10px;">
      <p class="lead">Get a random movie from your Letterboxd watchlist using a simulated quantum random number generator. You can specify a set of movies to narrow down the pool to choose from!</p>
    </div>
    
    {% if not movies %}
    <div class="card p-4">
      <form method="post">
        <div class="mb-3">
          <label for="username" class="form-label">Letterboxd Username</label>
          <input type="text" class="form-control" id="username" name="username" placeholder="e.g. your_username" required value="{{ request.form.username or '' }}">
        </div>
        <button type="submit" class="btn btn-primary w-100" id="submitBtn">Load Watchlist</button>
      </form>
      <div class="loading" id="loading">
        <div class="loading-spinner"></div>
        <p class="mt-2">Fetching your watchlist...</p>
      </div>
      {% if error %}
        <div class="alert alert-danger mt-3" role="alert">{{ error }}</div>
      {% endif %}
    </div>
    {% else %}
    
    <div class="card p-4">
      <form method="post">
        <input type="hidden" name="username" value="{{ request.form.username }}">
        <input type="hidden" name="step" value="select">
        
        <div class="movie-selection">
          <h5 class="text-white mb-3">Select those movies you would like to choose one at random from:</h5>          
          <div class="filters-section">
            <div class="row">
              <div class="col-md-4 mb-3">
                <label for="directorFilter" class="text-white mb-3">Director:</label>
                <select class="form-select" id="directorFilter" onchange="applyFilters()">
                  <option value="">All Directors</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label for="yearFilter" class="text-white mb-3">Year:</label>
                <select class="form-select" id="yearFilter" onchange="applyFilters()">
                  <option value="">All Years</option>
                  <option value="2020s">2020s</option>
                  <option value="2010s">2010s</option>
                  <option value="2000s">2000s</option>
                  <option value="1990s">1990s</option>
                  <option value="1980s">1980s</option>
                  <option value="1970s">1970s</option>
                  <option value="1960s">1960s</option>
                  <option value="1950s">1950s</option>
                  <option value="1940s">1940s</option>
                  <option value="1930s">1930s</option>
                  <option value="1920s">1920s</option>
                  <option value="pre-1920">Pre-1920</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label for="runtimeFilter" class="text-white mb-3">Runtime:</label>
                <select class="form-select" id="runtimeFilter" onchange="applyFilters()">
                  <option value="">All Runtimes</option>
                  <option value="0-90">Under 90 min</option>
                  <option value="90-120">90-120 min</option>
                  <option value="120-150">120-150 min</option>
                  <option value="150+">Over 150 min</option>
                </select>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <button type="button" class="btn btn-outline-secondary btn-sm" onclick="clearFilters()">
                  Clear Filters
                </button>
                <span class="ms-3 text-white">
                  Showing <span id="visibleCount">{{ movies|length }}</span> of {{ movies|length }} movies
                </span>
              </div>
            </div>
          </div>

          <div class="select-all-section">
            <div class="form-check">
              <input class="form-check-input" type="checkbox" id="selectAll" onchange="toggleAllMovies()">
              <label class="form-check-label" for="selectAll">
                <strong>Select all the movies in the watchlist ({{ movies|length }} total)</strong>
              </label>
            </div>
          </div>
          
          <div class="watchlist-grid">
              {% for movie in movies %}
              <div class="movie-grid-item">
                <div class="form-check">
                  <input class="form-check-input movie-checkbox" type="checkbox" name="selected_movies" value="{{ loop.index0 }}" id="movie{{ loop.index0 }}" 
                         data-json-endpoint="{{ movie.json }}" data-movie-name="{{ movie.name }}" data-movie-url="{{ movie.url }}"
                         {% if loop.index0 in selected_movies %}checked{% endif %}>
                  <div class="movie-info">
                    <div class="movie-title">
                      <a href="{{ movie.url }}" class="movie-link" target="_blank">{{ movie.name }}</a>
                    </div>
                    <div class="movie-details" id="details{{ loop.index0 }}" data-json-endpoint="{{ movie.json }}">
                      <span class="loading-text">Loading details...</span>
                    </div>
                  </div>
                </div>
              </div>
              {% endfor %}
            </div>
          
                      <div class="selection-summary">
              <p class="form-check-label"><strong>Selected <span id="selectedCount">{{ selected_movies|length if selected_movies else 0 }}</span> movies:</strong></p>
              <div id="selectedMoviesList" class="selected-movies-list" style="max-height: 150px; overflow-y: auto; margin: 10px 0; display: none;">
                <!-- Selected movies will be populated here by JavaScript -->
              </div>
              <button type="submit" class="btn btn-primary" id="submitBtn" {% if not selected_movies %}disabled{% endif %}>
                <strong>Get Random Movie from Selected</strong>
              </button>
            </div>
        </div>
      </form>
    </div>
    {% endif %}
    
    {% if random_movie %}
    <div class="card p-4">
      <div class="movie-card text-center">
        <h5 class="text-white">And the chosen movie is ...</h5
        <div class="movie-title">
          <a href="{{ random_movie.url }}" class="movie-link" target="_blank">{{ random_movie.name }}</a>
        </div>
        <a href="{{ random_movie.url }}" target="_blank" class="btn btn-outline-success mt-3 mb-2">
          View Poster & Details on Letterboxd
        </a>
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
    </div>
    {% endif %}
    
    <div class="footer">
      <span>Made with <span style="color:#00e054;">&#9733;</span> using Flask, Letterboxd & Qiskit. Developed by <a href="https://github.com/pablo-gf" target="_blank" style="color:#00e054; text-decoration:underline;">Pablo Gutiérrez Félix</a></span>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <script>
    function toggleAllMovies() {
      const selectAll = document.getElementById('selectAll');
      const checkboxes = document.querySelectorAll('.movie-checkbox');
      const submitBtn = document.getElementById('submitBtn');
      
      checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
      });
      
      updateSelectedCount();
      updateSubmitButton();
      updateSelectedMoviesList();
    }
    
    function updateSelectedCount() {
      const checkboxes = document.querySelectorAll('.movie-checkbox:checked');
      document.getElementById('selectedCount').textContent = checkboxes.length;
    }
    
    function updateSubmitButton() {
      const checkboxes = document.querySelectorAll('.movie-checkbox:checked');
      const submitBtn = document.getElementById('submitBtn');
      submitBtn.disabled = checkboxes.length === 0;
    }
    
    function updateSelectedMoviesList() {
      const checkboxes = document.querySelectorAll('.movie-checkbox:checked');
      const selectedMoviesList = document.getElementById('selectedMoviesList');
      
      if (checkboxes.length === 0) {
        selectedMoviesList.style.display = 'none';
        return;
      }
      
      selectedMoviesList.innerHTML = '';
      selectedMoviesList.style.display = 'block';
      
      checkboxes.forEach(checkbox => {
        const movieIndex = parseInt(checkbox.value);
        const movieName = checkbox.dataset.movieName;
        const movieUrl = checkbox.dataset.movieUrl;
        
        const movieItem = document.createElement('div');
        movieItem.className = 'selected-movie-item';
        movieItem.style.cssText = 'padding: 8px 0; border-bottom: 1px solid #444;';
        
        const movieLink = document.createElement('a');
        movieLink.href = movieUrl;
        movieLink.className = 'movie-link';
        movieLink.target = '_blank';
        movieLink.textContent = movieName;
        
        movieItem.appendChild(movieLink);
        selectedMoviesList.appendChild(movieItem);
      });
    }
    
    function fetchMovieDetails(movieIndex, jsonEndpoint, detailsElement) {
      fetch('/get_movie_details', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          movie_index: movieIndex,
          json_endpoint: jsonEndpoint
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const director = data.director !== 'Unknown' ? data.director : 'Unknown Director';
          const year = data.year !== 'Unknown' ? data.year : 'Unknown Year';
          const runtime = data.runtime !== 'Unknown' ? data.runtime : 'Unknown Runtime';
          detailsElement.textContent = `${director} (${year}) • ${runtime} min`;
          
          // Store movie data for filtering
          movieData[movieIndex] = {
            director: director,
            year: year,
            runtime: runtime
          };
          
          // Populate director filter after each successful fetch
          populateDirectorFilter();
        } else {
          detailsElement.textContent = 'Details unavailable';
          movieData[movieIndex] = {
            director: 'Unknown Director',
            year: 'Unknown Year',
            runtime: 'Unknown Runtime'
          };
        }
      })
      .catch(error => {
        console.error('Error fetching movie details:', error);
        detailsElement.textContent = 'Details unavailable';
        movieData[movieIndex] = {
          director: 'Unknown Director',
          year: 'Unknown Year',
          runtime: 'Unknown Runtime'
        };
      });
    }
    
    function loadAllMovieDetails() {
      const detailElements = document.querySelectorAll('.movie-details');
      detailElements.forEach((element, index) => {
        const jsonEndpoint = element.dataset.jsonEndpoint;
        if (jsonEndpoint) {
          fetchMovieDetails(index, jsonEndpoint, element);
        }
      });
    }
    
    // Store movie data for filtering
    let movieData = {};
    
    function applyFilters() {
      const directorFilter = document.getElementById('directorFilter').value;
      const yearFilter = document.getElementById('yearFilter').value;
      const runtimeFilter = document.getElementById('runtimeFilter').value;
      const movieItems = document.querySelectorAll('.movie-grid-item');
      let visibleCount = 0;
      
      movieItems.forEach((item, index) => {
        const movieInfo = movieData[index];
        let shouldShow = true;
        
        // Apply director filter
        if (directorFilter && movieInfo && movieInfo.director) {
          if (movieInfo.director !== directorFilter) {
            shouldShow = false;
          }
        }
        
        // Apply year filter
        if (yearFilter && movieInfo && movieInfo.year && movieInfo.year !== 'Unknown Year') {
          const year = parseInt(movieInfo.year);
          switch (yearFilter) {
            case '2020s':
              if (year < 2020 || year > 2029) shouldShow = false;
              break;
            case '2010s':
              if (year < 2010 || year > 2019) shouldShow = false;
              break;
            case '2000s':
              if (year < 2000 || year > 2009) shouldShow = false;
              break;
            case '1990s':
              if (year < 1990 || year > 1999) shouldShow = false;
              break;
            case '1980s':
              if (year < 1980 || year > 1989) shouldShow = false;
              break;
            case '1970s':
              if (year < 1970 || year > 1979) shouldShow = false;
              break;
            case '1960s':
              if (year < 1960 || year > 1969) shouldShow = false;
              break;
            case '1950s':
              if (year < 1950 || year > 1959) shouldShow = false;
              break;
            case '1940s':
              if (year < 1940 || year > 1949) shouldShow = false;
              break;
            case '1930s':
              if (year < 1930 || year > 1939) shouldShow = false;
              break;
            case '1920s':
              if (year < 1920 || year > 1929) shouldShow = false;
              break;
            case 'pre-1920':
              if (year >= 1920) shouldShow = false;
              break;
          }
        }
        
        // Apply runtime filter
        if (runtimeFilter && movieInfo && movieInfo.runtime) {
          const runtime = parseInt(movieInfo.runtime);
          switch (runtimeFilter) {
            case '0-90':
              if (runtime >= 90) shouldShow = false;
              break;
            case '90-120':
              if (runtime < 90 || runtime > 120) shouldShow = false;
              break;
            case '120-150':
              if (runtime < 120 || runtime > 150) shouldShow = false;
              break;
            case '150+':
              if (runtime < 150) shouldShow = false;
              break;
          }
        }
        
        if (shouldShow) {
          item.classList.remove('hidden');
          visibleCount++;
        } else {
          item.classList.add('hidden');
        }
      });
      
      document.getElementById('visibleCount').textContent = visibleCount;
      updateSelectedCount();
      updateSubmitButton();
    }
    
    function clearFilters() {
      document.getElementById('directorFilter').value = '';
      document.getElementById('yearFilter').value = '';
      document.getElementById('runtimeFilter').value = '';
      applyFilters();
    }
    
    function populateDirectorFilter() {
      const directorFilter = document.getElementById('directorFilter');
      const directors = new Set();
      
      Object.values(movieData).forEach(movie => {
        if (movie.director && movie.director !== 'Unknown Director') {
          directors.add(movie.director);
        }
      });
      
      // Clear existing options except the first one
      while (directorFilter.children.length > 1) {
        directorFilter.removeChild(directorFilter.lastChild);
      }
      
      // Add director options
      Array.from(directors).sort().forEach(director => {
        const option = document.createElement('option');
        option.value = director;
        option.textContent = director;
        directorFilter.appendChild(option);
      });
    }
    
    // Add event listeners to checkboxes
    document.addEventListener('DOMContentLoaded', function() {
      const checkboxes = document.querySelectorAll('.movie-checkbox');
      checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
          updateSelectedCount();
          updateSubmitButton();
          updateSelectedMoviesList();
          
          // Update select all checkbox
          const selectAll = document.getElementById('selectAll');
          const allCheckboxes = document.querySelectorAll('.movie-checkbox');
          const checkedCheckboxes = document.querySelectorAll('.movie-checkbox:checked');
          
          if (checkedCheckboxes.length === allCheckboxes.length) {
            selectAll.checked = true;
          } else {
            selectAll.checked = false;
          }
        });
      });
      
      // Initial setup
      updateSelectedCount();
      updateSubmitButton();
      updateSelectedMoviesList();
      
      // Load movie details for all movies
      loadAllMovieDetails();
    });
    
    document.querySelector('form').addEventListener('submit', function() {
      const submitBtn = document.getElementById('submitBtn');
      if (submitBtn) {
        submitBtn.disabled = true; 
        submitBtn.textContent = 'Processing...';
      }
      const loading = document.getElementById('loading');
      if (loading) {
        loading.style.display = 'block';
      }
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
    selected_movies = []
    selected_count = 0
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        step = request.form.get('step', '')
        
        if not username:
            error = 'Please enter a username.'
        else:
            try:
                # Fetch watchlist if not already loaded
                if not movies:
                    movies = fetch_watchlist(username)
                    if not movies:
                        error = 'No movies found for this user.'
                
                # Handle movie selection step
                if step == 'select' and movies:
                    selected_indices = request.form.getlist('selected_movies')
                    selected_movies = [int(idx) for idx in selected_indices if idx.isdigit()]
                    
                    if selected_movies:
                        # Get the selected movies
                        selected_movie_objects = [movies[i] for i in selected_movies]
                        selected_count = len(selected_movie_objects)
                        
                        # Use quantum random number generator on selected movies
                        quantum_result = qrng(len(selected_movie_objects) - 1)
                        random_movie = selected_movie_objects[quantum_result.random_number]
                        
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
                    else:
                        error = 'Please select at least one movie.'
                        
            except Exception as e:
                error = f'Error fetching watchlist: {e}'
    
    return render_template_string(HTML_FORM, movies=movies, random_movie=random_movie, 
                                error=error, quantum_info=quantum_info, 
                                circuit_image=circuit_image, request=request,
                                selected_movies=selected_movies, selected_count=selected_count)

@app.route('/get_movie_details', methods=['POST'])
def get_movie_details():
    """AJAX endpoint to fetch movie details"""
    try:
        data = request.get_json()
        movie_index = data.get('movie_index')
        json_endpoint = data.get('json_endpoint')
        
        if movie_index is not None and json_endpoint:
            movie_details = fetch_movie_details(json_endpoint)
            if movie_details:
                return jsonify({
                    'success': True,
                    'director': movie_details.get('directors', [{}])[0].get('name', 'Unknown') if movie_details.get('directors') else 'Unknown',
                    'year': movie_details.get('releaseYear', 'Unknown'),
                    'runtime': movie_details.get('runTime', 'Unknown')
                })
        
        return jsonify({'success': False, 'error': 'Invalid request'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 