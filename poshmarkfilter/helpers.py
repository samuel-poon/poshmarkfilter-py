
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def modify_query_param(url:str, param:str, value:str):
    '''Takes a URL and modifies a query parameter with a new value. If the query parameter does not exist, it is added.

    Args:
    * url (str): The URL to modify.
    * param (str): The query parameter to modify.
    * value (str): The new value for the query parameter.

    Returns:
    * str: The modified URL.
    '''
    parsed_url = urlparse(url)

    # Get the query param as a dict, update inside the dict
    query_params = parse_qs(parsed_url.query)
    query_params[param] = [value]
    
    new_query_string = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed_url._replace(query=new_query_string))

    return new_url