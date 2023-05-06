# GPT-based Automated Web Scraper

![GPT based automated webscrapper](https://cdn.discordapp.com/attachments/984632500875821066/1104363425439698944/analyticsynthetic_Small_cute_mining_robot_with_large_eyes_5501ffb9-ea08-4dfc-b04d-9623f7c4481a.png "GPT based automated webscrapper")

The GPT-based Universal Web Scraper is an MVP project that aims to provide a web scraping solution using GPT models to interact with users and generate scraper code based on user requirements, website structure analysis, and network traffic analysis. The purpose of this project is to simplify the process of web scraping by leveraging the capabilities of GPT models and various web scraping libraries.

**Note**: The GPT prompt for analyzing API calls is still in progress and may not return accurate results at this time. We are working on improving the prompt to provide better analysis results.

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

Next, copy the `config.json.example` file to `config.json` and enter your GPT-4 API key in the `gpt4` section:

```json
{
  "gpt4": {
    "api_key": "your-api-key-here"
  }
}
```

## Usage

You can analyze the network traffic of websites using the NetworkAnalyzer class provided in the `./website_analysis/network_analysis.py` file. Here's an example of how to use the class:

```python

from website_analysis.network_analysis import NetworkAnalyzer

# URL of the website to analyze
url = "https://www.example.com"

# User requirements for the data extraction (currently not used)
user_requirements = {}

# Create a NetworkAnalyzer instance
analyzer = NetworkAnalyzer(url, user_requirements)

# Analyze the website
analysis_results = analyzer.analyze_website()

# Print the analysis results
print(analysis_results)
```

You can also analyze multiple websites at once using the `analyze_websites` function provided in the same file. Just pass a list of website URLs as an argument:

```python

from website_analysis.network_analysis import analyze_websites

# List of website URLs to analyze
websites = [
    "https://www.example1.com",
    "https://www.example2.com",
    "https://www.example3.com"
]

# Analyze the websites
results = analyze_websites(websites)

# Print the analysis results
print(results)
```


## Testing

Currently the project is still under development. This section will be updated once the project is ready for use.

## Contributing

We welcome contributions to improve the GPT-based Universal Web Scraper. Please feel free to submit issues, feature requests, and pull requests on the repository.