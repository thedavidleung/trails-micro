import pika
import json
import requests

def fetch_trails_data(lat, long):
    trails_url = "https://trailapi-trailapi.p.rapidapi.com/trails/explore/"
    trails_querystring = {
        "lat": lat,
        "lon": long,
        "per_page": "10",
        "radius": "50"
    }
    trails_headers = {
        "X-RapidAPI-Key": "959061f318msh5ec12e3da05c92cp180c84jsn32e6297cffac",
        "X-RapidAPI-Host": "trailapi-trailapi.p.rapidapi.com"
    }

    # Request trail data
    trails_response = requests.get(trails_url, headers=trails_headers, params=trails_querystring)
    if trails_response.status_code == 200:
        trails_info = trails_response.json()['data']
        trails_dict = {}
        for trail in trails_info:
            name = trail['name']
            description = trail['description']
            trails_dict[name] = description
        return trails_dict
    else:
        return None

def get_trails_data(address):
    # Geocoding API request
    geocoding_url = "https://trueway-geocoding.p.rapidapi.com/Geocode"
    geocoding_querystring = {"address": address, "language": "en"}
    geocoding_headers = {
        "X-RapidAPI-Key": "959061f318msh5ec12e3da05c92cp180c84jsn32e6297cffac",
        "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
    }
    
    # Requesting geolocation data
    response = requests.get(geocoding_url, headers=geocoding_headers, params=geocoding_querystring)

    # Checking if the request was successful
    if response.status_code == 200:
        geocoding_data = response.json()
        if 'results' in geocoding_data and geocoding_data['results']:
            lat = geocoding_data['results'][0]['location']['lat']
            long = geocoding_data['results'][0]['location']['lng']
            print("Latitude:", lat)
            print("Longitude:", long)

            # Fetching trails data based on geolocation
            trails_data = fetch_trails_data(lat, long)
            return trails_data
        else:
            print("No geocoding results found")
            return None
    else:
        print("Failed to retrieve geocoding data. Status code:", response.status_code)
        return None


if __name__ == "__main__":
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='addresses')

    def callback(ch, method, properties, body):
        address_data = json.loads(body)
        address = address_data['address']

        trails_data = get_trails_data(address)
        if trails_data:
            print(f'Trails within 50 miles of {address}:')
            for trail_name, trail_description in trails_data.items():
                print(f"Trail: {trail_name}\n")
                print(f"Description: {trail_description}\n")
        else:
            print("No trail data found")

    channel.basic_consume(queue='addresses', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
