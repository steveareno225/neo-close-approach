import requests

# URL for NASA's Close Approach Data API
url = "https://ssd-api.jpl.nasa.gov/cad.api?dist-max=0.2AU&date-min=1900-01-01&date-max=2200-12-31&fullname=true&sort=dist"

# Filename to save the result
output_file = "cad.customization.json"

try:
    print("Fetching data from NASA JPL API...")
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Write response content to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print(f"✅ Data saved to '{output_file}'")

except requests.RequestException as e:
    print(f"❌ Error fetching data: {e}")
