import nltk
from nltk import word_tokenize, pos_tag
from nltk.chunk import RegexpParser

# Download necessary NLTK data files
# nltk.download()


def split_transcript_into_phrases(transcript):
    # Define chunk grammar for noun phrases (NP) and verb phrases (VP)
    grammar = r"""
        NP: {<DT|JJ|NN.*>+}   # Noun phrase
        VP: {<VB.*><NP|PP|CLAUSE>+$}   # Verb phrase
    """
    chunk_parser = RegexpParser(grammar)

    # Tokenize sentences
    sentences = nltk.sent_tokenize(transcript)

    # Process each sentence
    chunks = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)  # Tokenize sentence into words
        tagged = pos_tag(tokens)  # Part-of-speech tagging
        tree = chunk_parser.parse(tagged)  # Parse into NP and VP chunks

        # Extract NP and VP chunks
        for subtree in tree.subtrees(filter=lambda t: t.label() in {"NP", "VP"}):
            phrase = " ".join(word for word, tag in subtree.leaves())
            chunks.append((subtree.label(), phrase))

    return chunks


def split_transcript_into_phrases_simple(transcript):
    # Simplified chunk grammar for longer phrases
    grammar = r"""
        CHUNK: {<DT|JJ|NN.*|PRP.*|RB.*|VB.*|IN|CC>+}  # Chunk sequences of words with relevant tags
    """
    chunk_parser = RegexpParser(grammar)

    # Tokenize sentences
    sentences = nltk.sent_tokenize(transcript)

    # Process each sentence
    chunks = []
    for sentence in sentences:
        tokens = word_tokenize(sentence)  # Tokenize sentence into words
        tagged = pos_tag(tokens)  # Part-of-speech tagging
        tree = chunk_parser.parse(tagged)  # Parse into chunks

        # Extract chunks
        for subtree in tree.subtrees(filter=lambda t: t.label() == "CHUNK"):
            phrase = " ".join(word for word, tag in subtree.leaves())
            chunks.append(phrase)

    return chunks


# Example usage

# load the script from the file
with open(
    'generated_content/"Inboard Brakes: Innovation or Costly? 🤔🔗"/cleaned_video_script.txt',
    "r",
) as f:
    transcript = f.read()

phrases = split_transcript_into_phrases_simple(transcript)

# Output the phrases
print(type(phrases), type(phrases[0]))
for phrase in phrases:
    print(phrase)

for label, phrase in phrases:
    print(f"{label}: {phrase}")
