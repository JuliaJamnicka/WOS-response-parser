from Models.article import Article
from Models.author import Author
from Models.organization import Organization

def get_publications(parsed_json, grant_number):
    articles = []
    for entry in parsed_json['Data']['Records']['records']['REC']:
                article = Article(
                    uid=entry['UID'],
                    name=next((title['content'] for title in entry['static_data']['summary']['titles']['title'] if title["type"] == "item"), ''),
                    date=entry['static_data']['summary']['pub_info']['sortdate'],
                    citedBy=sum(entry["local_count"] for entry in entry["dynamic_data"]["citation_related"]["tc_list"]["silo_tc"]),
                    field=entry['static_data']["fullrecord_metadata"].get("category_info", {}).get("headings", {}).get("heading", ''),
                    doi=parse_article_links(entry['dynamic_data']['cluster_related']['identifiers'], "doi"),
                    issn=parse_article_links(entry['dynamic_data']['cluster_related']['identifiers'], "issn"),
                    isbn=parse_article_links(entry['dynamic_data']['cluster_related']['identifiers'], "isbn"),
                    grant_number=grant_number,
                    fund_text=""
                )
                
                article.authors = get_authors(entry)
                article.affiliations = get_affiliations(entry, article.authors)

                articles.append(article)
    
    return articles

def parse_article_links(identifiers, link_type):
        return next((ident['value'] for ident in identifiers["identifier"] if not isinstance(ident, str) and ident.get("type", '') == link_type), '')

def get_affiliations(entry, authors):
    affiliations = []

    if entry['static_data']["fullrecord_metadata"]["addresses"]["count"] == 0:
        return

    address_names = entry['static_data']["fullrecord_metadata"]["addresses"]["address_name"]
    for address in address_names:
        if (isinstance(address, str)):
            continue
        addr_no = address.get("address_spec", {}).get("addr_no", 0)
        organizations = address.get("address_spec", {}).get("organizations", {}).get("organization", [])

        preferred_org = next((org for org in organizations if org.get("pref") == "Y"), None)
        org_name = preferred_org.get("content") if preferred_org else address.get("address_spec", {}).get("full_address", "")

        affiliation = Organization( 
            addr_no=addr_no,
            name=org_name,
            city=address['address_spec']["city"],
            country=address["address_spec"]["country"],
            address=address["address_spec"]["full_address"]
        )
        
        affiliations.append(affiliation)

    for author in authors:
        affs =  [aff for aff in affiliations if str(aff.addr_no) in author.affiliation_ids]
        author.affiliations = affs


    return affiliations


def get_authors(entry):
    authors = []

    names = entry["static_data"]["summary"]["names"]["name"]
    for name in names:
        if isinstance(name, str):
            continue
        author = Author(
            given_name=name.get('first_name', ''),
            surname=name.get('last_name', ''),
            fullname=name.get('display_name', ''),
            affiliation_ids=str(name.get("addr_no", "")).split() if "addr_no" in name else [],
            affiliations=[]
        )
        if (author.fullname in [author.fullname for author in authors]):
            for auth in authors:
                if (auth.fullname == author.fullname):
                    auth.affiliation_ids += author.affiliation_ids
        elif author.fullname != '':
            authors.append(author)

    return authors
