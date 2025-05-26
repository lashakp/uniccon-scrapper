import requests
from bs4 import BeautifulSoup
import pandas as pd

# STEP 1: Define the target URL
url = "https://health.gov.ng/"

# STEP 2: Send an HTTP GET request to fetch the page content
response = requests.get(url)

# STEP 3: Check if the request was successful
if response.status_code != 200:
    raise Exception(f"Failed to load page: {response.status_code}")

# STEP 4: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# STEP 5: Extract the page <title>
title = soup.find("title").text.strip() if soup.find("title") else "No title found"
print(f"Page Title: {title}")

# STEP 6: Extract all hyperlinks (<a> tags with href attributes)
links = soup.find_all("a", href=True)
print("\n--- Links ---")
for link in links:
    print(f"Link: {link['href'].strip()}")

# STEP 7: Extract all paragraph elements (<p> tags)
paragraphs = soup.find_all("p")
print("\n--- Paragraphs ---")
for paragraph in paragraphs:
    print(f"Paragraph: {paragraph.text.strip()}")

# STEP 8: Extract all headings (h1 to h6)
headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
print("\n--- Headings ---")
for heading in headings:
    print(f"Heading: {heading.text.strip()}")

# STEP 9: Extract all script tags and get their 'src' attribute if present
scripts = soup.find_all("script")
print("\n--- Script Sources ---")
for script in scripts:
    src = script.get('src')
    print(f"Script: {src.strip() if src else 'Inline Script or None'}")

# STEP 10: Prepare detailed paragraph data: raw HTML and text
all_p_tags_html = [str(paragraph) for paragraph in paragraphs]  # HTML of <p>
all_p_tags_text = [paragraph.text.strip() for paragraph in paragraphs]  # Text only

# STEP 11: Compile extracted content into a dictionary for DataFrame
data = {
    "Title": [title],  # Title as a single value
    "Links": [[link['href'].strip() for link in links]],  # List of all href links
    "Paragraphs": [all_p_tags_text],  # List of all <p> text
    "Paragraphs_HTML": [all_p_tags_html],  # List of all <p> HTML strings
    "Headings": [[heading.text.strip() for heading in headings]],  # List of heading texts
    "Scripts": [[script.get('src').strip() for script in scripts if script.get('src')]]  # List of external script sources
}

# STEP 12: Create a pandas DataFrame
df = pd.DataFrame(data)

# STEP 13: Print the DataFrame for preview
print("\n--- DataFrame Preview ---")
print(df)

# STEP 14: Save the extracted data to a CSV file
df.to_csv("fedr_extracted_data.csv", index=False)
print("\n✅ Data successfully saved to 'fedr_extracted_data.csv'")
