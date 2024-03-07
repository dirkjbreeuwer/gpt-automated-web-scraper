# Technical Design Document: GPT-based Universal Web Scraper MVP

## 1. System Architecture

The GPT-based universal web scraper MVP will be built using a modular monolithic architecture, with an on-premises deployment. The system will consist of several components that interact with each other using internal APIs and direct connections. The architecture is designed to handle a moderate load and a limited number of websites and users, with a moderate level of fault tolerance and redundancy.

### 1.1. Components

The system will consist of the following components:

1. URL Preprocessing
2. User Requirements Gathering
3. Website Structure Analysis
4. Scraper Generation
5. Data Extraction
6. GPT interactions

### 1.2. Component Interaction

Components will communicate with each other using internal APIs and direct connections, allowing for a clean and standardized interface between components. This will enable loose coupling and easier integration, even within the monolithic application.

### 1.3. Deployment

The MVP will be deployed on-premises to reduce the cost associated with cloud resources and allow for better control over the infrastructure. As the product evolves and gains traction, it can be transitioned to a cloud platform to take advantage of the scalability and managed services it offers.


## 2. Component Design

In this section, we've detailed the design and functionality of each component of the GPT-based Universal Web Scraper MVP. The system is composed of five main components:

* **URL Preprocessing** : Handles URL validation, normalization, and cleaning tasks. 
* **User Requirements Gathering** : This module facilitates natural language interaction for users to specify data extraction goals and converts their input into predefined formats for efficient processing by subsequent components.
* **Website Structure Analysis** : Analyzes the website's DOM, identifies relevant elements, and detects APIs through network traffic analysis for data extraction. 
* **Scraper Generation** : Generates scraper code based on the results of the Website Structure Analysis and user requirements. 
* **Data Extraction** : Executes the generated scraper and extracts the data from the target website.

### 2.1. URL Preprocessing

The URL Preprocessing component will be organized into a module with one primary class and helper functions. The class will handle URL validation, normalization, and cleaning tasks.

- Input: Raw URL string
- Output: Cleaned and normalized URL

Libraries such as urllib (Python) or java.net.URL (Java) can be used for URL manipulation and validation. This component should handle various URL formats and edge cases, such as query parameters, URL encoding, and internationalized domain names.

### 2.2 User Requirements Gathering

The objective of this module is to enable users to specify their data extraction requirements using natural language and transform their input into predefined formats for seamless processing by other components in the system.

**Input** :

* User's natural language input describing data extraction requirements
* Examples of the desired output data structure provided by the user

**Output** :

* Predefined formats for website processing keywords and API processing keywords, derived from user requirements

**Classes and Methods** :

*Class*: `UserRequirementsGatherer`

* Methods:

* `__init__(self, user_input, example_output)`: Initializes the class with user input and example output 
* `process_user_input(self)`: Processes the user's natural language input and extracts relevant data extraction requirements 
* `generate_processing_keywords(self)`: Transforms the extracted requirements into predefined website and API processing keywords 
* `get_processing_keywords(self)`: Returns the generated processing keywords for website and API processing

**Integration with Other Components** :

* The output from this module (predefined website and API processing keywords) will be used by the Website Structure Analysis component to focus on extracting relevant data based on user requirements.
* The user's input may be further clarified or enhanced through interaction with the GPT model, where necessary.

### 2.3. Website Structure Analysis

The Website Structure Analysis component will consist of a module with multiple classes, each responsible for handling different aspects of the analysis, such as DOM parsing, element identification, content extraction, and network traffic analysis.

This module will leverage GPT to enhance the analysis process, especially for identifying relevant elements and detecting APIs through natural language understanding.

- Input: Normalized URL, user requirements (as a dictionary or custom data structure), and (optionally) captured network traffic data
- Output: Website structure analysis results, including relevant elements, their attributes, and detected APIs that can be used for data extraction

Libraries like Beautiful Soup (Python) can be used for parsing and analyzing website DOM. Browser automation tools like Selenium (Python) can be used for capturing network traffic data and identifying API calls made by the website. This component should handle parsing errors, inaccessible websites, anti-scraping measures, and network traffic analysis errors. It should also manage partial analysis results in case of errors and provide fallback strategies when possible, such as using DOM-based scraping if API calls are not accessible or vice versa.

#### 2.3.1. Network Traffic Analysis

We will integrate GPT into the `NetworkAnalyzer` class to enhance the identification and analysis of API calls. The GPT model will be used to understand the context of API calls, determine their relevance to the user requirements, and extract essential information from the API responses.

The component will be implemented as a class named `NetworkAnalyzer` inside the `network_analysis.py` file.

##### 2.3.1.1. Class Diagram

```
network_analysis.py
│
└── NetworkAnalyzer
    ├── __init__(self, url, user_requirements, captured_traffic=None)
    ├── capture_network_traffic(self)
    ├── identify_api_calls(self)
    ├── analyze_api_calls(self)
    ├── filter_api_calls(self)
    └── get_analysis_results(self)
```

