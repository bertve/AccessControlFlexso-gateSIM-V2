
class KeyValidation:
    def __init__(self,succes,message,data):
        self.succes = succes
        self.message = message
        self.data = data


class KeyId:
    def __init__(self,userId,officeId,deviceId):
        self.userId = userId
        self.officeId = officeId
        self.deviceId = deviceId

class Address:
    def __init__(self,street,house_number,postal_code,city,country):
        self.steet = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.country = country

    def to_format_string(self):
        return self.steet + " " + self.house_number + "\n" + self.postal_code + " " + self.city + "\n" + self.country
