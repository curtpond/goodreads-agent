"""
Data preparation script for Goodreads dataset before Snowflake ingestion.
This script handles data cleaning, transformation, and exports the data in a format
suitable for Snowflake ingestion.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

def load_and_clean_data(input_path: str) -> pd.DataFrame:
    """
    Load and clean the Goodreads dataset.
    
    Args:
        input_path (str): Path to the raw books.csv file
        
    Returns:
        pd.DataFrame: Cleaned dataset ready for Snowflake
    """
    # Load the data
    df = pd.read_csv(input_path)
    
    # Clean column names (remove spaces, standardize)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Convert publication_date to proper datetime
    df['publication_date'] = pd.to_datetime(df['publication_date'])
    
    # Clean text fields
    text_columns = ['title', 'authors', 'publisher']
    for col in text_columns:
        # Remove leading/trailing whitespace
        df[col] = df[col].str.strip()
        # Replace NULL strings with None
        df[col] = df[col].replace(['NULL', 'null', ''], None)
    
    # Ensure numeric fields are proper types
    df['average_rating'] = pd.to_numeric(df['average_rating'], errors='coerce')
    df['num_pages'] = pd.to_numeric(df['num_pages'], errors='coerce')
    df['ratings_count'] = pd.to_numeric(df['ratings_count'], errors='coerce')
    df['text_reviews_count'] = pd.to_numeric(df['text_reviews_count'], errors='coerce')
    
    # Add data quality columns
    df['data_quality_score'] = calculate_quality_score(df)
    df['processed_timestamp'] = datetime.now()
    
    return df

def calculate_quality_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate a data quality score for each row based on completeness and validity.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.Series: Quality scores (0-100) for each row
    """
    # Define weights for different quality aspects
    weights = {
        'has_isbn': 15,
        'has_title': 20,
        'has_author': 20,
        'has_rating': 15,
        'has_publisher': 10,
        'has_language': 10,
        'has_pages': 10
    }
    
    # Calculate individual quality indicators
    quality = pd.DataFrame({
        'has_isbn': df['isbn'].notna() | df['isbn13'].notna(),
        'has_title': df['title'].notna() & (df['title'].str.len() > 0),
        'has_author': df['authors'].notna() & (df['authors'].str.len() > 0),
        'has_rating': df['average_rating'].notna() & (df['average_rating'] > 0),
        'has_publisher': df['publisher'].notna() & (df['publisher'].str.len() > 0),
        'has_language': df['language_code'].notna() & (df['language_code'].str.len() > 0),
        'has_pages': df['num_pages'].notna() & (df['num_pages'] > 0)
    })
    
    # Calculate weighted score
    return (quality * pd.Series(weights)).sum(axis=1)

def prepare_for_snowflake(df: pd.DataFrame, output_dir: str):
    """
    Prepare and save the data in a format suitable for Snowflake ingestion.
    
    Args:
        df (pd.DataFrame): Cleaned dataframe
        output_dir (str): Directory to save the prepared files
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save main books table
    books_df = df.copy()
    books_df['book_id'] = books_df['bookid']  # Standardize ID column name
    books_df = books_df.drop('bookid', axis=1)
    books_df.to_csv(output_path / 'books_for_snowflake.csv', index=False)
    
    # Create authors dimension table (splitting multiple authors)
    authors = (df['authors'].str.split('/')
              .explode()
              .str.strip()
              .dropna()
              .unique())
    authors_df = pd.DataFrame({
        'author_id': range(1, len(authors) + 1),
        'author_name': authors
    })
    authors_df.to_csv(output_path / 'authors_for_snowflake.csv', index=False)
    
    # Create publishers dimension table
    publishers = df['publisher'].dropna().unique()
    publishers_df = pd.DataFrame({
        'publisher_id': range(1, len(publishers) + 1),
        'publisher_name': publishers
    })
    publishers_df.to_csv(output_path / 'publishers_for_snowflake.csv', index=False)

def main():
    # Define paths
    input_path = '../data/books.csv'
    output_dir = 'prepared_data'
    
    # Process the data
    df = load_and_clean_data(input_path)
    prepare_for_snowflake(df, output_dir)
    
    # Print summary statistics
    print(f"Processed {len(df)} books")
    print(f"Data quality score statistics:")
    print(df['data_quality_score'].describe())

if __name__ == '__main__':
    main()
