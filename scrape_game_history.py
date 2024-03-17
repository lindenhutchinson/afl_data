import requests
from bs4 import BeautifulSoup
import json
import re

#   1.4   2.4   7.8  8.10  = tries.conversions at each quarter of the game
def get_sibling_by_name(element, sibling_name):
    for sib in element.next_siblings:
        if sib.name == sibling_name:
            return sib
        
    return False



# with open("response.txt", "w+") as fn:
#     fn.write(str(resp.content))

# soup = BeautifulSoup(resp.conte)
# table_sibling = soup.find('a', name="1")
    
def get_round_urls_for_years(soup, start_year, finish_year):
    table = soup.find("table")
    started = False
    finished = False
    urls = []
    for cell in table.find_all("td"):
        if not cell.get_text():
            continue

        year_text = re.findall(r"(\d+)", cell.get_text())
        if not year_text:
            continue

        year = int(year_text[0])
        if not year:
            continue
        
        if finished:
            break

        if year == start_year:
            started = True

        if not started:
            continue

        if year == finish_year:
            finished = True

        if started:
            url = cell.find("a", href=True)["href"]
            urls.append({
                "year": year,
                "url": url
            })

    return urls        

        

def get_round_data(soup):
    round_data = []
    for i in range(1, 25): # 24 rounds in a year of AFL
        table_sibling = soup.find("b", string=f"Round {i}")
        if not table_sibling:
            continue

        table = table_sibling.parent.parent.parent# three parents away from the main table
        round_table = get_sibling_by_name(table, "table")
        match_data = []

        for table in round_table.find_all("table"):
            rows = table.find_all("tr")
            _meta_row = {} # used for grabbing the changing values that apply to the match, not the team
            team_data = []
            for row_num, row in enumerate(rows):
                cells = row.find_all("td")
                if len(cells) < 4:
                    break
                _meta_row[row_num] = cells[3] # changing value depending on row
                team_name = cells[0].get_text().strip()
                quarter_scores = cells[1]
                quarters = {}
                for quarter_num, quarter in enumerate(quarter_scores.get_text().split(" ")):
                    if not quarter:
                        continue
                    quarter_score = re.findall(r"(\d+\.\d+)", quarter)[0]
                    split_scores = quarter_score.split('.')
                    quarters.update(
                        {
                            str(quarter_num+1): {
                                "tries": int(split_scores[0]),
                                "conversions":int(split_scores[1])
                            }
                        }

                    )

                # split up the scores for each quarter
                final_score = cells[2].get_text()
                team_data.append(
                    {
                        "name":team_name,
                        "quarter_scores":quarters,
                        "final_score":int(final_score)
                    }
                )
            if _meta_row:
                dv = _meta_row[0].contents # date, venue and attendance
                if len(dv) == 6:
                    date = dv[0].strip()
                    attendance = int(dv[2].strip().replace(',', ''))
                    venue = dv[5].get_text()


                match_outcome = _meta_row[1]
                outcome_items = match_outcome.contents
                if len(outcome_items) > 5:
                    margin = int(re.findall(r"(\d+)", outcome_items[2].get_text())[0])
                    outcome_string = ''.join([outcome_items[0].get_text(), outcome_items[1], outcome_items[2].get_text()]).strip()
                else:
                    margin = 0
                    outcome_string = match_outcome.find("b").get_text()
                    
            
                for team in team_data:
                    team["won"] = team["name"] in outcome_string

                match_data.append({
                    "teams":team_data,
                    "date":date,
                    "venue":venue,
                    "attendance":attendance,
                    "outcome":outcome_string,
                    "margin":margin
                })

        round_data.append({
            str(i): match_data
        })

    return round_data

def get_soup(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.content, features="lxml")

base_url = "https://afltables.com/afl/seas/"
seasons_url = f"{base_url}season_idx.html"
# # resp = requests.get(url)
# with open("response.txt", "r") as fn:
#     soup = BeautifulSoup(fn.readline(), features="lxml")
soup = get_soup(seasons_url)
urls = get_round_urls_for_years(soup, 2010, 2015)
afl_data = []
for url in urls:
    print(url)
    soup = get_soup(base_url+url["url"])
    round_data = get_round_data(soup)
    afl_data.append({
        "year":url["year"],
        "data": round_data
    })


with open("2023_data.json", "w+") as fn:
    json.dump(afl_data, fn, indent=4)