# AFL Data Scraper

the first AFL dataset i found on kaggle didnt have venues, so i wrote this scraper to grab everything i wanted.

i used chatgpt to help with some visualisations and predictions.

## Usage

To use the scraper, follow these steps:

1. Set up a virtual environment (venv) for the project and install the required packages listed in requirements.txt.

2. Run the `scrape_afl_data` file, specifying the start year and end year for scraping AFL data. By default, data for the year 2020 is excluded. You can include 2020 data by passing the `-covid` flag with a value of `1`.

3. The scraped data will be saved in a JSON file named `{start_year}_{end_year}_data.json`.

## Running the Scraper

To run the scraper, execute the script specifying the start year and end year as command-line arguments. Optionally, include the `-covid` flag with a value of `1` to include data for the year 2020.

For example:

```bash
python scrape_afl_data.py 2018 2022 -covid 1
```

This will scrape AFL data for the years 2018 to 2022, including data for the year 2020.

Responses are cached to minimise the requests made to the source site.

The cache directory is created when a response is cached for the first time.

Delete it to force new requests. Cached responses are valid for 1 day