##### 2.3.1.2. Class Description

- `NetworkAnalyzer`: This class is responsible for analyzing the network traffic of a given website, identifying API calls, and extracting relevant information required for data extraction.

###### 2.3.1.2.1. Methods

- `__init__(self, url, user_requirements, captured_traffic=None)`: Initializes the `NetworkAnalyzer` instance with the given URL, user requirements (as a dictionary or custom data structure), and optionally, captured network traffic data.

- `capture_network_traffic(self)`: Captures network traffic data for the given URL using browser automation tools like Selenium. This method is called only if the `captured_traffic` parameter is not provided during initialization.

- `identify_api_calls(self)`: Identifies API calls made by the website by analyzing the captured network traffic data. This method should detect API calls made via different methods, such as AJAX requests and WebSockets.

- `analyze_api_calls(self)`: Analyzes the identified API calls and extracts relevant information, such as request format, response format, authentication requirements, and pagination details.

- `filter_api_calls(self)`: Filters the analyzed API calls based on the user requirements (provided as a dictionary or custom data structure), keeping only the API calls relevant to the data extraction process.

- `get_analysis_results(self)`: Returns the network traffic analysis results as a dictionary or custom data structure, including the identified and filtered API calls and their relevant information.

##### 2.3.1.3. Error Handling and Fallback Strategies

The `NetworkAnalyzer` class should handle various errors that might occur during the network traffic analysis process, such as:

- Parsing errors: Handle errors that might occur while parsing network traffic data or analyzing API calls and provide meaningful error messages to the user.

- Inaccessible websites: Handle cases where the target website is not accessible or blocked and provide a suitable error message.

- Anti-scraping measures: Implement strategies to bypass or handle anti-scraping measures, such as using proxies or changing user-agents.

- Network traffic analysis errors: Handle errors that might occur during the network traffic capturing process, such as timeouts or browser automation issues.

The `NetworkAnalyzer` class should also manage partial analysis results in case of errors and provide fallback strategies when possible, such as using DOM-based scraping if API calls are not accessible or vice versa.

##### 2.3.1.4. Interaction with Other Components

The `NetworkAnalyzer` class will interact with other components of the `website_analysis` module, such as the `DomAnalyzer` class, to provide a comprehensive analysis of the website structure. The results from both network traffic analysis and DOM analysis will be combined to generate a complete set of information required for scraper generation and data extraction.


### 2.4. Scraper Generation

The Scraper Generation component will be organized into a module with a primary class responsible for generating the scraper code based on the results of the Website Structure Analysis. Helper functions can be included to support different programming languages and scraping libraries.

- Input: Website structure analysis results and user requirements
- Output: Generated scraper code

Depending on the target programming language, different libraries like Scrapy (Python) or HtmlUnit (Java) can be used for generating the scraper code. This component should handle errors related to unsupported programming languages or scraping libraries and should provide informative error messages to guide the user. It should also validate the generated code to ensure its correctness.

### 2.5. Data Extraction

The Data Extraction component will be organized into a module with a primary class responsible for executing the generated scraper and extracting the data from the target website.

- Input: Generated scraper code and target URL
- Output: Extracted data in a structured format (e.g., JSON, CSV)

The generated scraper will utilize the chosen scraping library to extract data from the target website. The Data Extraction component should handle various types of websites and content, such as AJAX requests, iframes, and nested structures. Additionally, it should manage error handling, timeouts, and rate limits to ensure smooth and efficient data extraction. It should provide informative error messages, implement retries when appropriate, and consider using proxies or other techniques to bypass anti-scraping measures.

### 2.6 GPT Interaction
#### Module Objective

The GPT Interaction module aims to provide a structured way to interact with GPT models for various tasks within the Universal Web Scraper. It includes a base class for handling generic GPT interactions, and subclasses for specific use cases like network analysis and user requirements gathering.
#### Input and Output 
- **Input** : Task-specific prompts and parameters for GPT model calls. 
- **Output** : Processed responses from the GPT model, formatted according to the specific use case.
#### Classes and Methods 
1. `GPTInteraction` (base class) 
- `_set_params()`: Sets GPT model parameters. 
- `call()`: Calls the GPT model with an instruction and value, returning the processed response. 
2. `NetworkAnalysisGPT` (subclass) 
- `process_network_analysis_data()`: Processes network analysis data using the GPT model and returns the formatted results. 
3. `UserRequirementsGPT` (subclass) 
- `gather_user_requirements()`: Gathers user requirements by processing natural language inputs and returns them in a predetermined format.
#### Integration with Other Components

The GPT Interaction module will be utilized by other components within the Universal Web Scraper system: 
- The `NetworkAnalyzer` class in the Website Structure Analysis component can leverage the `NetworkAnalysisGPT` subclass to analyze API calls. 
- The User Requirements Gathering component can utilize the `UserRequirementsGPT` subclass to transform user requirements expressed in natural language into predetermined formats.