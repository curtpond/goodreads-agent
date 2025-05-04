-- Create a database for the Goodreads project
CREATE DATABASE IF NOT EXISTS goodreads_db;
USE DATABASE goodreads_db;

-- Create a schema for our tables
CREATE SCHEMA IF NOT EXISTS books;
USE SCHEMA books;

-- Create the books table
CREATE OR REPLACE TABLE books (
    book_id INTEGER,
    title VARCHAR(500),
    isbn VARCHAR(13),
    isbn13 VARCHAR(13),
    average_rating FLOAT,
    num_pages INTEGER,
    ratings_count INTEGER,
    text_reviews_count INTEGER,
    publication_date DATE,
    publisher_id INTEGER,
    language_code VARCHAR(10),
    data_quality_score FLOAT,
    processed_timestamp TIMESTAMP_NTZ,
    PRIMARY KEY (book_id)
);

-- Create the authors dimension table
CREATE OR REPLACE TABLE authors (
    author_id INTEGER,
    author_name VARCHAR(255),
    PRIMARY KEY (author_id)
);

-- Create the publishers dimension table
CREATE OR REPLACE TABLE publishers (
    publisher_id INTEGER,
    publisher_name VARCHAR(255),
    PRIMARY KEY (publisher_id)
);

-- Create the book_authors mapping table (for many-to-many relationship)
CREATE OR REPLACE TABLE book_authors (
    book_id INTEGER,
    author_id INTEGER,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Create a file format for CSV ingestion
CREATE OR REPLACE FILE FORMAT csv_format
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')
    FIELD_OPTIONALLY_ENCLOSED_BY = '"';

-- Comments for documentation
COMMENT ON TABLE books IS 'Main books table containing book metadata and metrics';
COMMENT ON TABLE authors IS 'Dimension table for book authors';
COMMENT ON TABLE publishers IS 'Dimension table for book publishers';
COMMENT ON TABLE book_authors IS 'Mapping table for book-author relationships';

-- Add column comments
COMMENT ON COLUMN books.data_quality_score IS 'Score (0-100) indicating the completeness and validity of the book record';
COMMENT ON COLUMN books.processed_timestamp IS 'Timestamp when the record was processed for Snowflake ingestion';
