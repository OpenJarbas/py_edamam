class APIError(Exception):
    """ raised when api requests fail """


class LowQualityQuery(APIError):
    """ raised when query is not understood """


class InvalidKey(APIError):
    """ raised when keys are invalid """


class InvalidFoodApiKey(InvalidKey):
    """ raised when food api keys are invalid """


class InvalidRecipeApiKey(InvalidKey):
    """ raised when recipe api keys are invalid """


class InvalidNutrientsApiKey(InvalidKey):
    """ raised when nutrients api keys are invalid """
