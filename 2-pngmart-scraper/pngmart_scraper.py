import requests
from bs4 import BeautifulSoup
import os

# Pretend to be a browser so the site doesn't block us
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Create folder to save images, skip if it already exists
os.makedirs('downloaded_images', exist_ok=True)

# Track already downloaded files so we don't re-download them
downloaded = set(os.listdir('downloaded_images'))

# Get the sitemap index (a list of all sitemaps on the site)
sitemap_index = "https://www.pngmart.com/sitemap_index.xml"
response = requests.get(sitemap_index, headers=headers)
soup = BeautifulSoup(response.text, 'xml')

# Extract all sitemap URLs from the index
site_maps = [loc.text for loc in soup.find_all('loc')]

count = 1  # Counter for filenames

# Loop through each sitemap
for sitemap_url in site_maps:
    response = requests.get(sitemap_url, headers=headers)
    soup = BeautifulSoup(response.text, 'xml')

    # Extract all page URLs from this sitemap
    urls = [loc.text for loc in soup.find_all('loc')]

    # Loop through each page URL
    for image_url in urls:
        try:
            # Visit the page and parse the HTML
            page = requests.get(image_url, headers=headers)
            page_soup = BeautifulSoup(page.text, 'html.parser')

            # Find the main image tag on the page
            img_tag = page_soup.find('img', {'class': 'wp-post-image'})
            if not img_tag:
                continue  # Skip if no image found

            # Get the actual image URL from the lazy-load attribute
            png_url = img_tag.get('data-lazy-src')
            if not png_url:
                continue  # Skip if no URL found

            # Build filename e.g. 1_Scope-Transparent-PNG.png
            filename = f"{count}_{png_url.split('/')[-1]}"

            # Skip if already downloaded
            if filename in downloaded:
                count += 1
                continue

            # Download and save the image
            img_response = requests.get(png_url, headers=headers)
            with open(f'downloaded_images/{filename}', 'wb') as f:
                f.write(img_response.content)

            downloaded.add(filename)
            print(f"Downloaded: {filename}")
            count += 1  # Increment after each download

        except Exception as e:
            print(f"Error on {image_url}: {e}")
            continue
    
 