import requests
import json
import logging

from py_edamam.exceptions import APIError, InvalidFoodApiKey, \
    InvalidNutrientsApiKey, InvalidRecipeApiKey, LowQualityQuery

logger = logging.getLogger("PyEdaman")


class Edaman(object):
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

        hits = r.json()["hits"]

        recipes = {}
        for hit in hits:
            recipe = hit["recipe"]
            name = recipe["label"]
            recipes[name] = {}
            recipes[name]["nutrients"] = recipe["totalNutrients"]
            recipes[name]["cautions"] = recipe["cautions"]
            recipes[name]["health_labels"] = recipe["healthLabels"]
            recipes[name]["diet_labels"] = recipe["dietLabels"]
            recipes[name]["calories"] = recipe["calories"]
            recipes[name]["ingredients"] = recipe["ingredientLines"]
            recipes[name]["url"] = recipe["url"]
        return recipes

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
        return r["parsed"]
