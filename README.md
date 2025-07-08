# RandMov

A tool to get random movies from your Letterboxd watchlist. Available in two modes:

- **Local Chrome Driver Webscraper** (uses Selenium and Chrome, for local use only)
- **HTML Parser Web App** (uses requests/BeautifulSoup, for web deployment or local Flask)

---

## Two Ways to Use

### 1. Local Chrome Driver Webscraper (Selenium)

**Script:** `randmov_local_chrome_parser.py`

#### Prerequisites
- Python 3.7+
- Google Chrome installed
- ChromeDriver (handled automatically by `chromedriver-autoinstaller`)
- All dependencies in `requirements.txt`

#### Installation
   ```bash
   pip install -r requirements.txt
   ```

#### Usage
```bash
python randmov_local_chrome_parser.py
```
- This script will prompt for your Letterboxd username and password.
- It will use Selenium to log in, fetch your watchlist, and select a random movie.
- **Note:** This script is intended for local use only and will not work on most free web hosts.

---

### 2. HTML Parser Web App (Flask)

**Scripts:** `randmov_html_parser.py` (logic) + `app.py` (Flask web app)

#### Prerequisites
- Python 3.7+
- All dependencies in `requirements.txt`

#### Installation
   ```bash
   pip install -r requirements.txt
   ```

#### Local Usage
   ```bash
python app.py
```
- Open your browser and go to `http://localhost:5000`
- Enter your Letterboxd username (no password required)
- The app will fetch your public watchlist and display a random movie

#### Web Deployment
- Deploy `app.py` and `randmov_html_parser.py` to a web host that allows outbound HTTP requests (e.g., Render, Fly.io, Railway, or PythonAnywhere **paid** account)
- See deployment instructions in this README for details

---

## File Structure

```
├── randmov_local_chrome_parser.py  # Local Chrome driver webscraper (Selenium)
├── randmov_html_parser.py          # HTML parser logic (requests/BeautifulSoup)
├── app.py                         # Flask web application
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## Deployment Notes
- **Local Chrome Driver Webscraper**: For local use only. Not suitable for most web hosts.
- **HTML Parser Web App**: Can be deployed to any host that allows outbound HTTP requests (not PythonAnywhere free tier).

For more details, see the full instructions below for each mode.