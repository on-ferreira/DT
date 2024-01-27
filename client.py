import requests
import time

while True:
    try:
        response = requests.get('http://127.0.0.1:5000/a')
        if response.status_code == 200:
            current_time = response.json()['time']
            print(f"Current time: {current_time}")
        else:
            print(f"Failed to fetch time. Status code: {response.status_code}")
    except requests.ConnectionError:
        print("Connection error. Make sure the server is running.")
    
    time.sleep(5)