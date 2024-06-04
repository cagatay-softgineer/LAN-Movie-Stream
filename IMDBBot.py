import requests
from bs4 import BeautifulSoup
import re
import os
import json


def update_imdb_score(movie_title, imdb_score, ROOT_FOLDER):
    # Read contents of movies.json
    movies_json_path = os.path.join(ROOT_FOLDER, 'data/movies.json')
    with open(movies_json_path, 'r') as file:
        movies_data = json.load(file)

    # Find the entry for the selected movie
    for movie in movies_data:
        if movie['title'] == movie_title:
            # Update imdb_score field
            movie['imdb_score'] = imdb_score
            break
    # Write updated contents back to movies.json
    with open(movies_json_path, 'w') as file:
        json.dump(movies_data, file, indent=4)

def extract_meaningful_title(movie_title):
    # Use regular expression to extract the meaningful part of the title
    match = re.match(r'(.+?) \(\d{4}\)', movie_title)
    if match:
        return match.group(1)
    return movie_title


def extract_all_part_with_mean(movie_title):
    
       # Define regular expression pattern to match unwanted parts
    patterns_to_remove = [
        r'\bS\d{2}E\d{2}\b',   # Match season and episode patterns like S01E01
        r'\b\d+p\b',           # Match resolution patterns like 1080p
        r'\bBluRay\b',         # Match specific source patterns like BluRay
        r'\bDDP\b',            # Match audio codec patterns like DDP
        r'\bH\.265\b',         # Match video codec patterns like H.265
        r'-\w+',               # Match patterns like -EDGE2020
        r'\b\d+\.\d+\b',       # Match patterns like 5.1
        r'\bBMO\b',             # Match specific substring like BMO
        r'\bObsidian\b',             # Match specific substring like BMO
        r'\bTogether.Again\b',             # Match specific substring like BMO
        r'\bWizard.City\b'             # Match specific substring like BMO
    ]

    pattern = re.compile('|'.join(patterns_to_remove))

    # Remove unwanted parts from the title string
    clean_title = re.sub(pattern, "", movie_title)
    # Remove consecutive periods
    clean_title = re.sub(r'\.{2,}', '.', clean_title)
    
    clean_title = clean_title.replace(".", " ")
    print(clean_title)
    return clean_title if clean_title != movie_title else None

def contains_only_one_word(s):
    # Split the string by spaces
    words = s.split()

    # Check if the resulting list contains only one element
    return not len(words) < 2

def contains_special_characters(s):
    # Define a set of special characters to check for
    special_characters = {'.', ',', '-', '_'}

    # Check if any of the special characters are present in the string
    return any(char in special_characters for char in s)


def get_imdb_score(movie_title):
    # Construct IMDb search URL
    search_url = f"https://www.imdb.com/find?q={movie_title}&ref_=nv_sr_sm"

    # Send HTTP GET request
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    
    # Parse HTML response
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all search results
    results = soup.find_all("li", class_="find-result-item")
    
    if results:
        # Get the URL of the first movie page
        first_result = results[0]
        movie_url = first_result.find("a")["href"]
        
        # Send HTTP GET request to the movie page
        response = requests.get(f"https://www.imdb.com{movie_url}", headers=headers)

        # Parse HTML response
        soup = BeautifulSoup(response.content, 'html.parser')

        
        
        # Find IMDb score
        score_element = soup.find("span", class_="sc-bde20123-1 cMEQkK")
        if score_element:
            return score_element.text

    return None