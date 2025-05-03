# Goodreads Agent

An example AI Agent using the Goodreads dataset from Kaggle

## Project Setup

This project is set up with the following structure:

```text
goodreads-agent/
├── venv/                    # Python virtual environment
├── data/                    # Dataset directory
│   └── books.csv            # Goodreads books dataset
├── requirements.txt         # Project dependencies
├── goodreads_data.py        # Main data processing module
├── goodreads_analysis.ipynb # Jupyter notebook for analysis
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Dependencies

The project uses the following main dependencies:

- pandas (2.0.0) - For data manipulation and analysis
- numpy (1.24.3) - For numerical operations
- kaggle (1.5.13) - For downloading the dataset
- jupyter (1.0.0) - For interactive data analysis
- matplotlib (3.7.1) - For data visualization
- seaborn (0.12.2) - For statistical data visualization

## Getting Started

1. Clone this repository

2. Set up the Python environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Kaggle Authentication Setup:
   - Create a Kaggle account if you haven't already
   - Go to your Kaggle account settings (<https://www.kaggle.com/account>)
   - Create an API token (this will download a `kaggle.json` file)
   - Place the `kaggle.json` file in `~/.kaggle/` directory
   - Ensure the file has appropriate permissions: `chmod 600 ~/.kaggle/kaggle.json`

4. Download the Dataset:

   ```bash
   kaggle datasets download jealousleopard/goodreadsbooks -p data --unzip
   ```

## Data Analysis

The project includes a Jupyter notebook (`goodreads_analysis.ipynb`) for interactive data analysis. To start analyzing the data:

1. Start the Jupyter notebook server:

   ```bash
   jupyter notebook
   ```


2. Open `goodreads_analysis.ipynb` in your browser
3. Run the cells using Shift+Enter

The notebook includes templates for various analyses:

- Rating distribution
- Popular authors
- Page count analysis
- Publication trends
- Language distribution
- Publisher analysis

## Usage

The main module `goodreads_data.py` contains functions for loading and processing the Goodreads dataset. For interactive data analysis, use the Jupyter notebook.

## Project Status

The project has been set up with:

- Basic environment and dependencies
- Downloaded Goodreads dataset
- Data processing module
- Interactive Jupyter notebook for analysis

Ready for data analysis and visualization.
