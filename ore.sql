-- Create the documents table with doc_id and doc_path
CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    doc_path TEXT,
    summary TEXT,
    doc_length INTEGER
);

-- Create the terms table with doc_id and term
-- This table has a foreign key reference to the documents table
CREATE TABLE IF NOT EXISTS terms (
    doc_id TEXT,
    term TEXT,
    FOREIGN KEY (doc_id) REFERENCES documents (doc_id)
);
