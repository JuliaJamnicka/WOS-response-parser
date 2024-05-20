import json

class Article:
    def __init__(self, uid, name, date, citedBy, doi, issn, isbn, field, grant_number, fund_text, authors = [], affiliations = []):
        self.uid = uid
        self.name = name
        self.date = date
        self.citedBy = citedBy
        self.field = field
        self.doi = doi
        self.issn = issn
        self.isbn = isbn
        self.grant_number = grant_number
        self.fund_text = fund_text
        self.authors = authors
        self.affiliations = affiliations

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=1)