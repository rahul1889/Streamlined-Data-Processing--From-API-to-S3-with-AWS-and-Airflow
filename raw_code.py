import requests
import json
import pandas as pd

URL = "https://api.beta.ons.gov.uk/v1/datasets"
response = requests.get(URL)
json_data = json.loads(response.text)

items = json_data["items"]

for item in items:
    print(f"ID: {item['id']}")
    print(f"Description: {item['description']}")

    # Extract and print contacts
    for contact in item['contacts']:
        print(f"Contact: {contact['name']} ({contact['email']}, {contact['telephone']})")

    # Extract and print keywords
    if 'keywords' in item:
        keywords = item['keywords']
        print(f"Keywords: {keywords}")
    else:
        print("No keywords available.")

    # Extract and print links
    print(f"Editions Link: {item['links']['editions']['href']}")
    print(f"Latest Version Link: {item['links']['latest_version']['href']}")
    print(f"Taxonomy Link: {item['links']['taxonomy']['href']}")

    # Extract and print methodologies link if present
    if 'methodologies' in item['links']:
        print(f"Methodologies Link: {item['links']['methodologies']['href']}")
    else:
        print("No methodologies link available.")

    # Extract and print methodology details
    for methodology in item.get('methodologies', []):
        print(f"Methodology: {methodology.get('title', 'N/A')}")
        print(f"National Statistic: {methodology.get('national_statistic', 'N/A')}")
        print(f"Next Release: {methodology.get('next_release', 'N/A')}")
        print(f"QMI: {methodology.get('qmi', 'N/A')}")
        print("\n")

    if 'release_frequency' in item:
        release_frequency = item['release_frequency']
        print(f"Release_frequency: {release_frequency}")
    else:
        print(f"No release_frequency available.")

    if 'state' in item:
        state = item['state']
        print(f"state: {state}")
    else:
        print("No state field available")
    if 'title' in item:
        title = item['title']
        print(f"Title: {title}")

        

        

    print("=" * 50)  # Separating each item for clarity

