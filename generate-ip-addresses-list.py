import requests
import random
import socket
import struct

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def generate_ip_address():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/200.34.24.56/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def get_locations():
    f = open("ip_addresses_with_countries.txt", "a")
    f.write(f"IP Address,Country\n")
    f.close()

    for _ in range(100):
        ip_address = generate_ip_address()
        response = requests.get(f"https://ipapi.co/{ip_address}/json").json()
        if not(response.get("city")):
            continue
        else: 
            f = open("ip_addresses_with_countries.txt", "a")
            f.write(f"{ip_address},{response.get('country_name')}\n")

        f.close()


get_locations()