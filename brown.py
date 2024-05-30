import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from the Wikipedia page
def scrape_dwarf_star_data():
    url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to retrieve data: {response.status_code}")
    
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table", attrs={"class": "wikitable"})

    # Assuming the first table is the correct one. Verify the correct table index if needed.
    table = tables[0]
    
    headers = ["Star_name", "Distance", "Mass", "Radius"]
    rows = table.find_all('tr')[1:]  # Skipping the header row

    dwarf_star_data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 10:  # Ensure there are enough columns
            continue
        star_data = [
            cols[0].text.strip(),  # Star_name
            cols[5].text.strip(),  # Distance
            cols[8].text.strip(),  # Mass
            cols[9].text.strip()   # Radius
        ]
        dwarf_star_data.append(star_data)

    # Convert to DataFrame for easier manipulation and display
    df = pd.DataFrame(dwarf_star_data, columns=headers)

    print("\nScraped Dwarf Star Data:")
    print(df)

    return df

# Scrape data from the URL
scraped_data = scrape_dwarf_star_data()

print(scraped_data)

headers = ["Star_name", "Distance", "Mass", "Radius"]

# Define pandas DataFrame   
starData = pd.DataFrame(scraped_data, columns=headers)

# Convert to CSV
starData.to_csv('scraped_data.csv',index=True, index_label="id")