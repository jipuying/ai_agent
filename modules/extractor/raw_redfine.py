import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


def extract_redfin_data(output_path, url):
    """
    Extracts data from a Redfin property page using Selenium with undetected-chromedriver.
    Saves the visible text of the page to a file.
    """
    # Ensure the directory exists
    import os
    os.makedirs(os.path.join(output_path, "raw"), exist_ok=True)
    
    # Initialize Chrome with undetected-chromedriver
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)

    try:
        # Visit Redfin page
        driver.get(url)
        
        # Simulate user interaction
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Get visible body text
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # Save or print the text
        with open(os.path.join(output_path, "raw", "redfin.txt"), "w", encoding="utf-8") as f:
            f.write(page_text)

        print("✅ Page text saved to redfin_output.txt")
    finally:
        driver.quit()

if __name__ == "__main__":
    urls = ["https://www.redfin.com/CA/Redwood-City/318-Genoa-Dr-94065/unit-160/home/1721607",
           "https://www.redfin.com/CA/Redwood-City/308-Whidbey-Ln-94065/home/40100269",
           "https://www.redfin.com/CA/Redwood-City/1-Spinnaker-Pl-94065/home/1883167",
           "https://www.redfin.com/CA/Belmont/14-Arroyo-View-Cir-94002/home/1515174",
           "https://www.redfin.com/CA/Belmont/366-Treasure-Island-Dr-94002/home/1505081"]
    
    for i, url in enumerate(urls):
        output_path = "../../data/example" + str(i + 1)
        extract_redfin_data(output_path, url)
        print(f"Extracting data from {url}")
   