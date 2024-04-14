from moviepy.editor import VideoFileClip

def extract_audio(input_video_path, output_audio_path):
    try:
        # Load the video clip
        video_clip = VideoFileClip(input_video_path)

        # Extract the audio from the video
        audio_clip = video_clip.audio

        # Save the audio to the specified output path
        audio_clip.write_audiofile(output_audio_path)

        print(f"Audio extracted successfully to {output_audio_path}")

        # Close the video and audio clips
        video_clip.close()
        audio_clip.close()
    except Exception as e:
        print(f"Error: {e}")

# Example usage
input_video_path = "video/v1.mkv"
output_audio_path = "music/1.mp3"

extract_audio(input_video_path, output_audio_path)
