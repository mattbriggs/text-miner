import nltk

def download_nltk_packages():
    # List of NLTK packages to download
    packages = [
        'vader_lexicon',   # For SentimentIntensityAnalyzer
        'punkt',           # Often used for tokenizing text into sentences
        'averaged_perceptron_tagger',  # For POS tagging
        'stopwords'        # Commonly used stop words
    ]

    # Download each package
    for package in packages:
        nltk.download(package)

if __name__ == "__main__":
    print("Downloading required NLTK packages...")
    download_nltk_packages()
    print("NLTK packages downloaded successfully.")
