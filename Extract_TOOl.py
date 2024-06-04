from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

def extract_movie_metadata(file_path):
    parser = createParser(file_path)
    metadata = extractMetadata(parser)

    movie_metadata = {}
    if metadata:
        for item in metadata.exportPlaintext():
            key, value = item.split(':', 1)
            movie_metadata[key.strip()] = value.strip()
    
    return movie_metadata

# Example usage
movie_path = 'path/to/your/movie/file.mp4'
metadata = extract_movie_metadata(movie_path)
print(metadata)