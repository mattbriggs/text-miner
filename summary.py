''' Wordcount
    Count the number of words in a topic.

    Input: Ingests a file and count the number of words.
    Output: the number of words.

'''

import re
import nltk
import heapq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure the necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    """
    Remove square brackets, extra spaces, special characters, and digits from text.
    """
    # Removing square brackets and excessive whitespace
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Removing special characters and digits, preserving only letters
    cleaned_text = re.sub('[^a-zA-Z]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text

def calculate_word_frequencies(text):
    """
    Calculate the frequency of each word in the text, excluding stopwords.
    """
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    frequencies = {}
    
    for word in words:
        if word not in stop_words:
            frequencies[word] = frequencies.get(word, 0) + 1

    return frequencies

def score_sentences(sentences, word_frequencies):
    """
    Score sentences based on word frequencies, considering only sentences with less than 30 words.
    """
    sentence_scores = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        sentence_length = len(words)
        if sentence_length < 30:
            for word in words:
                if word in word_frequencies:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    return sentence_scores

def summarize_text(text):
    """
    Generate a summary by identifying the most relevant sentences.
    """
    # Clean the text and split into sentences
    formatted_text = clean_text(text)
    sentences = sent_tokenize(text)

    # Calculate word frequencies and normalize them
    word_frequencies = calculate_word_frequencies(formatted_text)
    max_frequency = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    # Score the sentences based on the normalized frequencies
    sentence_scores = score_sentences(sentences, word_frequencies)
    
    # Extract the top 7 sentences as the summary
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences).replace("\n", " ").replace("#", "").replace("|", "")
    
    return summary

def main():
    """
    Example usage of the text summarization function.
    """
    input_text = """Your input text here."""
    print("Generated Summary:", summarize_text(input_text))

if __name__ == "__main__":
    main()
