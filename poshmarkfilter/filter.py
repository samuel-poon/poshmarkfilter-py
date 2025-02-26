from typing import Type, Any

class Filter:
    def __init__(
            self,
            name: str,
            description: str,
            type_annotation: Type[Any]
        ):
        '''Filter class for creating custom filters.

        Do not assume that the model will understand what you are looking for on the name alone. The description is where you should be defining the
        criteria for the filter.

        Args:
        * name (str): The name of the filter.
        * description (str): The description of the filter.
        * type_annotation (Type[Any]): The type annotation for the filter. This is used to generate the response format model.

        ------------------------------------------------------------------------------------------------------------------------------------------------------------
        A few examples...
        Filter example #1: Lapel style
        * name: lapel_style
        * description: The style of the lapel on the jacket. Options include 'notch', 'peak', and 'shawl'.
        * type_annotation: Literal['notch', 'peak', 'shawl']

        Filter example #2: Material
        * name: material
        * description: The material of the garment. Options include 'cotton', 'wool', 'polyester', 'silk', and 'other'.
        * type_annotation: Literal['cotton', 'wool', 'polyester', 'silk', 'other']

        Filter example #3: Pit-to-pit
        * name: pit_to_pit
        * description: The pit-to-pit measurement of the garment in inches, rounded to the nearest integer. Prioritize the measurement in the description over
        the images. If it is not provided, return 0.
        * type_annotation: int
        '''
        self.name = name
        self.description = description
        self.type_annotation = type_annotation