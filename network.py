import requests

base_url = "https://key-api.cfapps.eu10.hana.ondemand.com/api/"

def get_auth_ids_by_office_id(id):
    office_id=id

    req_auth_ids = requests.get(base_url+"gate/"+str(office_id)+"/authorized")

    req_auth_ids_json = req_auth_ids.json()

    auth_ids = []
    for id in req_auth_ids_json:
        auth_ids.append(id)
    return auth_ids

def get_office_info(id):
    req_info = requests.get(base_url+"gate/"+str(id)+"/info")
    req_info_string = req_info.text
    info_array = str(req_info_string).split(";")
    return info_array


