import json
    
class Organization:
    def __init__(self, addr_no, name, country, city, address):
        self.addr_no = addr_no
        self.name = name
        self.country = country
        self.city = city
        self.address = address

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=1)