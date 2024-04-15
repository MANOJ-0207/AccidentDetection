from moviepy.editor import VideoFileClip
from src import constants

def convert_to_browser_friendly_mp4(file_name):
    input_file_path = constants.OUTPUT_VIDEOS_PATH + "/Singly_Processed_Videos/ProcessedVideos/Processed" + file_name
    output_file_path = constants.OUTPUT_VIDEOS_PATH + "/Singly_Processed_Videos/BrowserVideos/Browser" + file_name
    clip = VideoFileClip(input_file_path)
    clip.write_videofile(output_file_path, codec='libx264', fps=30, preset='ultrafast')