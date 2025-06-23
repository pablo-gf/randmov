import requests
from bs4 import BeautifulSoup
import time
import os
import sys
from urllib.parse import urljoin

class LetterboxdScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def login(self):
        """Login to Letterboxd"""
        print("Attempting to login to Letterboxd...")
                
        # Prepare login payload
        login_data = {
            "username": self.username,
            "password": self.password,
        }
        
        # Submit login form
        try:
            login_resp = self.session.post("https://letterboxd.com/sign-in/", data=login_data)
            login_resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error during login: {e}")
            return False
            
        # Check if login was successful by looking for redirect or error messages
        if "sign-in" in login_resp.url or "error" in login_resp.text.lower():
            print("Login failed. Please check your username and password.")
            return False
            
        print("Login successful!")
        return True
        
    def navigate_to_data_page(self):
        """Navigate to the data export page"""
        print("Navigating to data export page...")
        
        try:
            resp = self.session.get("https://letterboxd.com/settings/data/")
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error accessing data export page: {e}")
            return None
            
        return BeautifulSoup(resp.text, "html.parser")
        
    def trigger_data_export(self, soup):
        """Trigger the data export process"""
        print("Looking for export button...")
        
        # Look for export form or button
        export_form = soup.find("form", {"action": lambda x: x and "export" in x})
        if not export_form:
            # Try to find any form that might be for export
            forms = soup.find_all("form")
            export_form = None
            for form in forms:
                if any(keyword in str(form).lower() for keyword in ["export", "download", "data"]):
                    export_form = form
                    break
                    
        if not export_form:
            print("Could not find export form. The page structure might have changed.")
            return False
            
        # Get form action URL
        form_action = export_form.get("action")
        if form_action:
            export_url = urljoin("https://letterboxd.com", form_action)
        else:
            export_url = "https://letterboxd.com/settings/data/"
            
        # Get all form inputs
        form_data = {}
        for input_tag in export_form.find_all("input"):
            name = input_tag.get("name")
            value = input_tag.get("value", "")
            if name:
                form_data[name] = value
                
        print(f"Triggering export to: {export_url}")
        
        try:
            export_resp = self.session.post(export_url, data=form_data)
            export_resp.raise_for_status()
        except requests.RequestException as e:
            print(f"Error triggering export: {e}")
            return False
            
        return export_resp
        
    def download_data_file(self, export_resp):
        """Download the data file"""
        print("Downloading data file...")
        
        # Check if the response contains a file
        content_type = export_resp.headers.get('content-type', '')
        
        if 'application/zip' in content_type or 'application/octet-stream' in content_type:
            filename = "letterboxd_data.zip"
        elif 'text/csv' in content_type:
            filename = "letterboxd_data.csv"
        else:
            # Try to extract filename from headers
            content_disposition = export_resp.headers.get('content-disposition', '')
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].strip('"')
            else:
                filename = "letterboxd_data.zip"
                
        # Save the file
        with open(filename, "wb") as f:
            f.write(export_resp.content)
            
        print(f"Data file saved as: {filename}")
        return filename
        
    def run(self):
        """Main method to run the scraper"""
        print("Starting Letterboxd data export...")
        
        # Step 1: Login
        if not self.login():
            return False
            
        # Step 2: Navigate to data page
        soup = self.navigate_to_data_page()
        if not soup:
            return False
            
        # Step 3: Trigger export
        export_resp = self.trigger_data_export(soup)
        if not export_resp:
            return False
            
        # Step 4: Download file
        filename = self.download_data_file(export_resp)
        
        print(f"Successfully exported Letterboxd data to {filename}")
        return True

def main():
    # Get credentials from environment variables or config file
    username = os.getenv("LETTERBOXD_USERNAME")
    password = os.getenv("LETTERBOXD_PASSWORD")
    
    # If not found in environment variables, try config file
    if not username or not password:
        try:
            from config import USERNAME, PASSWORD
            username = USERNAME
            password = PASSWORD
        except ImportError:
            pass
    
    if not username or not password:
        print("Please set your Letterboxd credentials:")
        print("\nOption 1: Environment variables (recommended):")
        print("export LETTERBOXD_USERNAME='your_username'")
        print("export LETTERBOXD_PASSWORD='your_password'")
        print("\nOption 2: Edit config.py file:")
        print("Set USERNAME and PASSWORD variables in config.py")
        print("\nOption 3: Edit main.py directly:")
        print("Modify the main() function to include your credentials")
        sys.exit(1)
        
    # Create and run scraper
    scraper = LetterboxdScraper(username, password)
    success = scraper.run()
    
    if not success:
        print("Failed to export data. Please check your credentials and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()