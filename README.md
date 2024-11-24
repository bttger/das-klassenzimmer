# das-klassenzimmer

## Tasks

## Scraping

- [x] Find appropriate subreddits (which languages? english, german, french, spanish?)
- [ ] Write playwright script to scrape the linked articles and the comments periodically
  - [ ] Navigate to each reddit post
  - [ ] Scrape the article
  - [ ] Scrape the reddit comments
  - [ ] Preprocess/Clean the article's HTML body to plain text and data (text, date, title, comments+usernames+datetime)
- [ ] Write (or add to) script Azure OpenAI wrapper and test the connection to the hackatum instance
- [ ] Set up RAG DB for a vector index
  - [ ] Use OpenAI API wrapper for the embeddings to create a vectors for each article and related comments
  - [ ] Track reddit post id, article id, comment id in database
  - [ ] Trigger video generation once virality threshold is reached (e.g. 1000 upvotes or 100 comments)

## Video Generation

- [ ] Write a system prompt for script generation
  - [ ] hook for the viewer, exaggeration, reformulation, etc.
  - [ ] give context for the topic (article plus comments)
  - [ ] explain the problem / the analysis using the article and reddit comments
- [ ] TTS for the script
- [ ] Scrape google images for fitting images to original article
- [ ] Generate video with script, images, and TTS using pymovie

- [ ] Write script with query to read data from DB
- [ ] Write a system prompt for image generation

## migrations

```
sqlite3 news.db < migrations.sql
```

## Development

Set up the Python virtual environment and run the scraping:

```bash
cd ./scraping
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the scraping
python scrape.py
```

## FFMPEG commands

```bash
# merge video and TTS audio
ffmpeg -i video.mp4 -i tts_audio.mp3 -c:v copy -c:a aac -itsoffset 0.5 output_video.mp4

# speed up video
ffmpeg -i output_video.mp4 -filter_complex "[0:v]setpts=0.8*PTS[v];[0:a]atempo=1.25[a]" -map "[v]" -map "[a]" output_video_sped_up.mp4

# merge video and default background music with reduced volume and the -shortest option
ffmpeg -i output_video_sped_up.mp4 -i bg_music.mp3 -filter_complex "[0:a]volume=1[a1];[1:a]volume=0.2[a2];[a1][a2]amix=inputs=2[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -ac 2 -shortest final_video.mp4
```
