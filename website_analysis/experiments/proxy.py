import asyncio
import time
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class RequestInterceptor:
    def __init__(self):
        self.urls = []

    def request(self, flow):
        self.urls.append(flow.request.url)

    def print_urls(self):
        for url in self.urls:
            print(url)

async def run_mitmproxy(mitm_options, master_ref):
    request_interceptor = RequestInterceptor()
    master = DumpMaster(mitm_options)
    master.addons.add(request_interceptor)
    master_ref.append(master)

    try:
        await master.run()
    except KeyboardInterrupt:
        pass
    finally:
        master.shutdown()

    request_interceptor.print_urls()

async def main():
    mitm_options = options.Options(listen_host="127.0.0.1", listen_port=8080, mode="transparent")
    master_ref = []

    # Start mitmproxy
    asyncio.create_task(run_mitmproxy(mitm_options, master_ref))
    await asyncio.sleep(5)  # Give mitmproxy some time to start

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

    # ...
    
    url = "https://www.reddit.com/"
    print("Starting request capture...")
    driver.get(url)
    print("Finished request capture.")
    # ...


    driver.implicitly_wait(10)
    driver.quit()

    # Stop mitmproxy
    master = master_ref[0]
    master.shutdown()

# Run the main function
asyncio.run(main())
