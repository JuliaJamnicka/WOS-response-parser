class Author:
    def __init__(self, given_name, surname, fullname, affiliation_ids, affiliations):
        self.given_name = given_name
        self.surname = surname
        self.fullname = fullname
        self.affiliation_ids = affiliation_ids
        self.affiliations = affiliations

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=1)
    
    def __eq__(self, other):
        if isinstance(other, Author):
            return self.authid == other.authid and self.affiliation == other.affiliation
        return False
    
    def __hash__(self):
        return hash((self.authid, self.affiliation))