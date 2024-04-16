# Text Miner

Text Miner is a Python application designed to process a text corpus stored in a SQLite database. The application extracts data from a database that contains corpus, generates summaries, and identifies the top fifty terms within the documents. The tool can be used for quick content analysis and data extraction from large text collections.

## Version
0.0.1 | Matt Briggs

## Features
- Load and read documents from a SQLite database.
- Summarize texts using custom algorithms.
- Extract and list top terms from the documents.

## Prerequisites
Before you start using Text Miner, ensure you have the following installed:
- Python 3.x
- SQLite3
- Required Python packages:
  - `yaml`
  - `sqlite3`
  - `os`

## Installation

To set up Text Miner on your local machine, follow these steps:

1. Clone the repository or download the source code.
2. Navigate to the directory containing the project files.
3. Create a virtual environment. On a PC:
    ```PowerShell
    virtualenv ENV
    ENV\Scripts\activate
    ```
4. Install the required Python packages in the virtual environment.
   ```PowerShell
   pip install -r requirements.txt
   ```
5. Install the Natural Language Toolkit data dependences in the virtual environment.
   ```PowerShell
   python ./setnltk.py
   ```

## Corpus stored in SQLite Database

Before you use Text Miner, you will need to create a corpus using the
[Text Collector](https://github.com/mattbriggs/text-collector) project. For an explanation of the database schema, see [Source corpus](docs/corpus.md)

## Configuration

Before running the application, you need to configure it:

1. Open the `config.yml` file.
2. Set the paths for `corpusdb` and `reportdb` to your SQLite database files.

## Usage

To run the application, execute the following command in the PowerShell:

```PowerShell
ENV\Scripts\activate
python ./mine.py
```

The application will:

- Connect to the database specified in the `config.yml`.
- Fetch documents, summarize them, and extract terms.
- Output the results to the target database.

## Common modules

- `createdatabase.py`: Defines the schema and functions for initializing the database.
- `terms.py`: Contains functions to extract terms from the documents.
- `summary.py`: Provides the summarization algorithm.

## Text miner

Text miner is intended to work as extensible text measurement platform. You can add additional modules and connect them to the miner so that you can produce additional measurements, extract features in the content, and perform other text analysis functions.

## Contributing

Contributions to Text Miner are welcome. Please submit your contributions via pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.