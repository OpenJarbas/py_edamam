import requests
import json
import logging

from py_edamam.exceptions import APIError, InvalidFoodApiKey, \
    InvalidNutrientsApiKey, InvalidRecipeApiKey, LowQualityQuery

logger = logging.getLogger("PyEdamam")


class Edamam(object):
    """ low level api returning raw json data"""

    def __init__(self,
                 # keys scrapped from web demos
                 nutrition_appid="47379841",
                 nutrition_appkey="d28718060b8adfd39783ead254df7f92",
                 recipes_appid=None, recipes_appkey=None,
                 food_appid="07d50733",
                 food_appkey="80fcb49b500737827a9a23f7049653b9"
                 ):
        self.nutrition_appid = nutrition_appid
        self.nutrition_appkey = nutrition_appkey
        self.recipes_appid = recipes_appid
        self.recipes_appkey = recipes_appkey
        self.food_appid = food_appid
        self.food_appkey = food_appkey

    def search_recipe(self, query="chicken"):
        url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + \
              self.recipes_appid + '&app_key=' + \
              self.recipes_appkey

        r = requests.get(url)
        if r.status_code == 401:
            logger.error("invalid recipe api key")
            raise InvalidRecipeApiKey
        return r.json()

    def search_nutrient(self, ingredients=None):
        ingredients = ingredients or []
        if isinstance(ingredients, str):
            ingredients = [ingredients]

        url = 'https://api.edamam.com/api/nutrition-details?app_id={id}' \
              '&app_key={key}'.format(id=self.nutrition_appid,
                                      key=self.nutrition_appkey)

        data = {"ingr": ingredients}
        r = requests.post(url,
                          headers={"Content-Type": "application/json"},
                          data=json.dumps(data))

        if r.status_code == 401:
            logger.error("invalid nutrients api key")
            raise InvalidNutrientsApiKey

        data = r.json()
        if data.get("error"):
            if data["error"] == "low_quality":
                logger.error("could not understand query")
                raise LowQualityQuery
            else:
                raise APIError
        return data

    def search_food(self, query="pizza"):
        url = 'https://api.edamam.com/api/food-database/parser?nutrition' \
              '-type=logging&ingr={query}&app_id={id}&app_key={key}' \
            .format(id=self.food_appid, key=self.food_appkey, query=query)

        r = requests.get(url)
        if r.status_code == 401:
            logger.error("invalid food api key")
            raise InvalidFoodApiKey

        r = r.json()
        if r.get("status") == "error":
            error = r.get("message")
            if not error:
                error = "Api request failed"
            logger.error(error)
            raise APIError
        return r


class PyEdamam(Edamam):
    """ High level api generating data objects"""

    def search_recipe(self, query):
        data = super().search_recipe(query)
        hits = data["hits"]
        for hit in hits:
            data = hit["recipe"]
            data["yields"] = data["yield"]
            data.pop("yield")
            data["ingredient_names"] = data["ingredientLines"]
            data.pop("ingredientLines")
            data["share_url"] = data["shareAs"]
            data.pop("shareAs")
            yield Recipe(edamam=self, **data)

    def search_nutrient(self, ingredients=None):
        ingredients = ingredients or []
        if isinstance(ingredients, str):
            ingredients = [ingredients]
        for ing in ingredients:
            data = super().search_nutrient(ing)
            data["yields"] = data["yield"]
            data.pop("yield")
            yield Ingredient(name=ing, **data)

    def search_food(self, query):
        data = super().search_food(query)
        for food in data["parsed"]:
            yield Food(measure=food["measure"],
                       quantity=food["quantity"],
                       **food["food"])


# Data classes
class Measure:
    def __init__(self, label, uri):
        self.label = label
        self.uri = uri

    def __repr__(self):
        return self.label


