# RandMov

A tool that outputs random movies from your Letterboxd watchlist. This program features two options: a local and a web version. The latter uses a simulated **Quantum Random Number Generator (QRNG)** to select the random movie. Web app available through Render here: [https://randmov.onrender.com/](https://randmov.onrender.com/).

---

## Two Ways to Use

### 1. HTML Parser Web App (Flask, Quantum Randomness)

**Scripts:** `randmov_html_parser.py` (logic) + `app.py` (Flask web app) + `qrng.py` (Quantum Random Number Generator simulator)

#### Quantum Random Number Generator (QRNG)

RandMov uses a simulated quantum random number generator, powered by [Qiskit](https://qiskit.org/) and the [AerSimulator](https://github.com/Qiskit/qiskit-aer) backend, to select a random movie from your watchlist.

- The QRNG is implemented in `qrng.py`.
- For each random selection, a quantum circuit is created with as many qubits as needed to cover the range of movies in the watchlist.
- Each qubit is put into superposition using Hadamard gates, then measured.
- The resulting bitstring is interpreted as a random number, and if it falls within the valid range, it is used to select your movie.
- The web app displays the quantum circuit used for your selection.

#### Prerequisites to run the web app locally
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
- The app will fetch your public watchlist and display a random movie, selected using the quantum random number generator
- The quantum circuit used for your selection will be shown on the page

---

### 2. Local Chrome Driver Webscraper (Selenium)

**Script:** `randmov_local_chrome_webscraper.py`

#### Prerequisites
- Python 3.7+
- Google Chrome installed
- ChromeDriver (handled automatically by `chromedriver-autoinstaller`)
- All dependencies in `requirements_local.txt`

#### Installation
   ```bash
   pip install -r requirements_local.txt
   ```

#### Usage
```bash
python randmov_local_chrome_webscraper.py
```
- This script will prompt for your Letterboxd username and password.
- It will use Selenium to log in, fetch your watchlist, and select a random movie (using standard pseudo-random selection).
- **Note:** This script is intended for local use only and will not work on most free web hosts.

---

## File Structure

```
├── randmov_local_chrome_webscraper.py  # Local Chrome driver webscraper
├── randmov_html_parser.py              # HTML parser logic (uses QRNG)
├── app.py                              # Flask web application (uses QRNG)
├── qrng.py                             # Quantum random number generator (Qiskit)
├── requirements_web.txt                # Python dependencies for the website version (QRNG)
├── requirements_local.txt              # Python dependencies for the local version
└── README.md                           # This file
```
