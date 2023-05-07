"""xhr.py: A script to monitor and capture XMLHttpRequest and Fetch API requests."""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scroll(driver, max_scroll_cycles=10, max_allowed_time=60, sleep_time=3):
    """
    Scroll down a web page to capture any API requests triggered by scrolling.

    :param driver: The WebDriver instance controlling the browser
    :param max_scroll_cycles: Maximum number of scroll cycles to perform
    :param max_allowed_time: Maximum allowed time in seconds for scrolling
    :param sleep_time: Time in seconds to wait between scroll actions
    """
    start_time = time.time()
    scroll_cycle = 0

    while (
        scroll_cycle < max_scroll_cycles
        and (time.time() - start_time) < max_allowed_time
    ):
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)

        # Check if the scroll position has changed after scrolling down
        scroll_position = driver.execute_script("return window.pageYOffset;")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)
        new_scroll_position = driver.execute_script("return window.pageYOffset;")

        # If the scroll position hasn't changed, the bottom of the page has been reached
        if scroll_position == new_scroll_position:
            break

        scroll_cycle += 1


chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
chrome_options.add_argument("--headless")


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://ra.co/events/uk/london?page=2")


def monitor_requests(driver):
    """
    Attach listeners to XMLHttpRequest and Fetch API to capture API requests.

    :param driver: The WebDriver instance controlling the browser
    """
    driver.execute_script(
        """
        window.api_endpoints = new Set();

        (function(open, send) {
            XMLHttpRequest.prototype.open = function() {
                this.url = arguments[1];
                open.apply(this, arguments);
            };
            XMLHttpRequest.prototype.send = function() {
                if (this.url) {
                    window.api_endpoints.add(this.url);
                }
                send.apply(this, arguments);
            };
        })(XMLHttpRequest.prototype.open, XMLHttpRequest.prototype.send);

        (function(fetch) {
            window.fetch = function() {
                window.api_endpoints.add(arguments[0]);
                return fetch.apply(this, arguments);
            };
        })(window.fetch);
    """
    )


monitor_requests(driver)
time.sleep(10)

# Perform scrolling to capture APIs triggered by scrolling
scroll(driver)

api_endpoints = driver.execute_script("return Array.from(window.api_endpoints);")

print("API Endpoints:")
for endpoint in api_endpoints:
    print(endpoint)

driver.quit()
