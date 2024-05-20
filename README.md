## Web of Science API rsponse parser

The Functions App calls the ```get_publications``` function to parse the response from a Web of Science API Expanded query, and after processing all of the publications returns the equivalent CSV file with header: 
```'UID', 'Title', 'Publication Date', 'Cited By', 'DOI', 'ISSN', 'ISBN', 'Research Areas', 'Grant Number', 'Funding Text', 'Author Given Name', 'Author Surname', 'Author Full Name', 'Affiliation Address Numbers',
'Address Number', 'Organization Name', 'Organization Country', 'Organization City', 'Organization Address'```.
