CREATE TABLE documents (
    doc_id TEXT PRIMARY KEY,
    doc_path TEXT,
    summary TEXT,
    ext TEXT,
    doc_length INTEGER
);

CREATE TABLE raw_terms (
    doc_id TEXT,
    term TEXT,
    count INTEGER,
    FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
);

CREATE TABLE terms (
    term TEXT PRIMARY KEY,
    term_definition TEXT,
    total_count INTEGER
);
