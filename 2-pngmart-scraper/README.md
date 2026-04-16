# PNGMart Image Scraper

A Python script that scrapes PNG images from PNGMart by crawling the sitemap and downloading all available images to a local folder.

## What It Does

- Fetches the sitemap index from `https://www.pngmart.com/sitemap_index.xml`
- Iterates through all sitemaps and extracts every page URL
- Visits each page and finds the main image using the `wp-post-image` class
- Downloads images using the lazy-load source (`data-lazy-src`)
- Saves all images incrementally to a `downloaded_images/` folder

The script prints progress for each downloaded file and skips any already downloaded images on re-run.

## Output

A folder (`downloaded_images/`) containing all downloaded PNG files:

| Filename | Description |
|----------|-------------|
| 1_Apple-Transparent-PNG.png | First downloaded image |
| 2_Car-PNG-Image.png | Second downloaded image |

## Features

- **Browser spoofing** — sends a real browser User-Agent header to avoid being blocked
- **Incremental saving** — already downloaded files are skipped on re-run, so progress is not lost
- **Lazy-load handling** — extracts image URLs from `data-lazy-src` attribute used by the site
- **Error handling** — network errors and missing images are caught and skipped gracefully
- **Auto folder creation** — `downloaded_images/` folder is created automatically if it doesn't exist
