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
