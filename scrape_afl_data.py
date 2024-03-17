import requests
from bs4 import BeautifulSoup
import json
import re
import argparse
import datetime
import os
import hashlib

CACHE_DIR = "./cache"
cache_usage = 0


def hash_url(url):
    # Hash the URL using SHA-256
    return hashlib.sha256(url.encode()).hexdigest()

def get_soup(url):
    global cache_usage
    # Create cache directory if it doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Generate cache file path
    cache_key = hash_url(url)
    cache_file = os.path.join(CACHE_DIR, cache_key)

    # Check if cached response exists and is recent
    if os.path.exists(cache_file):
        mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.datetime.now() - mod_time < datetime.timedelta(days=1):
            with open(cache_file, "r") as f:
                cache_usage += 1
                return BeautifulSoup(f.read(), features="lxml")

    # If not cached or cache is outdated, fetch from server
    resp = requests.get(url)

    # Save response to cache
    with open(cache_file, "w+") as f:
        f.write(resp.text)

    # Parse response content with BeautifulSoup and return
    return BeautifulSoup(resp.content, features="lxml")

def get_sibling_by_name(element, sibling_name):
    for sib in element.next_siblings:
        if sib.name == sibling_name:
            return sib

    return False

def get_round_urls_for_years(soup, start_year, finish_year, do_2020):
    """
    Extracts URLs for AFL rounds for the specified range of years from the provided BeautifulSoup soup object.

    Args:
    soup (BeautifulSoup): BeautifulSoup object containing HTML data of the webpage.
    start_year (int): Start year for extracting round URLs.
    finish_year (int): Finish year for extracting round URLs.

    Returns:
    list: A list of dictionaries containing URLs for AFL rounds within the specified year range.
          Each dictionary contains the year and the URL for the round.
    """
    table = soup.find("table")
    started = False
    finished = False
    urls = []

    # Iterate through cells in the table to extract round URLs
    for cell in table.find_all("td"):
        if not cell.get_text():
            continue

        year_text = re.findall(r"(\d+)", cell.get_text())
        if not year_text:
            continue

        year = int(year_text[0])
        if not year:
            continue
        
        if year == 2020 and not do_2020:
            print("Skipped 2020")
            continue

        # Break loop if already finished extracting URLs for specified year range
        if finished:
            break

        # Update started flag if the current year matches start_year
        if year == start_year:
            started = True

        # Skip cells until start_year is reached
        if not started:
            continue

        # Update finished flag if the current year matches finish_year
        if year == finish_year:
            finished = True

        # If started, extract URL for the round and add to the list
        if started:
            url = cell.find("a", href=True)["href"]
            urls.append({"year": year, "url": url})

    return urls

def get_round_data(soup):
    """
    Extracts data for each round from the provided BeautifulSoup soup object.

    Args:
    soup (BeautifulSoup): BeautifulSoup object containing HTML data of the webpage.

    Returns:
    list: A list of dictionaries containing data for each round. Each dictionary represents a round
          and contains information about matches including teams, date, venue, attendance, outcome, and margin.
    """
    round_data = {}

    # Iterate through rounds (there are typically 24 rounds in a year of AFL)
    for i in range(1, 25):
        table_sibling = soup.find("b", string=f"Round {i}")

        if not table_sibling:
            continue

        # Find the parent table element containing match data
        table = table_sibling.parent.parent.parent
        round_table = get_sibling_by_name(table, "table")
        match_data = []

        # Iterate through tables containing match data within the round
        for table in round_table.find_all("table"):
            rows = table.find_all("tr")
            _meta_row = (
                {}
            )  # Used for grabbing the changing values that apply to the match, not the team
            team_data = []

            # Iterate through rows of the table containing match data
            for row_num, row in enumerate(rows):
                cells = row.find_all("td")
                if len(cells) < 4:
                    break

                _meta_row[row_num] = cells[3]  # Changing value depending on row
                team_name = cells[0].get_text().strip()
                quarter_scores = cells[1]
                quarters = {}

                # Iterate through quarters of the match
                for quarter_num, quarter in enumerate(
                    quarter_scores.get_text().split(" ")
                ):
                    if not quarter:
                        continue
                    quarter_score = re.findall(r"(\d+\.\d+)", quarter)[0]
                    split_scores = quarter_score.split(".")
                    quarters[str(quarter_num + 1)] = {
                        "goals": int(split_scores[0]),
                        "conversions": int(split_scores[1]),
                    }

                # Split up the scores for each quarter
                final_score = cells[2].get_text()
                team_data.append(
                    {
                        "name": team_name,
                        "quarter_scores": quarters,
                        "final_score": int(final_score),
                    }
                )

            # Extract additional match metadata (date, venue, attendance, outcome, margin)
            if _meta_row:
                dv = _meta_row[0].contents  # Date, venue, and attendance
                if len(dv) == 6:
                    date = dv[0].strip()
                    attendance = int(dv[2].strip().replace(",", ""))
                    venue = dv[5].get_text()
                else:
                    # 2020 doesnt have attendance lol
                    date = dv[0].strip()
                    attendance = None
                    venue = dv[3].get_text()

                match_outcome = _meta_row[1]
                outcome_items = match_outcome.contents
                if len(outcome_items) > 5:
                    margin = int(re.findall(r"(\d+)", outcome_items[2].get_text())[0])
                    outcome_string = "".join(
                        [
                            outcome_items[0].get_text(),
                            outcome_items[1],
                            outcome_items[2].get_text(),
                        ]
                    ).strip()
                else:
                    margin = 0
                    outcome_string = match_outcome.find("b").get_text()

                # Determine the winning team for each match
                for team in team_data:
                    team["won"] = team["name"] in outcome_string

                # Append match data to the round_data list
                match_data.append(
                    {
                        "teams": team_data,
                        "date": date,
                        "venue": venue,
                        "attendance": attendance,
                        "outcome": outcome_string,
                        "margin": margin,
                    }
                )

        # Append match data for the current round to the round_data list
        round_data[str(i)] = match_data

    return round_data

def scrape_afl_data(start_year, end_year, do_2020):
    base_url = "https://afltables.com/afl/seas/"
    seasons_url = f"{base_url}season_idx.html"
    soup = get_soup(seasons_url)
    urls = get_round_urls_for_years(soup, start_year, end_year, do_2020)
    afl_data = []
    for url in urls:
        print(f"Scraped {url['year']}")
        soup = get_soup(base_url + url["url"])
        round_data = get_round_data(soup)
        afl_data.append({"year": url["year"], "rounds": round_data})

    output_file = f"{start_year}_{end_year}_data.json"

    with open(output_file, "w+") as fn:
        json.dump(afl_data, fn, indent=4)

    print(f"Data scraped and saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Scrape AFL data for specified years. 2020 is excluded by default.")
    parser.add_argument("start_year", type=int, help="Start year for scraping AFL data")
    parser.add_argument("end_year", type=int, help="End year for scraping AFL data")
    parser.add_argument("-covid", default=False, required=False, type=int, help="Include 2020 in the data, if it is a valid year. By default it is ignored.")
    args = parser.parse_args()

    start_year = args.start_year
    end_year = args.end_year
    do_2020 = args.covid
    if start_year > end_year:
        print("Error: Start year cannot be greater than end year.")
        return

    scrape_afl_data(start_year, end_year, do_2020)


if __name__ == "__main__":
    main()

    # scrape_afl_data(2019, 2021, True)
    
    print(f"Cache used {cache_usage} times")