# importing the requests library
import requests
import json

# api endpoints
with open("config.json", "r") as f:
    config = json.load(f)

api = config['apiEndpoint']
soldiers_url = api + "/soldiers"
officers_url = api + "/officers/"
carmodels_url = api + "/carmodels?all=true"
specific_carmodel_url = api + "/carmodels/?getcar="
duties_url = api + "/duties/"
carmovements_url = api + "/carmovements/"
enter_url = api + "/customcarmovements/?enter=true"
exit_url = api + "/customcarmovements/?exit=true"
inside_url = api + "/customcarmovements/?inside=true"
outside_url = api + "/customcarmovements/?outside=true"
getlastcar_url = api + "/customcarmovements/?getlast="



# GET requests
def handle_get_requests(URL, rfid=None, PARAMS={}):
    if not rfid:
        data = requests.get(url = URL, params = PARAMS)
    else:
        URL = URL + str(rfid)
        data = requests.get(url = URL, params = PARAMS)
    if data.status_code == 200:
        return data.json()
    elif data.status_code == 404:
        return "Object not found"
    else:
        return "There is error occurred.."

# POST requests
def handle_post_movement(sideMovement, carRFID):
    try:
        car = handle_get_requests(specific_carmodel_url, carRFID)
        data = {
            "car": car[0]['url'],
            "movement": sideMovement,
        }
        response = requests.post(url=carmovements_url, json=data)
        return response.json()
    except:
        print("Error occured in POST request..")
        return "No car found with given RFID"

# print(handle_post_movement("Çykdy", 123))
# print(handle_post_movement("Girdi", 12345))

# print(handle_get_requests(specific_carmodel_url, "177-231-117-29"))

# # get soldiers
# # all
# print(handle_get_requests(soldiers_url))
# # single
# print(handle_get_requests(soldiers_url, 3))
# print(1)

# # get officers
# # all
# print(handle_get_requests(officers_url))
# # single
# print(handle_get_requests(officers_url, 1))
# print(2)

# # get car models
# # all
# print(handle_get_requests(carmodels_url))
# # single
# print(handle_get_requests(carmodels_url, 1))
# print(3)

# # get duties
# # all
# print(handle_get_requests(duties_url))
# # single
# print(handle_get_requests(duties_url, 1))
# print(4)

# # get car movements
# # all
# print(handle_get_requests(carmovements_url))
# # single
# print(handle_get_requests(carmovements_url, 3))
# print(5)

# from dateutil import parser

# s = "2023-01-24T20:59:17.922822+05:00"

# ts = parser.parse(s)
# print(ts.hour)
# print(ts.minute)
# print(ts.second)
