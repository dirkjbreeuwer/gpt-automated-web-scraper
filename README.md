# AI Web Scraper
![GPT based automated webscrapper](https://cdn.discordapp.com/attachments/984632500875821066/1104363425439698944/analyticsynthetic_Small_cute_mining_robot_with_large_eyes_5501ffb9-ea08-4dfc-b04d-9623f7c4481a.png "GPT based automated webscrapper")

This project is an AI-powered web scraper that allows you to extract information from HTML sources based on user-defined requirements. It generates scraping code and executes it to retrieve the desired data.

## Prerequisites

Before running the AI Web Scraper, ensure you have the following prerequisites installed:

- Python 3.x
- The required Python packages specified in the `requirements.txt` file
- An API key for the OpenAI GPT-4

## Installation

1. Clone the project repository:

   ```shell
   git clone https://github.com/dirkjbreeuwer/gpt-automated-web-scraper
   ```

2. Navigate to the project directory:

   ```shell
   cd gpt-automated-web-scraper
   ```

3. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up the OpenAI GPT-4 API key:
   
   - Obtain an API key from OpenAI by following their documentation.
   - Rename the file called `.env.example` to `.env` in the project directory.
   - Add the following line to the `.env` file, replacing `YOUR_API_KEY` with your actual API key:

     ```plaintext
     OPENAI_API_KEY=YOUR_API_KEY
     ```

## Usage

To use the AI Web Scraper, run the `gpt-scraper.py` script with the desired command-line arguments.

### Command-line Arguments

The following command-line arguments are available:

- `--source`: The URL or local path to the HTML source to scrape.
- `--source-type`: Type of the source. Specify either `"url"` or `"file"`.
- `--requirements`: User-defined requirements for scraping.
- `--target-string`:  Due to the maximum token limit of GPT-4 (4k tokens), the AI model processes a smaller subset of the HTML where the desired data is located. The target string should be an example string that can be found within the website you want to scrape. 

### Example Usage

Here are some example commands for using the AI Web Scraper:

```shell
python3 gpt-scraper.py --source-type "url" --source "https://www.scrapethissite.com/pages/forms/" --requirements "Print a JSON file with all the information available for the Chicago Blackhawks" --target-string "Chicago Blackhawks"
```

Replace the values for `--source`, `--requirements`, and `--target-string` with your specific values.


## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify and use it according to your needs.

