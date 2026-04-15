from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
CHANNEL_URL = 'https://www.youtube.com/@abdulwaheed-101/videos'

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


def get_videos():
    driver.get(CHANNEL_URL)
    time.sleep(2)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(f"Channel: {soup.title.text}")

    videos = soup.find_all('div', {"id": "dismissible"})
    print(f"Total Videos: {len(videos)}\n")
    return list(reversed(videos))


def get_video_info(video):
    title_tag = video.find('a', {"id": "video-title-link"})
    metadata = video.find('div', {"id": "metadata-line"})

    if not title_tag or not metadata:
        return None

    spans = metadata.find_all('span')
    return {
        "title": title_tag.text.strip(),
        "url": "https://www.youtube.com" + title_tag.get('href'),
        "views": spans[0].text.strip() if spans else "N/A",
        "age": spans[1].text.strip() if len(spans) > 1 else "N/A",
    }


def get_exact_date():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'yt-formatted-string#info')))
        
        # Click description to reveal exact date
        try:
            desc = driver.find_element(By.CSS_SELECTOR, 'ytd-watch-metadata #description-inline-expander')
            desc.click()
            time.sleep(2)
        except:
            pass

        spans = driver.find_elements(By.CSS_SELECTOR, 'yt-formatted-string#info span')
        for span in spans:
            if any(m in span.text for m in MONTHS):
                return span.text.strip()

    except:
        pass

    # Fallback: meta tag
    try:
        meta = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="datePublished"]')
        return meta.get_attribute('content')
    except:
        pass

    return "N/A"


def get_likes():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'like-button-view-model')))
        time.sleep(1)
        btn = driver.find_element(By.CSS_SELECTOR, 'like-button-view-model button')
        text = btn.text.strip()
        aria = btn.get_attribute('aria-label') or ''

        if text.replace(',', '').isdigit():
            return text
        numbers = re.findall(r'[\d,]+', aria)
        return numbers[0] if numbers else "N/A"
    except:
        return "N/A"


# Main
videos = get_videos()

for i, video in enumerate(videos, start=1):
    info = get_video_info(video)
    if not info:
        continue

    driver.get(info["url"])

    print(f"Video #{i}: {info['title']}")
    print(f"    URL   : {info['url']}")
    print(f"    Views : {info['views']}")
    print(f"    Age   : {info['age']}")
    print(f"    Date  : {get_exact_date()}")
    print(f"    Likes : {get_likes()}\n")

driver.quit()
print("Scraping complete.")