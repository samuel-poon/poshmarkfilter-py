from bs4 import BeautifulSoup
import requests

from .listing import Listing
from .helpers import modify_query_param

from time import sleep
import re
import json

def _get_poshmark_intial_state(url:str) -> dict:
    '''Gets initial state from __INITIAL_STATE__. This can be found in the the page source of any feed outside of the home feed (i.e. https://poshmark.ca/feed).

    Include any query parameters for a more tailored response. Note that this function starts a new session, so sizes must be filtered manually. Using "My Size" will not work.

    Args:
    * url (str): The URL of the Poshmark feed.

    Returns:
    * dict: The __INITIAL_STATE__ JSON object.
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')

    initial_state_script = next((script for script in scripts if script.text.startswith("window.__INITIAL_STATE__")), None)

    if initial_state_script is None:
        raise ValueError('Could not find initial state script.')
    
    script_text = initial_state_script.text
    match = re.search(r"window\.__INITIAL_STATE__\s*=\s*({.*?});", script_text, re.DOTALL)

    if match:
        json_text = match.group(1)
        try:
            return json.loads(json_text) 
        except json.JSONDecodeError as e:
            print("Could not decode window.__INITIAL_STATE__ to JSON:", e)
        
def get_poshmark_listings_data(url:str) -> list[dict]:
    '''Gets Poshmark listings data from a Poshmark feed URL from the __INITIAL_STATE__ JSON object.

    Args:
    * url (str): The URL of the Poshmark feed.

    Returns:
    * list[dict]: A list of dictionaries containing listing data. Each element represents its own listing.
    '''
    initial_state = _get_poshmark_intial_state(url)

    valid_keys = [
        '$_category', # If the feed is by category (i.e. starts with https://poshmark.ca/category/...)
        '$_brand', # If the feed is by brand (i.e. starts with https://poshmark.ca/brand/...)
        '$_search' # If the feed is by search (i.e. starts with https://poshmark.ca/search/...)
    ]
    
    for valid_key in valid_keys:
        if valid_key in initial_state:
            return initial_state[valid_key]['gridData']['data']
    
    raise ValueError(f'Could not find listings data for {url}.')

def get_poshmark_listings(
        url:str,
        count:int           = 100,
        starting_max_id:int = 1,
        delay_seconds:int   = 2
    ) -> list[Listing]:
    '''Loops through Poshmark feed pages until count listings are found.

    Args:
    * url (str): The URL of the Poshmark feed.
    * count (int): The number of listings to find.
    * starting_max_id (int): The starting max_id for the feed.
    * delay_seconds (int): The delay in seconds between each request.

    Returns:
    * list[Listing]: A list of Listing objects.
    '''
    listings = []
    max_id = starting_max_id

    url = modify_query_param(url, 'max_id', max_id)
    poshmark_listings_data = get_poshmark_listings_data(url)

    while len(listings) < count and len(poshmark_listings_data) > 0:
        listings += list(map(lambda x: Listing(x), poshmark_listings_data))

        max_id += 1
        url = modify_query_param(url, 'max_id', max_id)
        sleep(delay_seconds)
        poshmark_listings_data = get_poshmark_listings_data(url)
    
    return listings[:count]