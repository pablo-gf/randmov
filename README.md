# RandMov

A tool to get random movies from your Letterboxd watchlist. Web app available through Render here: [https://randmov.onrender.com/](https://randmov.onrender.com/). This app is available in two modes:

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
- All dependencies in `requirements_web.txt`

#### Installation
   ```bash
   pip install -r requirements_web.txt
   ```

#### Local Usage
   ```bash
python app.py
```
- Open your browser and go to `http://localhost:5000`
- Enter your Letterboxd username (no password required)
- The app will fetch your public watchlist and display a random movie

--

## File Structure

```
├── randmov_local_chrome_parser.py  # Local Chrome driver webscraper
├── randmov_html_parser.py          # HTML parser logic
├── app.py                          # Flask web application
├── requirements_web.txt            # Python dependencies for the website version
├── requirements_local.txt          # Python dependencies for the local version
└── README.md                       # This file
```