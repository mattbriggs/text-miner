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

CREATE TABLE kwic (
    term TEXT,
    doc_id TEXT,
    line_no INTEGER,
    context TEXT,
    possent REAL,
    nuesent REAL,
    negsent REAL,
    compsent REAL,
    FOREIGN KEY (term) REFERENCES terms (term),
    FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
);

CREATE VIEW unique_terms AS -- Changed to 'AS' for creating view
    SELECT DISTINCT term FROM raw_terms ORDER BY term;