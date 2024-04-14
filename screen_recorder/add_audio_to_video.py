from moviepy.editor import VideoFileClip, AudioFileClip

# Load video and audio clips
video_clip = VideoFileClip("2024-02-04 19-39-16.mp4")
audio_clip = AudioFileClip("music/1.mp3")

# Set the audio of the video clip to the loaded audio clip
video_clip = video_clip.set_audio(audio_clip)

# Write the output video file
video_clip.write_videofile("video/output_video.mp4", codec="libx264", audio_codec="aac")

# Close the video and audio clips
video_clip.close()
audio_clip.close()
