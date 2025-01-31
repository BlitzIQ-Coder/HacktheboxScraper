from bs4 import BeautifulSoup
import requests
import pandas as pd

categories = {
    "Hoodies": "https://hackthebox.store/collections/hoodies",
    "T-Shirts (Page 1)": "https://hackthebox.store/collections/t-shirts?page=1",
    "T-Shirts (Page 2)": "https://hackthebox.store/collections/t-shirts?page=2",
    "Stickers (Page 1)": "https://hackthebox.store/collections/hack-the-box-stickers?page=1",
    "Stickers (Page 2)": "https://hackthebox.store/collections/hack-the-box-stickers?page=2",
    "Apparel Accessories": "https://hackthebox.store/collections/caps-hats-beanies",
    "Mugs & Thermos": "https://hackthebox.store/collections/mugs-thermos",
    "Jackets": "https://hackthebox.store/collections/jackets",
    "Socks": "https://hackthebox.store/collections/socks",
    "Pins & Badges": "https://hackthebox.store/collections/pins-badges",
    "Lanyards": "https://hackthebox.store/collections/lanyards",
    "Dog Swag": "https://hackthebox.store/collections/dog-swags"
}

excel_data = [] # List to hold all product details
# Function to scrape products from a category
def scrape_category(category_name, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.find_all("div", class_="card__content")

    product_names = set()
    
    excel_data.append([category_name, "", ""])  # Append category name as a header row
    excel_data.append(["Name", "Price", "Link"])  # Column Headers
    
    for product in products:
        try:
            name = product.find("h3", {"class": "card__heading"}).text.strip()
            price = product.find("span", {"class": "money"}).text.strip().replace("\u00a3", "$")
            link_suffix = product.a['href'].strip()
            link = f"https://hackthebox.store{link_suffix}"

            if name not in product_names:  # Prevent duplicate entries
                product_names.add(name)
                excel_data.append([name, price, link])
        except AttributeError:
            continue

    excel_data.append(["", "", ""])  # spacing row

# Scrape all categories
for category, url in categories.items():
    scrape_category(category, url)

df = pd.DataFrame(excel_data, columns=["Name", "Price", "Link"]) # Convert data to DataFrame

df.to_excel("HTB_Products.xlsx", index=False, header=False, engine="openpyxl")# Save to Excel in one sheet

print("Data successfully saved to HTB_Products.xlsx")
