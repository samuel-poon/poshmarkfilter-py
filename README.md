# poshmarkfilter

A Python library for creating custom filters on Poshmark. Extract (virtually) any information you want from a Poshmark listing.

## Requirements
* Python 3.11+
* An [OpenAI API key](https://openai.com/api/)

## Installation
```bash
pip3 install git+https://github.com/samuel-poon/poshmarkfilter-py
```

## Quick start
Include `OPENAI_API_KEY` and `DEFAULT_MODEL` in your environment variables. See `.env.example` for reference.

```python
from typing import Literal
import json

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


