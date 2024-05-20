import csv
import io
import azure.functions as func
import logging

from parse_methods import get_publications

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="wos_parser")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        grant_number = req.params.get('grantNumber', '')
        include_header = req.params.get('includeHeader', False)
        articles = get_publications(req_body, grant_number)
    except ValueError:
        pass

    field_names = [
        'UID', 'Title', 'Publication Date', 'Cited By', 'DOI', 'ISSN', 'ISBN', 'Research Areas', 'Grant Number', 'Funding Text',
        'Author Given Name', 'Author Surname', 'Author Full Name', 'Affiliation Address Numbers',
        'Address Number', 'Organization Name', 'Organization Country', 'Organization City', 'Organization Address'
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=field_names)

    if include_header:
        writer.writeheader()
    
    for article in articles:
        for author in article.authors:
            for affiliation in author.affiliations:
                row_data = {
                    'UID': article.uid,
                    'Title': article.name,
                    'Publication Date': article.date,
                    'Cited By': article.citedBy,
                    'DOI': article.doi,
                    'ISSN': article.issn,
                    'ISBN': article.isbn,
                    'Research Areas': article.field,
                    'Grant Number': article.grant_number,
                    'Funding Text': article.fund_text,
                    'Author Given Name': author.given_name,
                    'Author Surname': author.surname,
                    'Author Full Name': author.fullname,
                    'Affiliation Address Numbers': ", ".join(author.affiliation_ids),
                    'Address Number': affiliation.addr_no if affiliation else '',
                    'Organization Name': affiliation.name if affiliation else '',
                    'Organization Country': affiliation.country if affiliation else '',
                    'Organization City': affiliation.city if affiliation else '',
                    'Organization Address': affiliation.address if affiliation else ''
                }
                writer.writerow(row_data)

    csv_content = output.getvalue()
    output.close()

    return func.HttpResponse(
        body=csv_content,
        status_code=200,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="data.csv"'
        }
    )