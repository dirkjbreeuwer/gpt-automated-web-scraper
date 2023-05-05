from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import re
import pdb

class NetworkAnalyzer:
    def __init__(self, url, user_requirements, captured_traffic=None):
        self.url = url
        self.user_requirements = user_requirements
        self.captured_traffic = captured_traffic
        self.api_calls = []
        self.analysis_results = {}

    def capture_network_traffic(self):
        if not self.captured_traffic:
            # Set up Selenium with desired capabilities to capture network traffic
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

            # Configure the Chrome driver options
            chrome_options = webdriver.ChromeOptions()
            # Enable headless mode (optional)
            chrome_options.add_argument('--headless')
            # Disable images (optional, for faster browsing)
            #chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            # Disable GPU (optional, may improve stability)
            #chrome_options.add_argument('--disable-gpu')

            # Initialize the browser with the specified capabilities and options
            browser = webdriver.Chrome(desired_capabilities=desired_capabilities, options=chrome_options)

            # Browse the target URL
            browser.get(self.url)

            # Extract network traffic logs
            logs = browser.get_log('performance')

            # Save the longs to a text file
            with open('logs.txt', 'w') as f:
                f.write(str(logs))

            self.captured_traffic = [json.loads(log['message'])['message'] for log in logs]

            # Save the captured traffic to a JSON file

            with open('captured_traffic.json', 'w') as f:
                json.dump(self.captured_traffic, f)


            # Close the browser
            browser.quit()

        # Ensure that captured traffic is not empty
        if not self.captured_traffic:
            raise Exception("Network traffic capturing failed.")




    def identify_api_calls(self):
        identified_api_calls = []

        for entry in self.captured_traffic:
            method = entry.get('method')

            if method == 'Network.requestWillBeSent':
                request = entry['params']['request']
                request_url = request['url']
                request_method = request['method']
                content_type = request['headers'].get('Content-Type', '')

                # Check if the request is an AJAX request
                if request_method in ['GET', 'POST'] and ('application/json' in content_type or 'application/xml' in content_type):
                    api_call = {
                        'url': request_url,
                        'request': request
                    }
                    identified_api_calls.append(api_call)

                # Check if the request is a WebSocket connection
                elif 'WebSocket' in request['headers'].get('Upgrade', ''):
                    api_call = {
                        'url': request_url,
                        'request': request
                    }
                    identified_api_calls.append(api_call)

        # Store the identified API calls in the api_calls attribute
        self.api_calls = identified_api_calls

    def _is_api_call(self, request):
        content_type = request["response"]["headers"].get("Content-Type", "").lower()
        return "json" in content_type or "xml" in content_type


    def analyze_api_calls(self):
        # Return the list of identified API calls
        return self.api_calls

    def filter_api_calls(self):
        # Placeholder for filtering API calls based on user requirements
        pass

    def get_analysis_results(self):
        # Call analyze_api_calls and return the results
        return self.analyze_api_calls()

def main(url):
    user_requirements = {}
    analyzer = NetworkAnalyzer(url, user_requirements)
    analyzer.capture_network_traffic()
    analyzer.identify_api_calls()
    return analyzer.get_analysis_results()


def analyze_websites(websites):
    results = {}
    for url in websites:
        try:
            print(f"Analyzing {url}...")
            analysis_results = main(url)
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
