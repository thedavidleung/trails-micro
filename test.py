import time
import sending
import receiving

# Define the park address you want to send
park_address = "Central Park"

# Send the park address
sending.get_park(park_address)

time.sleep(10) 

# Get and print the trails data
trails_data = receiving.get_trails_data(park_address)
if trails_data:
    print(f'Trails within 50 miles of {park_address}:')
    for trail_name, trail_description in trails_data.items():
        print(f"Trail: {trail_name}\n")
        print(f"Description: {trail_description}\n")
else:
    print("No trail data found")
