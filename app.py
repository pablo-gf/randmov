from flask import Flask, render_template, request, jsonify
import os
import threading
import time
import tempfile
import shutil
import sys
from io import StringIO
import contextlib

import randmov

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Store active scraping sessions
active_sessions = {}

class WebScraper:
    def __init__(self, username, password, session_id):
        self.username = username
        self.password = password
        self.session_id = session_id
        self.status = 'initializing'
        self.message = 'Initializing scraper...'
        self.result = None
        self.error = None
        self.work_dir = tempfile.mkdtemp(prefix=f'letterboxd_{session_id}_')
        
    def run(self):
        """Run the scraping process using the existing randmov module"""
        try:
            # Change to work directory
            original_dir = os.getcwd()
            os.chdir(self.work_dir)
            
            self.status = 'starting'
            self.message = 'Starting browser...'
            
            # Capture stdout to get the result
            captured_output = StringIO()
            
            # Mock input function to provide credentials
            def mock_input(prompt):
                if 'username' in prompt.lower():
                    return self.username
                elif 'password' in prompt.lower():
                    return self.password
                return ''
            
            # Mock stdiomask.getpass
            def mock_getpass(prompt, mask='*'):
                return self.password
            
            # Store original functions
            import builtins
            original_input = builtins.input
            original_getpass = randmov.stdiomask.getpass
            
            try:
                # Replace input functions
                builtins.input = mock_input
                randmov.stdiomask.getpass = mock_getpass
                
                # Capture stdout
                with contextlib.redirect_stdout(captured_output):
                    # Run the main function
                    randmov.main()
                    
            finally:
                # Restore original functions
                builtins.input = original_input
                randmov.stdiomask.getpass = original_getpass
                
            # Parse the output to get the selected movie
            output = captured_output.getvalue()
            
            # Look for the result in the output
            if "Selected movie:" in output:
                movie_name = output.split("Selected movie:")[1].strip()
                self.result = {
                    'movie_name': movie_name,
                    'total_movies': 'Unknown',  # Could parse from CSV if needed
                    'year': 'Unknown',
                    'director': 'Unknown',
                    'url': ''
                }
                self.status = 'completed'
                self.message = 'Random movie selected successfully!'
            else:
                self.error = "Could not find selected movie in output"
                self.status = 'error'
                
        except Exception as e:
            self.error = f"An error occurred: {str(e)}"
            self.status = 'error'
            self.message = 'An error occurred during processing'
            
        finally:
            # Clean up
            try:
                # Clean up any files that might have been created
                for file in os.listdir(self.work_dir):
                    file_path = os.path.join(self.work_dir, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                
                # Remove work directory
                shutil.rmtree(self.work_dir)
            except:
                pass
            
            # Restore original directory
            os.chdir(original_dir)
    
    def get_status(self):
        """Get current status"""
        return {
            'status': self.status,
            'message': self.message,
            'error': self.error
        }
    
    def get_result(self):
        """Get the result if completed"""
        if self.status == 'completed' and self.result:
            return self.result
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Generate session ID
    session_id = os.urandom(16).hex()
    
    # Create scraper instance
    scraper = WebScraper(username, password, session_id)
    
    # Store in active sessions
    active_sessions[session_id] = scraper
    
    # Start scraping in background thread
    thread = threading.Thread(target=scraper.run)
    thread.daemon = True
    thread.start()
    
    return jsonify({'session_id': session_id})

@app.route('/check_status/<session_id>')
def check_status(session_id):
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    scraper = active_sessions[session_id]
    status = scraper.get_status()
    
    # Clean up completed sessions
    if status['status'] in ['completed', 'error']:
        del active_sessions[session_id]
    
    return jsonify(status)

@app.route('/get_result/<session_id>')
def get_result(session_id):
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    scraper = active_sessions[session_id]
    result = scraper.get_result()
    
    if result:
        # Clean up session after getting result
        del active_sessions[session_id]
        return jsonify(result)
    else:
        return jsonify({'error': 'Result not ready'}), 400

if __name__ == '__main__':
    app.run(debug=True) 