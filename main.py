import requests
from bs4 import BeautifulSoup
from getpass import getpass

session = requests.Session()

# Try to access the data settings page first
check_page = session.get('https://letterboxd.com/settings/data/')
if 'Sign in to Letterboxd' in check_page.text or 'Sign in' in check_page.text:
    # Not logged in, prompt for credentials
    print('Session not authenticated. Please log in.')
    # 1. Get the login page to fetch CSRF token
    login_page = session.get('https://letterboxd.com/sign-in/')
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_input = soup.find('input', {'name': '__csrf'})
    csrf_token = csrf_input['value'] if csrf_input else None

    username = input('Enter your Letterboxd username: ')
    password = getpass('Enter your Letterboxd password: ')

    login_data = {
        'username': username,
        'password': password,
        '__csrf': csrf_token,
        'authenticationCode': '',
    }

    # 2. Send POST request to the correct endpoint
    response = session.post('https://letterboxd.com/user/login.do', data=login_data)

    # 3. Check if login was successful (look for your username or profile link in the response)
    if username.lower() in response.text.lower():
        print('Login successful!')
        data_page = session.get('https://letterboxd.com/settings/data/')
        print(data_page.text)
    else:
        print('Login failed.')
else:
    print('Session already authenticated!')
    print(check_page.text) 