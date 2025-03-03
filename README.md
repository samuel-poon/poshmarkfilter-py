# poshmarkfilter

A Python library for creating custom filters on Poshmark. Use AI to extract (virtually) any information you want from a Poshmark listing.

## Requirements
* Python 3.11+
* An [OpenAI API key](https://openai.com/api/)

## Installation
```bash
pip3 install git+https://github.com/samuel-poon/poshmarkfilter-py
```

## Quick start
Include `OPENAI_API_KEY` in your environment variables. See `.env.example` for reference.

It is highly recommended that you store your API keys in a `.env` file and load them through [python-dotenv](https://pypi.org/project/python-dotenv/).

```python
from typing import Literal
import json

from dotenv import load_dotenv
from poshmarkfilter import get_poshmark_listings, scan_listing, Filter

filters = [
    Filter(
        name='lapel_style',
        description='The style of the lapel on the jacket. Options include "notch", "peak", and "shawl".',
        type_annotation=Literal['notch', 'peak', 'shawl']
        ),
    Filter(
        name='material',
        description='The material of the garment. Options include "cotton", "wool", "polyester", "silk", and "other".',
        type_annotation=Literal['cotton', 'wool', 'polyester', 'silk', 'other']
        ),
    Filter(
        name='pit_to_pit',
        description='The pit-to-pit measurement of the garment in inches, rounded to the nearest integer. Prioritize the measurement in the description over the images. If it is not provided, return 0.',
        type_annotation=int
    )
]

listings = get_poshmark_listings('https://poshmark.ca/category/Men-Suits_&_Blazers-Sport_Coats_&_Blazers?size%5B%5D=40R', count=10)

results = {}
for listing in listings:
    chat_completion = scan_listing(listing, filters=filters) # Returns a ParsedChatCompletion object
    filtered_result = json.loads(chat_completion.choices[0].message.content)
    
    results[listing.url] = filtered_result

print(json.dumps(results, indent=4)) # Pretty print results
```

## A closer look
### Filter
The core of `poshmarkfilter` is the `Filter` object. This is how you define the criteria you want to filter for. In the example above, I filter for lapel style, material, and the pit-to-pit measurement of the jacket.

`Filter` takes a `name`, `description`, and a [`type_annotation`](https://runestone.academy/ns/books/published/fopp/Functions/TypeAnnotations.html). Any `type_annotation` compatible with [`pydantic`](https://docs.pydantic.dev/latest/) should work.


### get_poshmark_listings
`get_poshmark_listings` gets the first `count` listings from a Poshmark feed in a `url`. Returns a list of `Listing` objects.

```python
poshmark_listings = get_poshmark_listings(
    url='https://poshmark.ca/link/to/feed', # Mandatory (str), the URL of the Poshmark feed to retrieve listings from
    count=100,                              # Optional (int, default=100), the number of listings to retrieve
    starting_max_id=1,                      # Optional (int, default=1), the starting page to retrieve listings from
    delay_seconds=2,                        # Optional (int, default=2), the delay between each page request
)
```

Recommendations:
* For best results, use `get_poshmark_listings` in conjunction with the existing filters on Poshmark. In the quick start example, I have filtered for Men's Suits & Blazers, Sports Coats & Blazers, in a size 40R.
* This library does not have access to your account. You must manually filter for your size as "My Size" will not work.
<img width="298" alt="image" src="https://github.com/user-attachments/assets/65b5856f-4943-430b-8ebf-d5e4480a2199" />

* `get_poshmark_listings` returns the first `count` listings. If you are not scanning every listing, consider how you sort the results.
<img width="1085" alt="image" src="https://github.com/user-attachments/assets/c0d90a8e-75ed-4092-b848-fa8ad07c77ec" />

### scan_listing
`scan_listing` takes a `Listing` and filters them based on `filters`. Returns a [`ParsedChatCompletion`](https://github.com/openai/openai-python/blob/main/helpers.md) object whose message content is `{"filter_name_1":"filter_1_result", "filter_name_2":"filter_2_result",...}`.

```python
chat_completion = scan_listing(
    listing=listing,            # Mandatory (poshmarkfilter.Listing), the Listing object to scan
    filters=filters,            # Mandatory (Iterable[poshmarkfilter.Filter]), the filters to include in the chat completion
    include_cover_shot=True,    # Optional (bool, default=True), if True, includes the cover shot in the prompt.
    include_all_pictures=False, # Optional (bool, default=False), if True, includes all pictures in the prompt.
    openai_client=None,         # Optional (openai.Client), the OpenAI client to use. If None, creates an OpenAI client using the OPENAI_API_KEY environment variable.
    model='gpt-4o-mini',        # Optional (str, default='gpt-4o-mini'), the OpenAI model to use.
    detail='low',               # Optional (str, default='low'), the detail level of the OpenAI model. Options include 'low', 'medium', and 'high'.
    max_tokens=None             # Optional (int | None, default=None), the maximum number of tokens to generate.
)
```

Recommendations:
* At a minimum, all listings scanned through `scan_listing` will include the title and description of the listing. By default, this function will also provide the cover shot to the model, but if this is unnecessary, I recommmend setting `include_cover_shot` to `False`.
* Unless you absolutely need to include all pictures in the prompt (e.g. for specific measurements), I recommend keeping `include_all_pictures` to `False`. Setting this to `True` can be expensive.

## Estimating costs
Based on my personal usage, scanning a listing using `gpt-4o-mini` with `include_cover_shot=True` and `include_all_pictures=False` at `detail=low` (the default options) consumes roughly 3k input tokens. Assuming that each completion takes 20 output tokens, this means each call costs ~$0.0005 or $0.46/1000 calls.

If the filter can be processed using the title and description of the listing alone, you can drastically reduce the cost by excluding all photos from the scan.
