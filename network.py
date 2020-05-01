import requests
import json
from models import KeyValidation,KeyId

base_url = "https://key-api.cfapps.eu10.hana.ondemand.com/api/gate/"

def get_office_info(id):
    req_info = requests.get(base_url+str(id)+"/info")
    req_info_string = req_info.text
    info_array = str(req_info_string).split(";")
    formated_info_array = ["street","city","country"]
    formated_info_array[0] = info_array[0] + " " + info_array[1]
    formated_info_array[1] = info_array[2] + " " + info_array[3]
    formated_info_array[2] = info_array[4]
    return formated_info_array

def validate_token(token,id):
    id_dict = {
        "userId": id.userId,
        "officeId": id.officeId,
        "deviceId": id.deviceId
    }
    id_json = json.dumps(id_dict)
    req_key_validation = requests.post(base_url+"validate/"+token,json= id_json,headers={"Content-Type":"application/json"})
    req_key_validation_json = req_key_validation.json()
    return KeyValidation(req_key_validation_json['succes'],
                         req_key_validation_json['message'],
                         req_key_validation_json['data'])





