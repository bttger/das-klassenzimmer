import math
from typing import List


def split_transcript(transcript, max_length=60):
    words = transcript.split()
    chunks = []
    current_chunk = []

    for word in words:
        if len(" ".join(current_chunk + [word])) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time


def write_subtitle_file(directory, segments: List[str], audio_duration_secs: float):
    subtitle_file = "subtitles.srt"
    text = ""
    segment_duration = audio_duration_secs / len(segments)
    for index, segment in enumerate(segments):
        segment_start_time = index * segment_duration
        segment_end_time = (index + 1) * segment_duration
        segment_start = format_time(segment_start_time)
        segment_end = format_time(segment_end_time)
        text += f"{str(index+1)}\n"
        text += f"{segment_start} --> {segment_end}\n"
        text += f"{segment}\n"
        text += "\n"

    path = f"{directory}/{subtitle_file}"
    f = open(path, "w")
    f.write(text)
    f.close()

    return path


if __name__ == "__main__":
    # Example usage
    # load the script from the file
    with open(
        'generated_content/"Inboard Brakes: Innovation or Costly? 🤔🔗"/cleaned_video_script.txt',
        "r",
    ) as f:
        transcript = f.read()

    chunks = split_transcript(transcript)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")
