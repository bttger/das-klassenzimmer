import os
import moviepy as mp
import moviepy.video.fx as vfx

content_path = 'generated_content/"Mercedes\' New Brakes: Worth It? 🚗🔍 Check Bio!"'
audio_save_path = os.path.join(content_path, "audio.mp3")
images_save_path = os.path.join(content_path, "images")
# get images from the images_save_path, sort the name by the number in the front
image_files = sorted(
    [os.path.join(images_save_path, f) for f in os.listdir(images_save_path)],
    key=lambda x: int(x.split("-")[0].split("/")[-1]),
)

audio_length = 0
audio = mp.AudioFileClip(audio_save_path)
audio_length = audio.duration

image_duration = audio_length / len(image_files)
transition_duration = image_duration / 0.4

clips = []
for image_path in image_files:
    img_clip = mp.ImageClip(image_path, duration=image_duration)
    clips.append(img_clip)

video = mp.concatenate_videoclips(clips, method="compose")
video = video.with_audio(audio)
video.write_videofile(
    os.path.join(content_path, "video.mp4"), codec="libx264", fps=24, audio_codec="aac"
)

print("Audio Length:", audio_length)
