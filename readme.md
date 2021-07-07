# Py_edamam

python api for https://developer.edamam.com


## install

    pip install py_edamam

## usage

working with json data directly

```python
from py_edamam import Edamam

e = Edamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')
           
print(e.search_nutrient("1 large apple"))
print(e.search_recipe("onion and chicken"))
print(e.search_food("coke"))
```

working with python objects

```python
from py_edamam import PyEdamam

e = PyEdamam(nutrition_appid='xxx',
           nutrition_appkey='xxx',
           recipes_appid='xxx',
           recipes_appkey='xxx',
           food_appid='xxx',
           food_appkey='xxx')

for recipe in e.search_recipe("onion and chicken"):
    print(recipe)
    print(recipe.calories)
    print(recipe.cautions, recipe.dietLabels, recipe.healthLabels)
    print(recipe.url)
    print(recipe.ingredient_quantities)
    break

for nutrient_data in e.search_nutrient("2 egg whites"):
    print(nutrient_data)
    print(nutrient_data.calories)
    print(nutrient_data.cautions, nutrient_data.dietLabels,
          nutrient_data.healthLabels)
    print(nutrient_data.totalNutrients)
    print(nutrient_data.totalDaily)

for food in e.search_food("coffee and pizza"):
    print(food)
    print(food.category)
```

## Credits

[Edamam](https://www.edamam.com/)

[JarbasAI](https://jarbasal.github.io
