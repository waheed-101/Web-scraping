import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
import os

OUTPUT_FILE = 'clinic_data.csv'
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def get_clinic_name(clinic_id):
    url = f"https://{clinic_id}.portal.athenahealth.com/"

    try:
        # Added timeout to prevent indefinite hanging
        response = requests.get(url, timeout=10)

        # Check status code before parsing
        if response.status_code != 200:
            return None

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Guard against empty h1 list to avoid IndexError
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            return None

        clinic_name = h1_tags[-1].text.strip()
        return clinic_name

    # Handle network/request errors gracefully
    except requests.exceptions.Timeout:
        print(f"[{clinic_id}] Request timed out.")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[{clinic_id}] Connection error.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[{clinic_id}] Request failed: {e}")
        return None


INVALID_NAMES = {
    '',
    'Payment Confirmation',
    "Sorry, we can't find that practice. Make sure you typed the right address."
}

# Write header once if file doesn't exist yet (incremental saving)
file_exists = os.path.isfile(OUTPUT_FILE)
csv_file = open(OUTPUT_FILE, 'a', newline='', encoding='utf-8')
writer = csv.DictWriter(csv_file, fieldnames=['clinic_id', 'clinic_name'])

if not file_exists:
    writer.writeheader()

for clinic_id in range(0, 15001):
    clinic_name = get_clinic_name(clinic_id)

    if clinic_name and clinic_name not in INVALID_NAMES:
        writer.writerow({'clinic_id': clinic_id, 'clinic_name': clinic_name})
        csv_file.flush()  # Flush to disk immediately after each write
        print(f"[{clinic_id}] Found: {clinic_name}")
    else:
        print(f"[{clinic_id}] Skipped.")

    # Rate limiting — pause between requests
    time.sleep(RATE_LIMIT_DELAY)

csv_file.close()
print("Done. Data saved to", OUTPUT_FILE)

# Load the saved CSV into a DataFrame for further analysis
df = pd.read_csv(OUTPUT_FILE)
print(df)