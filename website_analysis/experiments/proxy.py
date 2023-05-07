"""
proxy.py: A module for capturing network traffic using mitmproxy and Selenium WebDriver.

This module provides functionality to intercept HTTP requests and responses
while browsing a website using the Selenium WebDriver and mitmproxy as a proxy server.
"""

import asyncio
from asyncio import Event
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from mitmproxy import http


class RequestInterceptor:
    """A class for intercepting and storing HTTP requests and responses."""

    def __init__(self):
        """Initialize the RequestInterceptor class with an empty list of URLs."""
        self.urls = []

    def http_connect(self, flow: http.HTTPFlow) -> None:
        """
        Add the URL of the intercepted HTTP CONNECT request to the list of URLs.

        :param flow: The intercepted HTTPFlow object
        """
        self.urls.append(flow.request.url)

    def response(self, flow: http.HTTPFlow) -> None:
        """
        Add the URL of the intercepted HTTP response to the list of URLs.

        :param flow: The intercepted HTTPFlow object
        """
        self.urls.append(flow.request.url)

    def print_urls(self):
        """Print the list of intercepted URLs."""
        for url in self.urls:
            print(url)


async def run_mitmproxy(mitm_options, master_ref, shutdown_event, started_event):
    """
    Run mitmproxy with the specified options, addons, and events.

    :param mitm_options: The mitmproxy options object
    :param master_ref: A reference to the mitmproxy master instance
    :param shutdown_event: An asyncio event signaling mitmproxy to shut down
    :param started_event: An asyncio event signaling mitmproxy has started
    """
    request_interceptor = RequestInterceptor()
    master = DumpMaster(mitm_options)
    master.addons.add(request_interceptor)
    master_ref.append(master)

    async def set_started():
        await asyncio.sleep(0.5)
        started_event.set()

    asyncio.create_task(set_started())

    try:
        await master.run()
    except KeyboardInterrupt:
        pass
    finally:
        master.shutdown()

    await shutdown_event.wait()
    request_interceptor.print_urls()


async def main():
    """Set up mitmproxy, start Selenium WebDriver with Chrome, and capture network traffic."""
    mitm_options = options.Options(
        listen_host="127.0.0.1", listen_port=8080, mode="regular"
    )
    master_ref = []
    shutdown_event = Event()
    started_event = Event()

    # Start mitmproxy
    mitmproxy_task = asyncio.create_task(
        run_mitmproxy(mitm_options, master_ref, shutdown_event, started_event)
    )
    await started_event.wait()

    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--proxy-server=http://127.0.0.1:8080")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = "https://www.reddit.com/"
    print("Starting request capture...")
    driver.get(url)
    print("Finished request capture.")

    driver.implicitly_wait(10)
    driver.quit()

    # Stop mitmproxy
    master = master_ref[0]
    master.shutdown()
    shutdown_event.set()
    await mitmproxy_task


# Run the main function
asyncio.run(main())
