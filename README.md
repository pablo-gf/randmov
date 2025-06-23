# Letterboxd Data Export Scraper

This project provides a web scraper to automatically log into Letterboxd and download your personal data export (CSV file) from the settings page.

## Features

- Automated login to Letterboxd using your credentials
- Navigation to the data export page
- Automatic triggering of data export
- Download and save of the CSV/ZIP file
- Error handling and user feedback
- Secure credential management using environment variables

## Prerequisites

- Python 3.7 or higher
- Letterboxd account with username and password

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Using Environment Variables (Recommended)

Set your Letterboxd credentials as environment variables:

```bash
export LETTERBOXD_USERNAME="your_username"
export LETTERBOXD_PASSWORD="your_password"
```

Then run the scraper:

```bash
python main.py
```

### Method 2: Direct Credential Input

If you prefer to modify the script directly, you can edit the `main()` function in `main.py` to include your credentials:

```python
def main():
    username = "your_username"  # Replace with your actual username
    password = "your_password"  # Replace with your actual password
    
    scraper = LetterboxdScraper(username, password)
    success = scraper.run()
    
    if not success:
        print("Failed to export data. Please check your credentials and try again.")
        sys.exit(1)
```

## How it Works

1. **Login Process**: The scraper visits the Letterboxd sign-in page, extracts the CSRF token, and submits your credentials
2. **Navigation**: After successful login, it navigates to the data export page at `/settings/data/`
3. **Export Trigger**: It finds and submits the export form to trigger the data download
4. **File Download**: The resulting CSV or ZIP file is saved to your local directory

## Output

The scraper will download your Letterboxd data as either:
- `letterboxd_data.csv` (if the export is in CSV format)
- `letterboxd_data.zip` (if the export is in ZIP format)

## Error Handling

The scraper includes comprehensive error handling for:
- Network connection issues
- Invalid credentials
- Missing CSRF tokens
- Changes in website structure
- File download failures

## Security Notes

- **Never commit your credentials to version control**
- Use environment variables for credential management
- The scraper uses a realistic User-Agent to avoid detection
- All requests are made through a session to maintain login state

## Troubleshooting

### Login Issues
- Verify your username and password are correct
- Check if Letterboxd has any CAPTCHA or additional verification
- Ensure your account is not locked or suspended

### Export Issues
- The scraper may need updates if Letterboxd changes their website structure
- Some accounts might have restrictions on data export
- Check if you have sufficient permissions to export data

### Network Issues
- Ensure you have a stable internet connection
- Check if Letterboxd is accessible from your location
- Some networks may block automated requests

## Legal and Ethical Considerations

- This scraper is for personal use only
- Respect Letterboxd's Terms of Service
- Do not use this tool for commercial purposes
- Be mindful of rate limiting and server load
- Only download your own data

## Dependencies

- `requests`: HTTP library for making web requests
- `beautifulsoup4`: HTML parsing library
- `lxml`: XML/HTML parser backend for BeautifulSoup

## License

This project is for educational and personal use only. Please respect Letterboxd's terms of service when using this tool.