class Nutrient:
    """ A nutrient in some food"""

    def __init__(self, tag, label=None, quantity=0, unit=None):
        self.tag = tag
        self.label = label or tag
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        if self.unit:
            name = "{label} * {quantity} {unit}".format(label=self.label,
                                                        quantity=self.quantity,
                                                        unit=self.unit)
        else:
            name = "{quantity} * {label}".format(label=self.label,
                                                 quantity=self.quantity)
        return name


class Ingredient:
    """ Nutritional data about an ingredient of some food """

    def __init__(self,
                 name,
                 uri="",
                 dietLabels=None,
                 healthLabels=None,
                 yields=1.0,
                 cautions=None,
                 totalDaily=None,
                 totalWeight=0,
                 calories=0,
                 totalNutrients=None):
        self.name = name
        self.dietLabels = dietLabels or []
        self.healthLabels = healthLabels or []
        self.uri = uri
        self.yields = yields
        self.cautions = cautions
        self.totalDaily = []
        if isinstance(totalDaily, dict):
            for n in totalDaily:
                self.totalDaily += [Nutrient(n, **totalDaily[n])]
        else:
            self.totalDaily = totalDaily or []
        self.totalWeight = totalWeight
        self.calories = calories
        self.totalNutrients = []
        if isinstance(totalNutrients, dict):
            for n in totalNutrients:
                self.totalNutrients += [Nutrient(n, **totalNutrients[n])]
        else:
            self.totalNutrients = totalNutrients or []

    def __str__(self):
        return self.name


class Food:
    """ something you can eat """

    def __init__(self, foodId, label="",
                 category="Generic foods",
                 categoryLabel="",
                 measure=None,
                 quantity=1,
                 nutrients=None,
                 image=None):
        self.foodId = foodId
        self.label = label
        self.category = category
        self.categoryLabel = categoryLabel
        if isinstance(measure, dict):
            measure = Measure(**measure)
        self.measure = measure
        self.nutrients = []
        if isinstance(nutrients, dict):
            for n in nutrients:
                self.nutrients += [Nutrient(n, quantity=nutrients[n])]
        else:
            self.nutrients = nutrients or []
        self.quantity = quantity
        self.image = image

    def __str__(self):
        if self.quantity != 1:
            return str(self.quantity) + " * " + self.label
        return self.label


class Recipe:
    def __init__(self,
                 label,
                 uri="",
                 url="",
                 share_url="",
                 image=None,
                 dietLabels=None,
                 healthLabels=None,
                 yields=1.0,
                 cautions=None,
                 totalDaily=None,
                 totalWeight=0,
                 calories=0,
                 totalTime=0,
                 totalNutrients=None,
                 digest=None,
                 ingredients=None,
                 source="edamam",
                 ingredient_names=None,
                 edamam=None):
        self.ingredient_names = ingredient_names or []
        self.ingredient_quantities = ingredients or []
        self.label = label
        self.dietLabels = dietLabels or []
        self.healthLabels = healthLabels or []
        self.uri = uri
        self.url = url or self.uri
        self.share_url = share_url or self.url
        self.yields = yields
        self.cautions = cautions
        self.totalDaily = []
        if isinstance(totalDaily, dict):
            for n in totalDaily:
                self.totalDaily += [Nutrient(n, **totalDaily[n])]
        else:
            self.totalDaily = totalDaily or []
        self.totalWeight = totalWeight
        self.calories = calories
        self.totalTime = totalTime
        self.totalNutrients = []
        if isinstance(totalNutrients, dict):
            for n in totalNutrients:
                self.totalNutrients += [Nutrient(n, **totalNutrients[n])]
        else:
            self.totalNutrients = totalNutrients or []
        self.image = image
        if isinstance(digest, list):
            self.digest = {}
            for content in digest:
                self.digest[content["label"]] = content
        else:
            self.digest = digest or {}
        self.__edamam = edamam or Edamam()

    def get_ingredients_data(self):
        for ing in self.__edamam.search_nutrient(self.ingredient_names):
            yield ing

    def __str__(self):
        return self.label