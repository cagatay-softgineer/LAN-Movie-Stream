import os
import subprocess

# Specify the full path to ffmpeg.exe
FFMPEG_PATH = 'D:\Projects\Python\TEST/NOMEAN\MovieStream/ffmpeg.exe'

VIDEO_FOLDER = 'D:\Projects\Python\TEST/NOMEAN\MovieStream\Videos'
THUMBNAIL_FOLDER = 'D:\Projects\Python\TEST/NOMEAN\MovieStream\static/thumbnails'
THUMBNAIL_WIDTH = 160  # Width of the thumbnail (in pixels)

def generate_thumbnail(video_path, thumbnail_path):
    try:
        # Use subprocess to execute ffmpeg command
        command = [FFMPEG_PATH,"-n" , '-i', video_path, '-ss', '00:00:05', '-vframes', '1', '-vf', f'scale={THUMBNAIL_WIDTH}:-1', thumbnail_path]
        subprocess.run(command, check=True)
        print(f"Generated thumbnail for: {video_path}")
    except Exception as e:
        print(f"Error generating thumbnail for {video_path}: {str(e)}")

def generate_thumbnails():
    if not os.path.exists(THUMBNAIL_FOLDER):
        os.makedirs(THUMBNAIL_FOLDER)

    for root, dirs, files in os.walk(VIDEO_FOLDER):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv', 'webm')):
                video_path = os.path.join(root, file)
                thumbnail_name = os.path.splitext(file)[0] + '.jpg'
                thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_name)
                generate_thumbnail(video_path, thumbnail_path)

if __name__ == '__main__':
    generate_thumbnails()