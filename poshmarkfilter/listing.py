import re

class Listing:
    def __init__(
            self,
            listing_json: dict
        ):

        self._listing_json = listing_json

    @property
    def id(self) -> str:
        return self._listing_json['id']
    
    @property
    def title(self) -> str:
        return self._listing_json['title']
    
    @property
    def description(self) -> str:
        return self._listing_json['description']
    
    @property
    def brand(self) -> str:
        return self._listing_json['brand']

    @property
    def size(self) -> str:
        return self._listing_json['size']

    @property
    def status_change_at(self) -> str:
        return self._listing_json['status_changed_at']
    
    @property
    def price_amount(self) -> float:
        return self._listing_json['price_amount']['val']
    
    @property
    def origin_domain(self) -> str:
        return self._listing_json['origin_domain']
    
    @property
    def currency_code(self) -> str:
        return self._listing_json['price_amount']['currency_code']
        
    @property
    def department(self) -> str:
        return self._listing_json['catalog']['department_obj']['slug']
    
    @property
    def category(self) -> str:
        return self._listing_json['catalog']['category_obj']['slug']
    
    @property
    def catalog_features(self) -> list[str]:
        return list(map(lambda x: x['slug'], self._listing_json['catalog']['category_feature_objs']))

    @property
    def cover_shot(self) -> dict:
        return self._listing_json['cover_shot']

    @property
    def pictures(self) -> list[dict]:
        return self._listing_json['pictures']
    
    @property
    def url(self) -> str:
        '''
        Generates a Poshmark URL for the listing. This is not explicitly provided in the JSON data so we need to generate this manually.

        Need to test this more to ensure it works for all cases.
        '''
        DOMAIN_TO_TLD = {
            'ca': 'ca',
            'us': 'com'
        }

        tld = DOMAIN_TO_TLD[self.origin_domain]
        
        # Removes all punctuation marks from the title
        modified_title = re.sub(r'[^a-zA-Z0-9 ]', '', self.title)
        modified_title = modified_title.replace(' ', '-')

        return f'https://poshmark.{tld}/listing/{modified_title}-{self.id}'