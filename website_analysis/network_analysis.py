"""network_analysis.py: A script to identify API calls using Selenium and GPT-4.

The analysis results are presented in a tabular format.
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import openai


def load_config():
    """
    Load the API key from the configuration file.

    :return: A dictionary containing the configuration data
    """
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
    return config_data


config = load_config()
gpt4_api_key = config["gpt4"]["api_key"]


class NetworkAnalyzer:
    """NetworkAnalyzer: A class for analyzing network traffic.

    Identifies API calls, processes them using GPT
    and the analysis results are presented in a tabular format.
    """

    def __init__(
        self, url, user_requirements, captured_traffic=None, open_api_key=None
    ):
        """
        Initialize the NetworkAnalyzer class.

        :param url: The target website URL
        :param user_requirements: A dictionary containing user requirements (unused)
        :param captured_traffic: A list of captured network traffic (optional)
        :param open_api_key: The GPT-4 API key
        """
        self.url = url
        self.user_requirements = user_requirements
        self.captured_traffic = captured_traffic
        self.api_calls = []
        self.analysis_results = {}
        self.open_api_key = open_api_key
        if open_api_key:
            openai.api_key = open_api_key

    def capture_network_traffic(self):
        """Capture network traffic using Selenium and save the logs to a JSON file."""
        if not self.captured_traffic:
            # Set up Selenium with desired capabilities to capture network traffic
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

            # Configure the Chrome driver options
            chrome_options = webdriver.ChromeOptions()
            # Enable headless mode (optional)
            chrome_options.add_argument("--headless")
            # Disable images (optional, for faster browsing)
            chrome_options.add_argument("--blink-settings=imagesEnabled=false")
            # Disable GPU (optional, may improve stability)
            chrome_options.add_argument("--disable-gpu")

            # Initialize the browser with the specified capabilities and options
            browser = webdriver.Chrome(
                desired_capabilities=desired_capabilities, options=chrome_options
            )

            # Browse the target URL
            browser.get(self.url)

            # Extract network traffic logs
            logs = browser.get_log("performance")

            # Save logs to a text file
            with open("logs.txt", "w") as f:
                f.write(str(logs))

            self.captured_traffic = [
                json.loads(log["message"])["message"] for log in logs
            ]

            # Save the captured traffic to a JSON file
            with open("captured_traffic.json", "w") as f:
                json.dump(self.captured_traffic, f)

            # Close the browser
            browser.quit()

        # Ensure that captured traffic is not empty
        if not self.captured_traffic:
            raise Exception("Network traffic capturing failed.")

    def identify_api_calls(self):
        """Identify API calls in the captured network traffic."""
        identified_api_calls = []

        for entry in self.captured_traffic:
            method = entry.get("method")

            if method == "Network.requestWillBeSent":
                request = entry["params"]["request"]
                request_url = request["url"]
                request_method = request["method"]
                content_type = request["headers"].get("Content-Type", "")

                # Check if the request is an AJAX request
                if request_method in ["GET", "POST"] and (
                    "application/json" in content_type
                    or "application/xml" in content_type
                ):
                    api_call = {"url": request_url, "request": request}
                    identified_api_calls.append(api_call)

                # Check if the request is a WebSocket connection
                elif "WebSocket" in request["headers"].get("Upgrade", ""):
                    api_call = {"url": request_url, "request": request}
                    identified_api_calls.append(api_call)

        # Store the identified API calls in the api_calls attribute
        self.api_calls = identified_api_calls

    def _is_api_call(self, request):
        content_type = request["response"]["headers"].get("Content-Type", "").lower()
        return "json" in content_type or "xml" in content_type

    def analyze_api_calls(self):
        """
        Analyze API calls using GPT-4 and return the analysis results.

        :return: The API analysis results
        """
        # Prepare the API calls data for input to GPT-3
        api_calls_data = json.dumps(self.api_calls, indent=2)

        # Construct the GPT-3 prompt
        prompt = (
            f"We are trying to identify a website's internal API.\n\n"
            f"Here are all XML and JSON results we found when navigating this website:\n\n"
            f"{api_calls_data}\n\n"
            f"Can you parse the websites XML and JSON results into the following format: \n\n"
            f"| URL | Referer | Method | Purpose |\n"
        )

        # Call the GPT-3 API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the API analysis results from the GPT-3 response
        api_analysis_results = response.choices[0].text.strip()

        return api_analysis_results

    def filter_api_calls(self):
        """Filter the API calls based on user requirements."""
        # Placeholder for filtering API calls based on user requirements
        return "Module not implemented."

    def get_analysis_results(self):
        """
        Get the API analysis results by calling analyze_api_calls.

        :return: The API analysis results
        """
        return self.analyze_api_calls()

    def analyze_website(self):
        """
        Analyze the target website.

        :return: The API analysis results
        """
        self.capture_network_traffic()
        self.identify_api_calls()
        api_analysis_results = self.analyze_api_calls()
        return api_analysis_results


def analyze_websites(websites):
    """
    Analyze a list of websites using the NetworkAnalyzer class.

    :param websites: A list of website URLs to analyze
    :return: A dictionary containing the analysis results for each website
    """
    results = {}
    for url in websites:
        try:
            print(f"Analyzing {url}...")
            analyzer = NetworkAnalyzer(url, {}, open_api_key=gpt4_api_key)
            analysis_results = analyzer.analyze_website()
            results[url] = analysis_results
            print(f"Analysis results for {url}: {analysis_results}")
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
            results[url] = {"error": str(e)}
    return results


# Usage example
if __name__ == "__main__":
    websites = [
        "https://www.airbnb.com",
        "https://www.twitter.com",
        "https://www.github.com",
        "https://www.reddit.com",
        "https://www.spotify.com",
        "https://www.netflix.com",
        "https://www.amazon.com",
        "https://www.instagram.com",
        "https://www.linkedin.com",
        "https://www.trello.com",
        "https://www.slack.com",
        "https://www.pinterest.com",
        "https://www.foursquare.com",
        "https://www.yelp.com",
        "https://www.dropbox.com",
        "https://www.medium.com",
        "https://www.coursera.org",
        "https://www.stackoverflow.com",
        "https://www.khanacademy.org",
        "https://www.weather.com",
    ]
    results = analyze_websites(websites)
    print(results)
