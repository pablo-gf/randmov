# RandMov

A tool to get random movies from your Letterboxd watchlist. Available both as a web application and a command-line script.

## Two Ways to Use

### Option 1: Web Application (Recommended)

Visit the live web application hosted on PythonAnywhere to use the tool through your browser.

**Coming Soon**: Link will be provided once deployed.

### Option 2: Local Command Line Script

Run the original script directly on your computer using the terminal.

## Files Structure

```
├── randmov.py          # Original command-line script
├── app.py              # Flask web application
├── wsgi.py             # WSGI entry point for PythonAnywhere
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface template
└── README.md           # This file
```

## Option 1: Web Application Usage

### Using the Live Web App
1. Visit the web application URL (will be provided after deployment)
2. Enter your Letterboxd username and password
3. Click "Get Random Movie"
4. Wait for the process to complete
5. View your randomly selected movie

### Local Web Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the web application:
   ```bash
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

## Option 2: Command Line Usage

### Prerequisites
- Python 3.12 or higher
- Google Chrome installed
- ChromeDriver (automatically installed via `chromedriver-autoinstaller`)

### Installation

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd randmov
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Linux/macOS
   # or
   .venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the script:
```bash
python randmov.py
```

The script will:
1. Prompt for your Letterboxd username and password
2. Log into Letterboxd automatically
3. Export your watchlist data
4. Extract the ZIP file containing the watchlist
5. Load the watchlist CSV file
6. Select and display a random movie from the watchlist
7. Clean up all temporary files

## PythonAnywhere Deployment (For Web App)

### Step 1: Upload Files
1. Create a new PythonAnywhere account
2. Go to the Files tab
3. Upload all the files from this project to your home directory

### Step 2: Set Up Virtual Environment
1. Go to the Consoles tab
2. Open a Bash console
3. Create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 myenv
   ```
4. Activate the environment:
   ```bash
   workon myenv
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Configure Web App
1. Go to the Web tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.9
5. Set the source code directory to your home directory
6. Set the working directory to your home directory
7. Set the WSGI configuration file to point to your `wsgi.py`

### Step 4: Update WSGI Configuration
1. Click on the WSGI configuration file link
2. Replace the content with:
   ```python
   import sys
   path = '/home/yourusername'
   if path not in sys.path:
       sys.path.append(path)
   
   from wsgi import app as application
   ```
   (Replace `yourusername` with your actual PythonAnywhere username)

### Step 5: Install Chrome/ChromeDriver
1. In the Bash console, install Chrome:
   ```bash
   sudo apt-get update
   sudo apt-get install -y google-chrome-stable
   ```
2. The `chromedriver-autoinstaller` package will handle ChromeDriver installation automatically

### Step 6: Reload Web App
1. Go back to the Web tab
2. Click "Reload" to restart your web app

## How It Works

### Web Application
1. **User Interface**: Users enter their Letterboxd credentials through a web form
2. **Background Processing**: The Flask app creates a background thread to run the `randmov.py` script
3. **Input Mocking**: The web app mocks the `input()` and `getpass()` functions to provide credentials
4. **Output Capture**: The script's output is captured and parsed to extract the selected movie
5. **Real-time Updates**: The web interface polls for status updates and displays progress
6. **Result Display**: Once complete, the selected movie is displayed to the user

### Command Line Script
1. **Direct Execution**: Runs the `randmov.py` script directly
2. **Interactive Input**: Prompts user for credentials via terminal
3. **Automated Process**: Handles login, data export, and movie selection automatically
4. **Immediate Output**: Displays results directly in the terminal

## Security Notes

- User credentials are only stored in memory during processing
- All temporary files are cleaned up after processing
- No credentials are logged or stored permanently
- Each session uses a unique temporary directory

## Troubleshooting

### Web Application Issues:
1. **Chrome/ChromeDriver not found**: Make sure Chrome is installed on PythonAnywhere
2. **Import errors**: Ensure all dependencies are installed in your virtual environment
3. **Permission errors**: Check that your working directory has proper permissions
4. **Timeout errors**: The scraping process can take several minutes, especially for large watchlists

### Command Line Issues:
- Ensure Google Chrome is installed and updated
- If the script fails to locate elements, verify the CSS selectors in the code match the current Letterboxd website structure
- If the virtual environment is not working correctly, recreate it using:
  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### Debug Mode:
To enable debug mode locally, set `debug=True` in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

## Customization

You can customize the web interface by modifying `templates/index.html`. The current design uses:
- Bootstrap 5 for styling
- Font Awesome for icons
- Custom CSS for gradients and animations
- JavaScript for real-time updates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: Make sure to comply with Letterboxd's terms of service when using this application.