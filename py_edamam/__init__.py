import requests
import json


class Edaman(object):
    def __init__(self, nutrition_appid=None, nutrition_appkey=None,
                 recipes_appid=None, recipes_appkey=None):
        self.nutrition_appid = nutrition_appid
        self.nutrition_appkey = nutrition_appkey
        self.recipes_appid = recipes_appid
        self.recipes_appkey = recipes_appkey

    def search_recipe(self, query="chicken"):
        url = 'https://api.edamam.com/search?q=' + query + '&app_id=' + \
              self.recipes_appid + '&app_key=' + \
              self.recipes_appkey

        r = requests.get(url)
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

    def search_nutrient(self, query="1 large apple", servings=1):
        ingredient = self.search_food(query)
        ingredients = [{"quantity": ingredient.get("quantity"),
                        "foodURI": ingredient["food"]["uri"],
                        "measureURI": ingredient.get("measure", {}).get(
                            "uri")}]

        url = 'https://api.edamam.com/api/food-database/nutrients?app_id=' + \
              self.nutrition_appid + '&app_key=' + self.nutrition_appkey

        data = {"ingredients": ingredients, "yield": servings}
        r = requests.post(url,
                          headers={"Content-Type": "application/json"},
                          data=json.dumps(data))
        data = r.json()
        if "error" in data:
            return None
        data["ingredients"] = data["ingredients"][0]["parsed"][0]
        data["name"] = ingredient["food"]["label"]
        return data

    def search_food(self, query="pizza"):
        query = query.replace(" ", "%20")
        url = 'https://api.edamam.com/api/food-database/parser?ingr=' + \
            query + '&app_id=' + self.nutrition_appid + '&app_key=' + \
            self.nutrition_appkey + '&page=0'
        r = requests.get(url)
        return r.json()["parsed"][0]

    def pretty_nutrient(self, query="cheese"):
        n = self.search_nutrient(query)
        sentences = []
        if n is None:
            query = "1 piece of " + query
            n = self.search_nutrient(query)
            if n is None:
                return "could not find nutrients for " + query
        if not n["ingredients"]["status"] == "MISSING_QUANTITY":
            text = str(n["ingredients"]["quantity"]) + " " + \
                   n["ingredients"]["measure"] + " " + \
                   n["ingredients"]["food"] + " has;"
        else:
            text = n["ingredients"]["food"] + " has;"
        sentences.append(text)
        sentences.append(str(n["calories"]) + " calories")

        for nutrient in n["totalNutrients"]:
            nutrient = n["totalNutrients"][nutrient]
            text = "\n" + str(nutrient["quantity"]) + " " + nutrient[
                "unit"] + " of " + nutrient["label"]

            text = text.replace(" mg", " milligram")\
                       .replace(" ug", " microgram")\
                       .replace(" g ", " gram ")\
                       .replace("kcal", "kilo calories")\
                       .replace(" cal ", " calories ")
            sentences.append(text)
        return "\n".join(sentences)