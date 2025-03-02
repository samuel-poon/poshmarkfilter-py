from typing import Iterable
import os

from openai import OpenAI
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from pydantic import create_model

from .config import DEFAULT_MODEL
from .listing import Listing
from .filter import Filter

def scan_listing(
        listing: Listing,
        filters: Iterable[Filter],
        include_cover_shot: bool        = True,
        include_all_pictures: bool      = False,
        openai_client: OpenAI | None    = None,
        model: str                      = DEFAULT_MODEL,
        detail: str                     = 'low',
        max_tokens: int | None          = None,
    ) -> ParsedChatCompletion:
    '''
    Given a Listing object and a list of Filters, generates a chat completion using OpenAI's API.

    Args:
    * listing (Listing): The Listing object to scan.
    * filters (Iterable[Filter]): An iterable of Filter objects to use as criteria for the completion (see Filter class for more information).
    * include_cover_shot (bool): Whether to include the cover shot image in the completion. Defaults to True.
    * include_all_pictures (bool): Whether to include all pictures in the completion. Defaults to False. It is highly recommended to keep this as False as images can be expensive to process.
    * openai_client (OpenAI): An OpenAI client object. If not provided, the function will attempt to use the OPENAI_API_KEY environment variable to create a new client.
    * model (str): The model to use for the completion. If not provided, the function will attempt to use the OPENAI_MODEL environment variable.
    * detail (str): The detail level of the images to include in the completion. One of 'low', 'medium', or 'high'. Defaults to 'low'.
    * max_tokens (int): The maximum number of tokens to generate in the completion. If not provided, the completion will generate as many tokens as necessary to complete the prompt.

    Returns:
    * ParsedChatCompletion: A ParsedChatCompletion object representing the completion.
    '''
    
    if openai_client is None:
        if 'OPENAI_API_KEY' in os.environ:
            openai_client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            raise ValueError('An openai_client object must be provided as an argument or an OPENAI_API_KEY environment variable must be set.')
    
    cover_shot_url = listing.cover_shot['url']
    pictures_urls = list(map(lambda x: x['url'], listing.pictures))

    image_urls = []

    if include_cover_shot:
        image_urls.append(cover_shot_url)

    if include_all_pictures:
        image_urls.extend(pictures_urls)
        
    prompt = f'Here are some details regarding a listing on Poshmark.\n\nTITLE: {listing.title}.\n\nDESCRIPTION: {listing.description}\n\nGiven the following criteria, return a JSON object in the following format.\n'
    
    prompt += '{'
    prompt += ','.join([f'"{filter.name}": {filter.description}' for filter in filters])
    prompt += '}'

    
    # Need this to create the response format model 
    response_format_fields = {}
    for filter in filters:
        response_format_fields[filter.name] = (filter.type_annotation, ...)
    
    ResponseFormatModel = create_model('ResponseFormatModel', **response_format_fields)

    chat_completion = openai_client.beta.chat.completions.parse(
        model=model,
        messages=[{
            'role':'user',
            'content': [
                {'type': 'text', 'text': prompt},
                *[{'type': 'image_url', 'image_url': {'url':url, 'detail': detail}} for url in image_urls]
            ]
        }],
        response_format=ResponseFormatModel,
        max_tokens=max_tokens
    )

    return chat_completion