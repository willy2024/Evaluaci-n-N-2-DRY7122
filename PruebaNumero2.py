import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "af6919c1-d5fe-468c-af78-19d41b7b3469"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")
        
        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name
        
        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de Ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc

while True:
    loc1 = input("Ubicación de Inicio: ")
    if loc1.lower() == "quit" or loc1.lower() == "q":
        break

    orig = geocoding(loc1, key)
    loc2 = input("Destino: ")
    if loc2.lower() == "quit" or loc2.lower() == "q":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de Enrutamiento: " + str(paths_status) + "\nURL de la API de Enrutamiento:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")
        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia Recorrida: {0:.2f} km".format(km))
            print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))

            # Calcular el combustible requerido suponiendo 10 km/litro
            fuel_liters = km / 10
            print("Combustible Requerido: {0:.2f} litros".format(fuel_liters))

            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ({1:.2f} km)".format(path, distance / 1000))
            print("=============================================")
