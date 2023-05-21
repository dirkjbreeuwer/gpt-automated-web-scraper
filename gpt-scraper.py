from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.llms import OpenAI
import argparse
from website_analysis.dom_analysis import HtmlLoader, UrlHtmlLoader, HtmlManager
from scraper_generation.scraper_generator import ScrapingCodeGenerator, CodeWriter
from data_extraction.data_extractor import CodeExecutor 


def main():
    # Receive and parse arguments
    parser = argparse.ArgumentParser(description='AI Web Scraper')
    parser.add_argument('--source', type=str, help='The URL or local path to HTML to scrape')
    parser.add_argument('--source-type', type=str, choices=['url', 'file'], help='Type of the source: url or file')
    parser.add_argument('--requirements', type=str, help='The user requirements for scraping')
    parser.add_argument('--target-string', type=str, help='An example string to guide the scraper')
    args = parser.parse_args()

    source = args.source
    source_type = args.source_type
    USER_REQUIREMENTS = args.requirements
    target_string = args.target_string
    

    # Instantiate the HTML manager
    manager = HtmlManager(source, source_type, target_string)

    # Load Processed HTML
    processed_html = manager.process_html()

    # Instantiate ScrapingCodeGenerator with the processed_html
    code_generator = ScrapingCodeGenerator(processed_html, source=source, source_type=source_type)

    # Generate scraping code
    scraping_code = code_generator.generate_scraping_code(USER_REQUIREMENTS)

    # Instantiate CodeWriter
    code_writer = CodeWriter('scraping_code.py')

    # Write the code to a file
    code_writer.write(scraping_code)

    # Instantiate CodeExecutor
    code_executor = CodeExecutor('scraping_code.py')

    # Execute the code
    code_executor.execute()

if __name__ == "__main__":
    main()


# python3 gpt-scraper.py --source-type "file" --source "./results/denver.html" --requirements "Extract the average monthly temperature in denver"