# RandMov

RandMov is a Python project that automates the process of logging into Letterboxd, exporting movie data, and selecting a random movie from the watchlist.

## Features
- Automates login to Letterboxd using Selenium.
- Exports movie data from Letterboxd.
- Extracts the exported ZIP file containing the watchlist.
- Loads the watchlist CSV file and selects a random movie.

## Requirements
- Python 3.12 or higher
- Google Chrome installed
- ChromeDriver (automatically installed via `chromedriver-autoinstaller`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd randmov
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Linux/macOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script:
```bash
python randmov.py
```

The script will:
1. Prompt for your username and password
3. Log into Letterboxd.
4. Export your watchlist data.
5. Extract the ZIP file containing the watchlist.
6. Load the watchlist CSV file.
7. Select and display a random movie from the watchlist.

## Troubleshooting

- Ensure Google Chrome is installed and updated.
- If the script fails to locate elements, verify the CSS selectors in the code match the current Letterboxd website structure.
- If the virtual environment is not working correctly, recreate it using:
  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## License
This project is licensed under the MIT License.