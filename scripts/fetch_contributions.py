import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_contributions(username="Oneshika7", output_path="data/contributions.json"):
    print(f"Fetching contributions for {username}...")
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url} - Status: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    
    for cell in soup.find_all("td", class_="ContributionCalendar-day"):
        date = cell.get("data-date")
        level = cell.get("data-level")
        if date and level:
            days.append({
                "date": date,
                "level": int(level)
            })
            
    if not days:
        print("Warning: Could not find any contribution cells. The DOM might have changed.")
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(days, f, indent=2)
        
    print(f"Saved {len(days)} days of contributions to {output_path}")

if __name__ == "__main__":
    fetch_contributions()
