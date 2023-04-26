# GPT-based Automated Web Scraper

The GPT-based Universal Web Scraper is an MVP project that aims to provide a web scraping solution using GPT models to interact with users and generate scraper code based on user requirements, website structure analysis, and network traffic analysis. The purpose of this project is to simplify the process of web scraping by leveraging the capabilities of GPT models and various web scraping libraries.

## Documentation

Detailed information about the project can be found in the following documents:

- [Technical Design Document (TDD)](tdd.md): The TDD provides a comprehensive overview of the system architecture, component design, and implementation details.
- [Product Requirements Document (PRD)](prd.md): The PRD outlines the features, functionality, and requirements of the GPT-based Universal Web Scraper.

## Main Components

1. `gpt_interaction`: Handles communication with the GPT model and manages user interaction to gather scraping requirements.
2. `scraper_generation`: Generates scraper code based on the results of the website structure analysis and user requirements.
3. `url_preprocessing`: Handles URL validation, normalization, and cleaning tasks.
4. `website_analysis`: Analyzes website DOM, identifies relevant elements, and detects APIs through network traffic analysis for data extraction.
5. `data_extraction`: Executes the generated scraper and extracts data from the target website.

## Installation

To install the project dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage

Currently the project is still under development. This section will be updated once the project is ready for use.

## Testing

Currently the project is still under development. This section will be updated once the project is ready for use.

## Contributing

We welcome contributions to improve the GPT-based Universal Web Scraper. Please feel free to submit issues, feature requests, and pull requests on the repository.