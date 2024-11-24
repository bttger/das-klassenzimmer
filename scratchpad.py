import os
import moviepy as mp
import moviepy.video.fx as vfx
from PIL import Image, ImageFilter
from moviepy import CompositeVideoClip

content_path = 'generated_content/"Mercedes\' Go-Kart Brakes: Cool or Costly? 🚗🔗 Check the Link!"'
audio_save_path = os.path.join(content_path, "audio.mp3")
images_save_path = os.path.join(content_path, "images")
# get images from the images_save_path, sort the name by the number in the front
image_files = sorted(
    [os.path.join(images_save_path, f) for f in os.listdir(images_save_path)],
    key=lambda x: int(os.path.basename(x).split("-")[0].split("/")[-1]),
)

# Create slide transition effect
def slide_transition(clip1, clip2, duration):
    # Slide the first clip out to the left
    clip1_slide = clip1.with_position(lambda t: (-clip1.w * t / duration, 0)).with_duration(duration)
    # Slide the second clip in from the right
    clip2_slide = clip2.with_position(lambda t: (clip2.w * (1 - t / duration), 0)).with_duration(duration)
    # Overlay both clips during the transition
    return CompositeVideoClip([clip1_slide, clip2_slide], size=clip1.size)


# resize images to 1080x1920, without changing the aspect ratio
for image_path in image_files:
    original_img = Image.open(image_path).convert("RGB")
    width, height = original_img.size
    if width > height:
        # Landscape: scale width to 1080 pixels
        new_width = 1080
        new_height = int((new_width / width) * height)
    else:
        # Portrait or square: scale height to 1920 pixels
        new_height = 1920
        new_width = int((new_height / height) * width)

    resized_img = original_img.resize((new_width, new_height))

    blurred_img = original_img.resize((1080, 1920)).filter(ImageFilter.GaussianBlur(20))
    paste_position = (1080 - resized_img.width) // 2, (1920 - resized_img.height) // 2
    blurred_img.paste(resized_img, paste_position)
    blurred_img.save(image_path)


audio_length = 0
audio = mp.AudioFileClip(audio_save_path)
audio_length = audio.duration / 5

image_duration = audio_length / len(image_files)
transition_duration = 0.3

clips = []
for image_path in image_files:
    img_clip = mp.ImageClip(image_path, duration=image_duration)
    clips.append(img_clip)

# Add transitions between clips
final_clips = []
for i in range(len(clips) - 1):
    final_clips.append(clips[i])
    transition = slide_transition(clips[i], clips[i + 1], transition_duration)
    final_clips.append(transition)

# Append the last clip (no transition after it)
final_clips.append(clips[-1])

# Concatenate all clips
video = mp.concatenate_videoclips(final_clips, method="compose")

#video = video.with_audio(audio)
video.write_videofile(
    os.path.join(content_path, "video.mp4"), codec="libx264", fps=24, audio_codec="aac"
)

print("Audio Length:", audio_length)
