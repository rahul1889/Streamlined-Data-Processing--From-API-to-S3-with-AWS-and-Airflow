import requests
import json
import pandas as pd
import s3fs

def extract_field(item, field_name, default='N/A'):
    if item is not None and isinstance(item, dict):
        field_value = item.get(field_name, default)
        return field_value
    else:
        return default

URL = "https://api.beta.ons.gov.uk/v1/datasets"
response = requests.get(URL)
json_data = json.loads(response.text)

items = json_data["items"]

data_list = []

for item in items:
    data = {
        "ID": extract_field(item, 'id'),
        "Description": extract_field(item, 'description')
    }

    # Extract and append contacts
    for i, contact in enumerate(item.get('contacts', []), start=1):
        data[f"Contact {i} Name"] = extract_field(contact, 'name', 'Contact')
        data[f"Contact {i} Email"] = extract_field(contact, 'email', 'N/A')
        data[f"Contact {i} Telephone"] = extract_field(contact, 'telephone', 'N/A')

    # Extract and append keywords
    data["Keywords"] = extract_field(item, 'keywords', 'No keywords available')

    # Extract and append links
    data["Editions Link"] = extract_field(item['links']['editions'], 'href', 'No editions link available')
    data["Latest Version Link"] = extract_field(item['links']['latest_version'], 'href', 'No latest version link available')
    data["Taxonomy Link"] = extract_field(item['links']['taxonomy'], 'href', 'No taxonomy link available')

    # Extract and append methodologies link if present
    data["Methodologies Link"] = extract_field(item['links'].get('methodologies'), 'href', 'No methodologies link available')

    # Extract and append methodology details
    for i, methodology in enumerate(item.get('methodologies', []), start=1):
        data[f"Methodology {i} Title"] = extract_field(methodology, 'title', 'N/A')
        data[f"Methodology {i} National Statistic"] = extract_field(methodology, 'national_statistic', 'N/A')
        data[f"Methodology {i} Next Release"] = extract_field(methodology, 'next_release', 'N/A')
        data[f"Methodology {i} QMI"] = extract_field(methodology, 'qmi', 'N/A')

    # Extract and append additional fields
    data["Release Frequency"] = extract_field(item, 'release_frequency', 'No release frequency available')
    data["State"] = extract_field(item, 'state', 'No state field available')
    data["Title"] = extract_field(item, 'title', 'No title available')

    data_list.append(data)

# Create DataFrame
df = pd.DataFrame(data_list)

# Save to CSV
df.to_csv("s3:path")
