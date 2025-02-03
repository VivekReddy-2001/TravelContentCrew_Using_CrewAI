import re
import spacy
import requests
import os 
from dotenv import load_dotenv
load_dotenv(override=True)

def pattern_match(text):
    """
        Returns the exact match of the text we wanted to generate the images for the landmark.
    """

    pattern = r"\*\*5\. Key Activities and Itineraries:\*\*([\s\S]*?)(?=\n\*\*\d+\.|\Z)"

    match = re.search(pattern, text)
    if match:
        extracted_text = match.group(1).strip()
        print(extracted_text)
    else:
        print("Section not found.")
    
    return extracted_text 

def named_entity_recog(text):
    """
        Gets the extract text from the recommends and finds the landmarks from it.
    """
    # small english NER model
    ner_model = spacy.load("en_core_web_sm")
    doc = ner_model(text=text)

    landmarks = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC', 'FAC']] 
    if landmarks:
        return landmarks 
    else:
        print("No landmarks found !!") 
        return [] 

import os
import requests

def fetch_photos_for_cities(city_names, api_key, base_folder="City_Photos", max_photos=3):
    """Fetches up to `max_photos` for each city and saves them in respective folders."""
    
    os.makedirs('D:/make_my_trip/TravelContentCrew_Using_CrewAI/src/city_images', exist_ok=True)  # Ensure the base folder exists

    for city in city_names:
        city_folder = os.path.join(base_folder, city.replace(" ", "_"))
        os.makedirs(city_folder, exist_ok=True)  # Create folder for each city
        
        # Step 1: Get Place ID
        geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={api_key}"
        geo_response = requests.get(geo_url).json()
        
        if not geo_response.get("results"):
            print(f"❌ Place not found: {city}")
            continue
        
        place_id = geo_response["results"][0]["place_id"]
        print(f"🔹 Place ID for {city}: {place_id}")

        # Step 2: Get Photo References
        places_url = f"https://places.googleapis.com/v1/places/{place_id}"
        headers = {"X-Goog-Api-Key": api_key}
        params = {"fields": "photos"}
        
        places_response = requests.get(places_url, headers=headers, params=params).json()
        
        if "photos" not in places_response:
            print(f"❌ No photos available for {city}.")
            continue
        
        photo_references = [photo["name"] for photo in places_response["photos"][:max_photos]]

        # Step 3: Download Photos
        for i, photo_reference in enumerate(photo_references):
            photo_url = f"https://places.googleapis.com/v1/{photo_reference}/media?maxWidthPx=800&key={api_key}"
            photo_response = requests.get(photo_url)

            if photo_response.status_code == 200:
                filename = os.path.join(city_folder, f"{city.replace(' ', '_')}_photo_{i+1}.jpg")
                with open(filename, "wb") as file:
                    file.write(photo_response.content)
                print(f"✅ Saved: {filename}")
            else:
                print(f"❌ Failed to download photo {i+1} for {city}")


text = """
Some introduction text...

**5. Key Activities and Itineraries:**

   - **Day 1**:
     - Morning: Arrive in Los Angeles. Visit Griffith Observatory for panoramic city views.
     - Afternoon: Explore Hollywood Boulevard and the Walk of Fame.
     - Evening: Dine at a local restaurant and visit Santa Monica Pier.

   - **Day 2**:
     - Morning: Drive to San Francisco (approximately 6 hours if opting for this route). Alternatively, fly for faster transit.
     - Afternoon: Explore Alcatraz Island or walk across the Golden Gate Bridge.
     - Evening: Enjoy dinner at Fisherman’s Wharf and explore Union Square.

Some other text...
"""
def recommends(text):
    extracted_text = pattern_match(text)
    cities = named_entity_recog(extracted_text)
    fetch_photos_for_cities(cities, os.getenv('GOOGLE_PLACES_API'))
