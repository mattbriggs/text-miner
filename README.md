# Text Miner

Text-Miner is a Python application designed to process a text corpus stored in a SQLite database. The application extracts data from the corpus, generates summaries, and identifies the top fifty terms within the documents. Developed by Matt Briggs, this tool is useful for quick content analysis and data extraction from large text collections.

## Version
0.0.1

## Features
- Load and read documents from a SQLite database.
- Summarize texts using custom algorithms.
- Extract and list top terms from the documents.

## Prerequisites
Before you start using Text-Miner, ensure you have the following installed:
- Python 3.x
- SQLite3
- Required Python packages:
  - `yaml`
  - `sqlite3`
  - `os`

## Installation

To set up Text-Miner on your local machine, follow these steps:
1. Clone the repository or download the source code.
2. Navigate to the directory containing the project files.
3. Install the required Python packages:
   ```bash
   pip install pyyaml sqlite3
   ```
4. Set up the SQLite database using the schema provided in the `createdatabase` module.

## Configuration
Before running the application, you need to configure it:
1. Open the `config.yml` file.
2. Set the paths for `corpusdb` and `reportdb` to your SQLite database files.

## Usage

To run the application, execute the following command in the terminal:
```bash
python text-miner.py
```

The application will:
- Connect to the database specified in the `config.yml`.
- Fetch documents, summarize them, and extract terms.
- Output the results to the console.

## Modules

- `createdatabase.py`: Defines the schema and functions for initializing the database.
- `terms.py`: Contains functions to extract terms from the documents.
- `summary.py`: Provides the summarization algorithm.

## Contributing
Contributions to Text-Miner are welcome. Please submit your contributions via pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Matt Briggs