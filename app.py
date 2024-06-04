from flask import Flask, render_template, send_file, send_from_directory,request,redirect
from IMDBBot import get_imdb_score, extract_meaningful_title, update_imdb_score, extract_all_part_with_mean, contains_only_one_word, contains_special_characters
import os
import json

app = Flask(__name__)

SUB_FOLDER = "D:/Projects/Python/TEST/NOMEAN/MovieStream/static/subtitles"
ROOT_FOLDER = "D:/Projects/Python/TEST/NOMEAN/MovieStream"
VIDEO_FOLDER = 'D:/Projects/Python/TEST/NOMEAN/MovieStream/Videos'

class Video:
    def __init__(self, title, description, thumbnail, path):
        self.title = title
        self.description = description
        self.thumbnail = thumbnail
        self.path = path

@app.route('/Home')
def custom_dns_route():
    # Redirect to the actual route you want to show
    return redirect('/')

@app.route('/')
def index():
    query = request.args.get('query', '').lower()  # Default to empty string if query is not provided

    videos = get_videos()
    
    # Convert each Video object to a dictionary
    video_dicts = [video.__dict__ for video in videos]
    
    # Pass the query variable to the template context
    return render_template('index.html', query=query, videos=video_dicts)

@app.route('/video/<path:video_path>')
def stream_video(video_path):
    return send_file(os.path.join(VIDEO_FOLDER, video_path))

@app.route('/subtitles/<path:filename>')
def subtitles(filename):
    return send_from_directory('path/to/subtitles/directory', filename)

@app.route('/watch/<path:video_path>')
def watch(video_path):
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    
    # Load movie information from JSON file
    with open(os.path.join(ROOT_FOLDER,'data/movies.json'), 'r') as file:
        movies = json.load(file)
    
    # Find the movie corresponding to the video path
    selected_movie = None
    for movie in movies:
        if movie['title'] == video_filename:
            selected_movie = movie
            break
    
    if selected_movie:
        genres = ', '.join(selected_movie['genres'])
        selected_movie['title'] = extract_meaningful_title(selected_movie['title'])
        if selected_movie['title'] == video_filename and contains_only_one_word(selected_movie['title']) and contains_special_characters(selected_movie['title']):
            selected_movie['title'] = extract_all_part_with_mean(selected_movie['title']) if not None else selected_movie['title']
        
        if len(selected_movie['imdb_score'])<1:
            imdb_score = get_imdb_score(selected_movie['title'])
            if imdb_score is not None:
                
                update_imdb_score(video_filename,imdb_score,ROOT_FOLDER)
                
                selected_movie['imdb_score'] = imdb_score
                
        return render_template('watch.html', video_path=video_path, subtitles_path=selected_movie['subtitles_path'],
                               movie_title=selected_movie['title'], 
                               movie_description=selected_movie['description'],
                               release_date=selected_movie['release_date'], 
                               genres=genres, 
                               director=selected_movie['director'],
                               imdb_score=selected_movie['imdb_score'])
    else:
        return 'Movie not found'

def get_videos():
    with open(os.path.join(ROOT_FOLDER,'data/movies.json'), 'r') as file:
        movies = json.load(file)
    videos = []
    for root, dirs, files in os.walk(VIDEO_FOLDER):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv', 'webm')):
                title = os.path.splitext(file)[0]  # Extract video title from filename
                for movie in movies:
                    if movie['title'] == title:
                        selected_movie = movie
                        break
                    
                if selected_movie:
                    description = selected_movie['description']
                    thumbnail = "thumbnails/" + title + ".jpg"  # Assuming thumbnails are stored in a 'thumbnails' folder
                    path = os.path.relpath(os.path.join(root, file), VIDEO_FOLDER)
                    videos.append(Video(title, description, thumbnail, path))
    return videos

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)