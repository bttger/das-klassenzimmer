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
