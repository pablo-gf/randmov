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

## Configuration

1. Create a `login_details.yml` file in the project directory with the following structure:
   ```yaml
   letterboxd_app:
     username: <your-letterboxd-username>
     password: <your-letterboxd-password>
   ```

2. Ensure the `login_details.yml` file is correctly formatted and contains your Letterboxd credentials.

## Usage

Run the script:
```bash
python randmov.py
```

The script will:
1. Log into Letterboxd.
2. Export your watchlist data.
3. Extract the ZIP file containing the watchlist.
4. Load the watchlist CSV file.
5. Select and display a random movie from the watchlist.

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