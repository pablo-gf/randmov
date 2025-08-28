import requests
from bs4 import BeautifulSoup
from spinner import spinner
import threading
from qrng import qrng

class Movie:
    def __init__(self, name, poster, url, json):
        self.name = name
        self.poster = poster
        self.url = url
        self.json = json
    
    def __str__(self):
        return f'{self.name} ({self.url}) \n {self.json}'

# Retrieves the username's watchlist
def fetch_watchlist(username):

    movies = []

    # To manage multiple-page watchlists
    watchlist_page = 1

    while True:

        # Set http request details
        url = f"https://letterboxd.com/{username}/watchlist/page/{watchlist_page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Make http request
        response = requests.get(url, headers=headers, timeout=(5, 10))

        # Break if the page does not exist (end of the watchlist pages)
        if response.status_code != 200:
            break  # Stop if the page doesn't exist

        # Load the html file
        soup = BeautifulSoup(response.text, 'html.parser')
            
        # Get the grid containing all the movies in the page
        grid_list = soup.find_all('ul', class_='grid')

        # Break when no movies are found on the page
        if not grid_list:
            break 

        movies_found_this_page = 0
        
        # Within the grid. each <li> is a movie, and the <div> tag contains the attributes we are interested in
        for grid in grid_list:
            li_items = grid.find_all('li', class_='griditem')
            for li in li_items:
                div = li.find('div', class_='react-component')
                if div:
                    name = div.get('data-item-name')
                    poster = "https://letterboxd.com" + div.get('data-poster-url')
                    url = "https://letterboxd.com" + div.get('data-target-link')
                    json = "https://letterboxd.com" + div.get('data-details-endpoint')

                    movie = Movie(name, poster, url, json)
                    movies.append(movie)
                    movies_found_this_page += 1
                
        # Break if no movies were found on this page
        if movies_found_this_page == 0:
            break

        # Check if there are more pages in the watchlist
        watchlist_page += 1
    return movies

def get_random_movie(movies):
    random_index_instance = qrng(len(movies) - 1)
    random_movie = movies[random_index_instance.random_number]
    
    return print(f'\n\nYour random movie is: {random_movie.name} ({random_movie.url}). \n\nIt was chosen using this quantum circuit:\n{random_index_instance.qc.draw('text')}')

def main():
    # Ask user for username
    username = input('Enter your Letterboxd username: ')

    # Start spinner
    stop_spinner = threading.Event()
    print()
    spinner_thread = threading.Thread(target=spinner, args=("Working on your watchlist...", stop_spinner))
    spinner_thread.start()

    # Show all movies in the watchlist for the given username
    movies = fetch_watchlist(username)

    for movie in movies:
        print(movie.json)

    # Uncomment this section if want to see the user's entire watchlist
    #print(f'\n\nThis is your watchlist ({len(movies)} movies in total):')
    #for movie in movies:
    #   print(f"- {movie.name} ({movie.url})")

    # Output a random movie
    random_mov = get_random_movie(movies)

    # Stop spinner
    stop_spinner.set()
    spinner_thread.join()
    print('\r' + ' ' * 80 + '\r', end='')  # Clear the spinner line

if __name__ == '__main__':
    main()



