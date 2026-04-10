# AthenaHealth Clinic Scraper

A Python script that scrapes clinic names from AthenaHealth patient portals by iterating over clinic IDs and saving the results to a CSV file.

## What It Does

- Iterates over clinic IDs from 1 to 15000
- Visits each clinic's AthenaHealth portal URL (`https://{clinic_id}.portal.athenahealth.com/`)
- Extracts the clinic name from the page
- Saves valid results incrementally to `clinic_data.csv`
- Loads the final CSV into a pandas DataFrame for further analysis

The script will print progress for each ID and save results to `clinic_data.csv` in the same directory.

## Output

A CSV file (`clinic_data.csv`) with two columns:

| clinic_id | clinic_name |
|-----------|-------------|
| 195 | Example Medical Group |
| 502 | Sunrise Health Clinic |

## Features

- **Incremental saving** — results are written to disk after each valid entry, so progress is not lost if the script crashes
- **Rate limiting** — 0.5 second delay between requests to avoid getting IP blocked
- **Timeout handling** — each request times out after 10 seconds
- **Error handling** — network errors, timeouts, and connection failures are caught and skipped gracefully
- **Status code checks** — non-200 responses are skipped
- **Invalid name filtering** — generic or error page names are excluded from results
