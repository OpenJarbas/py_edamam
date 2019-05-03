#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py_edamam import Edamam

e = Edamam(recipes_appid='ecxxxb',
           recipes_appkey='83347a87xxxde8106646')


recipes_list = e.search_recipe("onion and chicken")

# keys scrapped from web demo, but you can provide yours above
nutrient_data = e.search_nutrient("1 large apple")

foods_list = e.search_food("coke")

from pprint import pprint

pprint(nutrient_data)
pprint(foods_list)
pprint(recipes_list)