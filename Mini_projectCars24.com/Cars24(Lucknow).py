from bs4 import BeautifulSoup
import pandas as pd
import requests

# List of car brands to scrape
brands = ['tata', 'hyundai', 'honda', 'maruti']

# Initialize lists for combined data
all_company = []
all_car_name = []
all_Km = []
all_fuel_type = []
all_types = []
all_price = []
all_location = []
all_years = []
all_brand = []

# Function to scrape data from a page
def scrape_page(website):
    response = requests.get(website)
    Soup = BeautifulSoup(response.content, 'html.parser')
    result = Soup.find_all('div', {'class': "_2YB7p"})

    # Extract data
    for i in result:
        # Company and car_name
        k = i.find_all('h3', {'class': "_11dVb"})
        for item in k:
            parts = item.get_text().split()
            if len(parts) >= 3:
                all_years.append(parts[0])
                all_company.append(parts[1])
                all_car_name.append(parts[2])
                all_brand.append(brand)

        # Km driven
        k = i.find_all('ul', {'class': "_3J2G-"})
        for item in k:
            p = item.find_all('li')
            all_Km.append(p[0].get_text() if len(p) > 0 else None)

        # Fuel type
        if len(p) > 2:
            all_fuel_type.append(p[2].get_text())
        else:
            all_fuel_type.append(None)

        # Transmission type
        if len(p) > 4:
            all_types.append(p[4].get_text())
        else:
            all_types.append(None)

        # Price
        k = i.find_all('div', {'class': '_2KyOK'})
        for item in k:
            j = item.find_all('strong')
            all_price.append(j[0].get_text() if len(j) > 0 else None)

        # Location
        k = i.find_all('p', {'class': "_3dGMY"})
        for item in k:
            j = item.find_all('span')
            location_text = j[1].get_text() if len(j) > 1 else None
            all_location.append('Lucknow' if location_text is None else 'Lucknow')

# Loop through each brand and scrape data from all pages
for brand in brands:
    page = 1
    while True:
        website = f'https://www.cars24.com/buy-used-car?f=make%3A%3D%3A{brand}&sort=bestmatch&serveWarrantyCount=true&gaId=855532033.1722741892&listingSource=TabFilter&storeCityId=290&page={page}'
        response = requests.get(website)
        if response.status_code != 200:
            break
        scrape_page(website)
        page += 1

# Handle cases where some lists might be shorter by filling with None
max_length = max(len(all_company), len(all_car_name), len(all_Km), len(all_fuel_type), len(all_types), len(all_price), len(all_location), len(all_years))

all_company += [None] * (max_length - len(all_company))
all_car_name += [None] * (max_length - len(all_car_name))
all_Km += [None] * (max_length - len(all_Km))
all_fuel_type += [None] * (max_length - len(all_fuel_type))
all_types += [None] * (max_length - len(all_types))
all_price += [None] * (max_length - len(all_price))
all_location += [None] * (max_length - len(all_location))
all_years += [None] * (max_length - len(all_years))

# Create DataFrame
data = pd.DataFrame({
    'Year': all_years,
    'Car': all_company,
    'Model': all_car_name,
    'KM Driven': all_Km,
    'Fuel_type': all_fuel_type,
    'Transmission': all_types,
    'Price': all_price,
    'Location': all_location,
    'Brand': all_brand
})

data['Location'] = data['Location'].replace('', 'Lucknow').fillna('Lucknow')

# Verify DataFrame
print(data)

# Save to CSV
data.to_csv('Cars24_Lucknow.csv', index=False)

import pandas as pd
df=pd.read_csv('merged_car_details.csv')
df

